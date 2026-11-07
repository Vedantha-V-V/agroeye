# ============================================================
# AgroEye Phase 2 — FastAPI Inference Server
# Run: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
# ============================================================

import os, glob, base64, json, subprocess
from pathlib import Path
from datetime import datetime

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image

# ── Paths & Config ───────────────────────────────────────────
BASE_DIR        = Path(__file__).resolve().parent
FRAME_DIR       = BASE_DIR / "frames"
FRAME_DIR.mkdir(parents=True, exist_ok=True)

MODEL_NAME      = "wambugu71/crop_leaf_diseases_vit"
LOCAL_FINETUNED = BASE_DIR / "finetuned"
LOCAL_CACHE     = BASE_DIR / "model_cache"
FRAME_SIZE      = (224, 224)
DB_PROFILES     = BASE_DIR / "db" / "profiles.json"

if LOCAL_FINETUNED.exists() and (LOCAL_FINETUNED / "config.json").exists():
    MODEL_SOURCE = str(LOCAL_FINETUNED)
elif LOCAL_CACHE.exists():
    MODEL_SOURCE = str(LOCAL_CACHE)
else:
    MODEL_SOURCE = MODEL_NAME

app = FastAPI(title="AgroEye Inference Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Model Pipeline Setup ──────────────────────────────────────
classifier = None

def get_classifier():
    global classifier
    if classifier is None:
        try:
            from transformers import pipeline
            print(f"Loading model from: {MODEL_SOURCE}")
            classifier = pipeline(
                "image-classification",
                model=MODEL_SOURCE,
                device=-1       # CPU always
            )
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Warning: Failed to load model ({e})")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Model could not be loaded: {str(e)}"
            )
    return classifier

# ── State ─────────────────────────────────────────────────────
state = {
    "last_frame": None,
    "last_result": None,
    "ffmpeg_process": None,
    "stream_key": None
}

# ── Auth & Stream Schemas ─────────────────────────────────────
class LoginRequest(BaseModel):
    username: str
    password: str

class StreamStartRequest(BaseModel):
    stream_key: str

def load_profile() -> dict:
    if not DB_PROFILES.exists():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Profile database not found"
        )
    with open(DB_PROFILES, "r", encoding="utf-8") as f:
        return json.load(f)

# ── Helpers ───────────────────────────────────────────────────
def get_latest_frame(folder: Path) -> Path | None:
    frames = sorted(
        glob.glob(f"{folder}/*.jpg") + glob.glob(f"{folder}/*.png"),
        key=os.path.getmtime
    )
    return Path(frames[-1]) if frames else None


def parse_label(label: str, score: float) -> dict:
    label_clean = label.replace("_", " ").strip()
    is_healthy  = "healthy" in label_clean.lower()

    if is_healthy:
        return {
            "crop_health_score": round(score, 3),
            "disease_detected":  False,
            "disease_name":      None,
            "anomaly_flags":     []
        }

    health = round(1.0 - score, 3)
    flags  = []
    l      = label_clean.lower()
    if any(k in l for k in ["blight", "rot", "wilt"]):   flags.append("wilting")
    if any(k in l for k in ["spot", "rust", "mold", "mildew"]): flags.append("lesions")
    if any(k in l for k in ["mosaic", "virus", "yellow"]):flags.append("yellowing")
    if any(k in l for k in ["pest", "mite", "aphid"]):   flags.append("pest_damage")

    return {
        "crop_health_score": health,
        "disease_detected":  True,
        "disease_name":      label_clean,
        "anomaly_flags":     flags if flags else ["anomaly_detected"]
    }


# ── Auth Endpoints ────────────────────────────────────────────
@app.post("/auth/login")
def login(req: LoginRequest):
    profile = load_profile()
    if req.username == profile.get("username") and req.password == profile.get("password"):
        return {
            "success": True,
            "user": {
                "username": profile.get("username"),
                "display": profile.get("display", "Admin")
            }
        }
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password"
    )


@app.get("/auth/profile")
def get_profile():
    profile = load_profile()
    return {
        "username": profile.get("username"),
        "display": profile.get("display", "Admin")
    }


# ── Stream Endpoints ──────────────────────────────────────────
@app.post("/stream/start")
def start_stream(req: StreamStartRequest):
    proc = state["ffmpeg_process"]
    if proc is not None and proc.poll() is None:
        return {
            "status": "already_running",
            "stream_key": state["stream_key"]
        }

    key = req.stream_key.strip()
    if not key:
        raise HTTPException(status_code=400, detail="Stream key is required")

    stream_url = key if (key.startswith("rtmp://") or key.startswith("http://")) else f"rtmp://localhost:1935/live/{key}"

    output_pattern = str(FRAME_DIR / "frame_%Y%m%d_%H%M%S.jpg")
    cmd = [
        "ffmpeg",
        "-y",
        "-i", stream_url,
        "-vf", "fps=0.5",
        "-strftime", "1",
        output_pattern
    ]

    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
        )
        state["ffmpeg_process"] = process
        state["stream_key"] = key
        return {
            "status": "started",
            "stream_key": key,
            "stream_url": stream_url
        }
    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail="ffmpeg executable not found in system PATH"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to start ffmpeg: {str(e)}"
        )


@app.post("/stream/stop")
def stop_stream():
    proc = state["ffmpeg_process"]
    if proc is not None and proc.poll() is None:
        try:
            proc.terminate()
            proc.wait(timeout=3)
        except Exception:
            proc.kill()

    state["ffmpeg_process"] = None
    state["stream_key"] = None
    return {"status": "stopped"}


@app.get("/stream/status")
def stream_status():
    proc = state["ffmpeg_process"]
    is_running = proc is not None and proc.poll() is None
    return {
        "is_streaming": is_running,
        "stream_key": state["stream_key"]
    }


# ── Health & Inference Endpoints ──────────────────────────────
@app.get("/health")
def health():
    return {
        "model_connected": True,
        "model":           MODEL_SOURCE,
        "device":          "cpu",
        "status":          "ready"
    }


@app.get("/infer")
def infer():
    frame_path = get_latest_frame(FRAME_DIR)

    if frame_path is None:
        raise HTTPException(404, detail="No frames found in FRAME_DIR. Waiting for stream input...")

    if str(frame_path) == state["last_frame"] and state["last_result"] is not None:
        return state["last_result"]

    clf = get_classifier()

    try:
        img    = Image.open(frame_path).convert("RGB").resize(FRAME_SIZE, Image.LANCZOS)
        top    = clf(img, top_k=1)[0]
        parsed = parse_label(top["label"], top["score"])

        with open(frame_path, "rb") as f:
            frame_bytes = f.read()
            frame_base64 = base64.b64encode(frame_bytes).decode("utf-8")

        state["last_frame"] = str(frame_path)
        result = {
            **parsed,
            "confidence":      round(top["score"], 3),
            "timestamp":       datetime.utcnow().isoformat() + "Z",
            "source_frame":    frame_path.name,
            "model_connected": True,
            "frame_base64":    frame_base64
        }
        state["last_result"] = result
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Inference error: {str(e)}"
        )

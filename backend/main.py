# ============================================================
# AgroEye Phase 2 — FastAPI Inference Server
# Run: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
# ============================================================

import os, glob, base64, json, subprocess, threading, time, shutil
from pathlib import Path
from datetime import datetime
from collections import deque
from typing import Optional

from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent / ".env")

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from PIL import Image

from leaf_detector import LeafDetector

# ── Insights (Gemini + Qdrant RAG) ───────────────────────────────
from insights import embed_all, embed_profile, embed_inferences, generate_insight, retrieve_context

# ── Paths & Config ───────────────────────────────────────────
BASE_DIR         = Path(__file__).resolve().parent
FRAME_DIR        = BASE_DIR / "frames"
FRAME_DIR.mkdir(parents=True, exist_ok=True)

DB_DIR           = BASE_DIR / "db"
DB_IMAGES_DIR    = DB_DIR / "images"
DB_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
DB_METADATA_FILE = DB_DIR / "inferences.json"
DB_PROFILES      = DB_DIR / "profiles.json"

MODEL_NAME       = "wambugu71/crop_leaf_diseases_vit"
LOCAL_FINETUNED  = BASE_DIR / "finetuned"
LOCAL_CACHE      = BASE_DIR / "model_cache"
FRAME_SIZE       = (224, 224)
NGINX_PATH       = Path(r"C:\nginx-rtmp\nginx.exe")
NGINX_DIR        = NGINX_PATH.parent

# Threshold for archiving disease frames to db/images
DISEASE_CONFIDENCE_THRESHOLD = 0.60

leaf_detector = LeafDetector(yolo_path=BASE_DIR / "models" / "yolo11m.pt")

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

app.mount("/db/images", StaticFiles(directory=str(DB_IMAGES_DIR)), name="db_images")

# ── State & Logs ──────────────────────────────────────────────
log_buffer = deque(maxlen=200)

def add_log(msg: str):
    timestamp = datetime.now().strftime("%H:%M:%S")
    formatted = f"[{timestamp}] {msg}"
    log_buffer.append(formatted)
    print(formatted)

def read_pipe(pipe, prefix: str):
    try:
        for line in iter(pipe.readline, ''):
            if not line:
                break
            clean_line = line.strip()
            if clean_line:
                add_log(f"[{prefix}] {clean_line}")
    except Exception:
        pass
    finally:
        try:
            pipe.close()
        except Exception:
            pass

state = {
    "last_frame": None,
    "last_result": None,
    "nginx_process": None,
    "ffmpeg_process": None,
    "stream_key": None
}

# ── Model Pipeline Setup ──────────────────────────────────────
classifier = None

def get_classifier():
    global classifier
    if classifier is None:
        try:
            from transformers import pipeline
            add_log(f"[MODEL] Loading model from: {MODEL_SOURCE}")
            classifier = pipeline(
                "image-classification",
                model=MODEL_SOURCE,
                device=-1       # CPU always
            )
            add_log("[MODEL] Model loaded successfully.")
        except Exception as e:
            add_log(f"[MODEL ERROR] Failed to load model: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Model could not be loaded: {str(e)}"
            )
    return classifier

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

def save_disease_metadata(record: dict):
    records = []
    if DB_METADATA_FILE.exists():
        try:
            with open(DB_METADATA_FILE, "r", encoding="utf-8") as f:
                records = json.load(f)
        except Exception:
            records = []

    # Insert latest record at the front
    records.insert(0, record)
    try:
        with open(DB_METADATA_FILE, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2)
    except Exception as e:
        add_log(f"[DB ERROR] Failed to write metadata: {str(e)}")

# ── Subprocess Management ─────────────────────────────────────
def start_nginx():
    if not NGINX_PATH.exists():
        add_log(f"[NGINX ERROR] Executable not found at {NGINX_PATH}")
        raise FileNotFoundError(f"Nginx binary not found at {NGINX_PATH}")

    add_log(f"[NGINX] Starting RTMP server from {NGINX_PATH}...")
    proc = subprocess.Popen(
        [str(NGINX_PATH)],
        cwd=str(NGINX_DIR),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    )
    threading.Thread(target=read_pipe, args=(proc.stdout, "NGINX"), daemon=True).start()
    threading.Thread(target=read_pipe, args=(proc.stderr, "NGINX"), daemon=True).start()
    add_log(f"[NGINX] RTMP server started (PID: {proc.pid})")
    return proc

def stop_nginx(proc):
    add_log("[NGINX] Stopping Nginx RTMP server...")
    if NGINX_PATH.exists():
        try:
            subprocess.run(
                [str(NGINX_PATH), "-s", "stop"],
                cwd=str(NGINX_DIR),
                timeout=2,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except Exception:
            pass

    if proc is not None:
        try:
            proc.terminate()
            proc.wait(timeout=2)
        except Exception:
            try:
                proc.kill()
            except Exception:
                pass

    if os.name == "nt":
        try:
            subprocess.run(["taskkill", "/F", "/IM", "nginx.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass

    add_log("[NGINX] RTMP server stopped.")

def start_ffmpeg(stream_url: str, output_pattern: str):
    add_log(f"[FFMPEG] Starting frame extraction from {stream_url}...")
    cmd = [
        "ffmpeg",
        "-y",
        "-i", stream_url,
        "-vf", "fps=0.5",
        "-strftime", "1",
        output_pattern
    ]
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    )
    threading.Thread(target=read_pipe, args=(proc.stdout, "FFMPEG"), daemon=True).start()
    threading.Thread(target=read_pipe, args=(proc.stderr, "FFMPEG"), daemon=True).start()
    add_log(f"[FFMPEG] Extraction process active (PID: {proc.pid})")
    return proc

def stop_ffmpeg(proc):
    add_log("[FFMPEG] Stopping FFmpeg process...")
    if proc is not None:
        try:
            proc.terminate()
            proc.wait(timeout=3)
        except Exception:
            try:
                proc.kill()
            except Exception:
                pass
    add_log("[FFMPEG] Process stopped.")

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
                "display": profile.get("display", "Admin"),
                "location": profile.get("location", "Bengaluru")
            }
        }
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password"
    )

@app.get("/auth/profile")
def get_profile():
    profile = load_profile()
    return profile

# ── Stream Endpoints ──────────────────────────────────────────
@app.post("/stream/start")
def start_stream(req: StreamStartRequest):
    key = req.stream_key.strip()
    if not key:
        raise HTTPException(status_code=400, detail="Stream key is required")

    if state["ffmpeg_process"] is not None and state["ffmpeg_process"].poll() is None:
        return {
            "status": "already_running",
            "stream_key": state["stream_key"]
        }

    add_log(f"[PIPELINE] Initializing stream pipeline for key: '{key}'")

    # Step 1: Start Nginx RTMP server
    try:
        nginx_proc = start_nginx()
        state["nginx_process"] = nginx_proc
    except Exception as e:
        add_log(f"[PIPELINE ERROR] Nginx startup failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to start Nginx RTMP server: {str(e)}"
        )

    time.sleep(1.0)  # Wait for RTMP port binding

    # Step 2: Start FFmpeg reading the RTMP stream
    stream_url = key if (key.startswith("rtmp://") or key.startswith("http://")) else f"rtmp://localhost:1935/live/{key}"
    output_pattern = str(FRAME_DIR / "frame_%Y%m%d_%H%M%S.jpg")

    try:
        ffmpeg_proc = start_ffmpeg(stream_url, output_pattern)
        state["ffmpeg_process"] = ffmpeg_proc
        state["stream_key"] = key
        add_log("[PIPELINE] Ingest pipeline running successfully.")
        return {
            "status": "started",
            "stream_key": key,
            "stream_url": stream_url
        }
    except Exception as e:
        stop_nginx(state["nginx_process"])
        state["nginx_process"] = None
        add_log(f"[PIPELINE ERROR] FFmpeg startup failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to start FFmpeg: {str(e)}"
        )

@app.post("/stream/stop")
def stop_stream():
    add_log("[PIPELINE] Stop request received. Teardown sequence started.")

    # 1. Close FFmpeg first
    if state["ffmpeg_process"] is not None:
        stop_ffmpeg(state["ffmpeg_process"])
        state["ffmpeg_process"] = None

    # 2. Close Nginx RTMP server second
    if state["nginx_process"] is not None:
        stop_nginx(state["nginx_process"])
        state["nginx_process"] = None
    else:
        stop_nginx(None)

    state["stream_key"] = None
    add_log("[PIPELINE] All streaming services stopped successfully.")
    return {"status": "stopped"}

@app.get("/stream/status")
def stream_status():
    proc = state["ffmpeg_process"]
    is_running = proc is not None and proc.poll() is None
    return {
        "is_streaming": is_running,
        "stream_key": state["stream_key"]
    }

@app.get("/stream/logs")
def stream_logs():
    return {
        "logs": list(log_buffer),
        "is_streaming": state["ffmpeg_process"] is not None and state["ffmpeg_process"].poll() is None
    }

# ── Health & Inference Endpoints ──────────────────────────────

# ── Insights Schemas ──────────────────────────────────────────
class InsightQueryRequest(BaseModel):
    query: str

class EmbedRequest(BaseModel):
    pass

# ── Insights Endpoints ─────────────────────────────────────────
@app.post("/insights/embed")
def insights_embed():
    """Embed profile + high-severity inferences into Qdrant."""
    try:
        result = embed_all()
        add_log(f"[INSIGHTS] Embedding complete: {result}")
        return {"status": "ok", "result": result}
    except Exception as e:
        add_log(f"[INSIGHTS ERROR] Embedding failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/insights/query")
def insights_query(req: InsightQueryRequest):
    """RAG: retrieve context from Qdrant and generate Gemini insight."""
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    try:
        profile = load_profile()
        result = generate_insight(req.query, profile=profile)
        add_log(f"[INSIGHTS] Query answered: {req.query[:60]}")
        return result
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        add_log(f"[INSIGHTS ERROR] {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/insights/context")
def insights_context(query: str, top_k: int = 5):
    """Return raw Qdrant retrieval results for a query (debugging)."""
    try:
        hits = retrieve_context(query, top_k=top_k)
        return {"query": query, "hits": hits}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {
        "model_connected": True,
        "model":           MODEL_SOURCE,
        "device":          "cpu",
        "status":          "ready"
    }

@app.get("/inferences")
def get_past_inferences():
    if not DB_METADATA_FILE.exists():
        return {"inferences": []}
    try:
        with open(DB_METADATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return {"inferences": data}
    except Exception:
        return {"inferences": []}

@app.get("/infer")
def infer():
    frame_path = get_latest_frame(FRAME_DIR)

    if frame_path is None:
        raise HTTPException(404, detail="No frames found in FRAME_DIR. Waiting for stream input...")

    if str(frame_path) == state["last_frame"] and state["last_result"] is not None:
        return state["last_result"]

    try:
        img = Image.open(frame_path).convert("RGB").resize(FRAME_SIZE, Image.LANCZOS)

        with open(frame_path, "rb") as f:
            frame_bytes = f.read()
            frame_base64 = base64.b64encode(frame_bytes).decode("utf-8")

        timestamp  = datetime.utcnow().isoformat() + "Z"
        frame_name = frame_path.name

        # ── Stage 1: Fast Leaf Presence Check ────────────────────────
        has_leaf, leaf_score, reason = leaf_detector.is_leaf_present(img)
        if not has_leaf:
            add_log(f"[INFER] Frame '{frame_name}' skipped: No leaf detected ({reason}, score: {leaf_score}).")
            state["last_frame"] = str(frame_path)
            result = {
                "leaf_detected":     False,
                "crop_health_score": None,
                "disease_detected":  False,
                "disease_name":      "No Leaf Detected",
                "anomaly_flags":     ["no_plant_tissue_detected"],
                "confidence":        0.0,
                "timestamp":         timestamp,
                "source_frame":      frame_name,
                "model_connected":   True,
                "frame_base64":      frame_base64,
                "saved_to_db":       False,
                "image_url":         None
            }
            state["last_result"] = result
            return result

        # ── Stage 2: Disease Classification (only if leaf is present) ──
        clf    = get_classifier()
        top    = clf(img, top_k=1)[0]
        parsed = parse_label(top["label"], top["score"])

        confidence = round(top["score"], 3)
        is_disease = parsed["disease_detected"] and confidence >= DISEASE_CONFIDENCE_THRESHOLD
        saved_to_db = False
        image_url = None

        # If disease detected with high confidence, move to db/images and save metadata
        if is_disease:
            dest_image_path = DB_IMAGES_DIR / frame_name
            try:
                shutil.move(str(frame_path), str(dest_image_path))
                saved_to_db = True
                image_url = f"/db/images/{frame_name}"

                meta_entry = {
                    "id": datetime.utcnow().strftime("%Y%m%d%H%M%S%f"),
                    "filename": frame_name,
                    "image_url": image_url,
                    "crop_health_score": parsed["crop_health_score"],
                    "disease_detected": parsed["disease_detected"],
                    "disease_name": parsed["disease_name"],
                    "confidence": confidence,
                    "anomaly_flags": parsed["anomaly_flags"],
                    "timestamp": timestamp,
                    "source_frame": frame_name,
                    "saved_to_db": True
                }
                save_disease_metadata(meta_entry)
                add_log(f"[DB] Saved high confidence disease frame ({parsed['disease_name']} @ {confidence}) to db/images/{frame_name}")
                state["last_frame"] = str(dest_image_path)
            except Exception as move_err:
                add_log(f"[DB ERROR] Moving frame to db/images failed: {str(move_err)}")
                state["last_frame"] = str(frame_path)
        else:
            state["last_frame"] = str(frame_path)

        result = {
            **parsed,
            "leaf_detected":   True,
            "confidence":      confidence,
            "timestamp":       timestamp,
            "source_frame":    frame_name,
            "model_connected": True,
            "frame_base64":    frame_base64,
            "saved_to_db":     saved_to_db,
            "image_url":       image_url
        }
        state["last_result"] = result
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Inference error: {str(e)}"
        )

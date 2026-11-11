"""
AgroEye AI Insights Module
- Embeddings: local sentence-transformers (all-MiniLM-L6-v2, dim=384)
- Generation: Google Gemini 1.5 Flash via google-genai SDK
- Vector store: Qdrant
Install: pip install sentence-transformers google-genai qdrant-client
"""

import json, os, hashlib, warnings
from pathlib import Path
from datetime import datetime
from typing import Optional

warnings.filterwarnings("ignore", category=FutureWarning)

from sentence_transformers import SentenceTransformer
from google import genai
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct

# ── Config ────────────────────────────────────────────────────────
BASE_DIR        = Path(__file__).resolve().parent
DB_DIR          = BASE_DIR / "db"
METADATA_FILE   = DB_DIR / "inferences.json"
PROFILES_FILE   = DB_DIR / "profiles.json"

QDRANT_HOST     = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT     = int(os.getenv("QDRANT_PORT", "6333"))
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION", "agroeye_insights")
GEMINI_API_KEY  = os.getenv("GEMINI_API_KEY", "")

CHAT_MODEL      = "gemini-3.5-flash-lite"
EMBED_DIM       = 384          # all-MiniLM-L6-v2
EMBED_THRESHOLD = 0.40

# Load local embedding model once at startup
_embed_model = SentenceTransformer("all-MiniLM-L6-v2")


def _embed(text: str) -> list[float]:
    return _embed_model.encode(text, normalize_embeddings=True).tolist()


def _gemini_client() -> genai.Client:
    key = os.getenv("GEMINI_API_KEY", GEMINI_API_KEY)
    if not key:
        raise RuntimeError("GEMINI_API_KEY not set in backend/.env")
    return genai.Client(api_key=key)


def _qdrant() -> QdrantClient:
    return QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)


def _ensure_collection(qc: QdrantClient):
    existing = [c.name for c in qc.get_collections().collections]
    if COLLECTION_NAME not in existing:
        qc.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=EMBED_DIM, distance=Distance.COSINE),
        )


def _doc_id(text: str) -> int:
    return int(hashlib.sha256(text.encode()).hexdigest(), 16) % (2 ** 63)


# ── Embedding pipeline ────────────────────────────────────────────

def embed_profile(profile: dict) -> dict:
    text = (
        f"User: {profile.get('display', 'Admin')}. "
        f"Location: {profile.get('location', 'Unknown')}. "
        f"Land size: {profile.get('land_size', 'N/A')} acres. "
        f"Soil type: {profile.get('soil', 'Unknown')}. "
        f"Crops grown: {', '.join(profile.get('crops', []))}. "
        f"Language preference: {profile.get('language', 'English')}."
    )
    vec = _embed(text)
    qc = _qdrant()
    _ensure_collection(qc)
    qc.upsert(
        collection_name=COLLECTION_NAME,
        points=[PointStruct(
            id=_doc_id("profile:" + profile.get("username", "admin")),
            vector=vec,
            payload={
                "type": "profile",
                "username": profile.get("username"),
                "display": profile.get("display"),
                "location": profile.get("location"),
                "soil": profile.get("soil"),
                "crops": profile.get("crops", []),
                "land_size": profile.get("land_size"),
                "text": text,
                "embedded_at": datetime.utcnow().isoformat() + "Z",
            }
        )]
    )
    return {"embedded": 1, "type": "profile"}


def embed_inferences(inferences: list[dict]) -> dict:
    qc = _qdrant()
    _ensure_collection(qc)

    points = []
    for inf in inferences:
        if not inf.get("disease_detected"):
            continue
        conf = float(inf.get("confidence", 0.0))
        if conf < EMBED_THRESHOLD:
            continue

        disease   = inf.get("disease_name", "Unknown Disease")
        health    = inf.get("crop_health_score", "N/A")
        anomalies = inf.get("anomaly_flags", [])
        if isinstance(anomalies, list):
            anomalies = ", ".join(anomalies)
        ts    = inf.get("timestamp", "")
        frame = inf.get("source_frame", "")

        text = (
            f"Disease detected: {disease}. "
            f"Confidence: {round(conf * 100, 1)}%. "
            f"Crop health score: {health}. "
            f"Anomaly flags: {anomalies}. "
            f"Frame: {frame}. Timestamp: {ts}."
        )
        vec = _embed(text)
        points.append(PointStruct(
            id=_doc_id("inference:" + (inf.get("id") or frame or ts)),
            vector=vec,
            payload={
                "type": "inference",
                "disease_name": disease,
                "confidence": conf,
                "crop_health_score": health,
                "anomaly_flags": anomalies,
                "timestamp": ts,
                "source_frame": frame,
                "text": text,
            }
        ))

    if points:
        qc.upsert(collection_name=COLLECTION_NAME, points=points)
    return {"embedded": len(points), "type": "inferences"}


def embed_all() -> dict:
    results = {}
    if PROFILES_FILE.exists():
        with open(PROFILES_FILE, "r", encoding="utf-8") as f:
            profile = json.load(f)
        results["profile"] = embed_profile(profile)

    if METADATA_FILE.exists():
        with open(METADATA_FILE, "r", encoding="utf-8") as f:
            inferences = json.load(f)
        results["inferences"] = embed_inferences(inferences)
    else:
        results["inferences"] = {"embedded": 0, "type": "inferences"}

    return results


# ── Retrieval + Generation ─────────────────────────────────────────

def retrieve_context(query: str, top_k: int = 5) -> list[dict]:
    vec = _embed(query)
    qc = _qdrant()
    _ensure_collection(qc)
    hits = qc.query_points(
        collection_name=COLLECTION_NAME,
        query=vec,
        limit=top_k,
        with_payload=True,
    ).points
    return [{"score": round(h.score, 4), "payload": h.payload} for h in hits]


def generate_insight(query: str, profile: Optional[dict] = None) -> dict:
    if profile is None and PROFILES_FILE.exists():
        with open(PROFILES_FILE, "r", encoding="utf-8") as f:
            profile = json.load(f)

    profile_ctx = ""
    if profile:
        profile_ctx = (
            f"Farmer: {profile.get('display', 'Admin')}, "
            f"Location: {profile.get('location', 'Unknown')}, "
            f"Soil: {profile.get('soil', 'Unknown')}, "
            f"Crops: {', '.join(profile.get('crops', []))}, "
            f"Land size: {profile.get('land_size', 'N/A')} acres."
        )

    hits = retrieve_context(query, top_k=5)
    rag_ctx = "\n".join(
        f"- [{h['payload'].get('type', '?')}] {h['payload'].get('text', '')}"
        for h in hits
    )

    prompt = (
        f"You are AgroEye, an AI agricultural assistant.\n"
        f"Provide precise, actionable insights for the farmer.\n"
        f"Be concise but helpful. Use plain language.\n\n"
        f"--- Farmer Profile ---\n{profile_ctx}\n\n"
        f"--- Relevant Past Data ---\n{rag_ctx if rag_ctx else 'No prior records found.'}\n\n"
        f"--- Farmer's Question ---\n{query}\n\n"
        f"--- Your Answer ---\n"
    )

    c = _gemini_client()
    response = c.models.generate_content(model=CHAT_MODEL, contents=prompt)
    answer = response.text.strip() if response.text else "No response generated."

    return {
        "query": query,
        "answer": answer,
        "context_used": hits,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }

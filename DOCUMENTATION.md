# AgroEye Documentation

## System Architecture

AgroEye is an automated crop leaf disease monitoring system that integrates live RTMP/video ingestion, Vision Transformer (ViT) classification models, local vector embeddings, Qdrant vector database, Google Gemini RAG insights, FastAPI backend services, and a React web dashboard.

```
+------------------+         RTMP Feed          +---------------------------+
|  Drone / Camera  | ------------------------> |  Nginx RTMP (Port 1935)   |
+------------------+                           +---------------------------+
                                                             |
                                                             v (0.5 fps)
+------------------+         JSON / Base64     +---------------------------+
| React Dashboard  | <------------------------ |    FFmpeg Frame Ingest    |
| (Results & Logs) |        /infer endpoint    |  (C:\nginx-rtmp\nginx.exe)|
+------------------+                           +---------------------------+
         |                                                   |
         |                                                   v
         |                                     +---------------------------+
         |                                     |  ViT Crop Classifier      |
         |                                     |   (finetuned / hub)       |
         |                                     +---------------------------+
         |                                                   |
         |                                                   v (Inferences JSON)
         v                                     +---------------------------+
+------------------+                           | sentence-transformers     |
| AI Insights Page |                           | (all-MiniLM-L6-v2, 384d)  |
| (Chat & Sources) |                           +---------------------------+
+------------------+                                         |
   |            ^                                            v
   | /insights/ | RAG Context Hits             +---------------------------+
   | query      +----------------------------- | Qdrant Vector DB (:6333)  |
   v                                           +---------------------------+
+----------------------+                                     |
| Google Gemini        | <-----------------------------------+
| 1.5 Flash Generation |
+----------------------+
```

---

## 1. Prerequisites

- Python 3.10+
- Node.js 18+ and npm
- `ffmpeg` installed and accessible in system PATH
- Nginx with RTMP module (e.g. `C:\nginx-rtmp\nginx.exe`)
- Docker (for Qdrant vector database)
- Google Gemini API Key (`GEMINI_API_KEY`)

---

## 2. Ingest & Streaming Pipeline Lifecycle

1. **Stream Start Sequence**:
   - User enters stream key (e.g. `agroeye`) and clicks **Start Stream**.
   - Backend starts `C:\nginx-rtmp\nginx.exe` to bind the RTMP listener at port 1935.
   - After RTMP listener initialization, `ffmpeg` starts extracting frames at `0.5 fps` into `backend/frames/`.
   - Both Nginx and FFmpeg process logs are captured and broadcast to `GET /stream/logs`.
2. **Inference Loop**:
   - Frontend polls `GET /infer` to classify incoming frames with the ViT model.
   - Inferences are persisted in `backend/db/inferences.json`.
3. **Stream Teardown Sequence**:
   - User clicks **Stop Stream**.
   - Backend first terminates `ffmpeg` to flush and release frame handles.
   - Backend then stops `nginx.exe` cleanly (`nginx -s stop`).

---

## 3. AI Insights & Vector RAG Module

The AI Insights module (`backend/insights.py`) provides intelligent advisory and historical crop analysis for farmers:

- **Embeddings**: Uses local `sentence-transformers` (`all-MiniLM-L6-v2`, 384 dimensions) for embedding farmer profiles (`backend/db/profiles.json`) and high-severity inference records (`backend/db/inferences.json`). No external API call is used for vectorization.
- **Vector Search**: Vectors are stored in a Qdrant collection (`agroeye_insights`) with Cosine distance. Vector similarity search uses `QdrantClient.query_points()`.
- **RAG Generation**: Google Gemini 1.5 Flash (`google-genai` SDK) synthesizes responses grounded on retrieved context hits and the farmer's soil, crop, and location profile.

---

## 4. Backend Server & API Reference

### Running the Server

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Endpoints

#### Authentication & Profiles
- `POST /auth/login`: Authenticates user against `backend/db/profiles.json`.
- `GET /auth/profile`: Returns active user profile.

#### RTMP Streaming & Pipeline
- `POST /stream/start`: Starts Nginx RTMP server, then starts FFmpeg frame extraction.
- `POST /stream/stop`: Stops FFmpeg first, then stops Nginx server.
- `GET /stream/status`: Returns streaming state.
- `GET /stream/logs`: Returns live stdout/stderr log lines for Nginx and FFmpeg.

#### Inference & Health
- `GET /infer`: Performs inference on latest frame in `backend/frames/`.
- `GET /health`: Health status of model and server.

#### Insights & RAG
- `POST /insights/embed`: Triggers local vectorization of profile and inference history into Qdrant.
- `POST /insights/query`: Accepts `{"query": "..."}`, performs vector similarity retrieval via Qdrant, and returns Gemini 1.5 Flash generated answer with context sources.
- `GET /insights/context?query=...&top_k=5`: Returns raw Qdrant retrieval hits for debugging.

---

## 5. Frontend Dashboard

```bash
cd frontend
npm install
npm run dev
```

App routes:
- `/auth`: Login screen.
- `/`: Main dashboard (Stream control, live feed, RTMP/FFmpeg logs, detection statistics).
- `/inferences`: Historical detection table, filtering, and inspection.
- `/insights`: AI Insights chat interface with farm data embedder, suggestion chips, and context hit inspection.

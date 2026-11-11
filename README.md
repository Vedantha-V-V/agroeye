# AgroEye

AI-powered UAV crop disease detection, real-time monitoring, and agricultural insights system.

## Quick Start Guide

### 1. Run Qdrant Vector DB

```bash
docker run -d --name qdrant -p 6333:6333 -p 6334:6334 -v qdrant_data:/qdrant/storage qdrant/qdrant
```

### 2. Configure Environment Variables

Create or update `backend/.env`:

```env
GEMINI_API_KEY=your_gemini_api_key_here
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_COLLECTION=agroeye_insights
```

### 3. Run the Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

- Backend API: `http://localhost:8000`

### 4. Run the Frontend

```bash
cd frontend
npm install
npm run dev
```

- Frontend App: `http://localhost:5173`

### 5. Install and Setup Nginx RTMP for Windows

```ps1
C:\nginx-rtmp\nginx.exe
```

## Pipelines & Features

### Ingest & Inference Pipeline
1. Enter your Stream Key in the dashboard.
2. Click **Start Stream** — this automatically:
   - Starts the Nginx RTMP server (`C:\nginx-rtmp\nginx.exe`).
   - Starts `ffmpeg` to extract frames into `backend/frames/`.
   - Locks the stream key in the UI and streams live running logs to the dashboard.
3. Click the **Pipeline Logs** tab to view real-time debug outputs from Nginx and FFmpeg.
4. Click **Stop Stream** — this stops FFmpeg first, then terminates the Nginx server.

### AI Insights & Vector RAG Pipeline
1. Ensure Qdrant is running on port `6333` and `GEMINI_API_KEY` is set in `backend/.env`.
2. Navigate to **AI Insights** (`/insights`) in the dashboard.
3. Click **⬆ Embed Farm Data** to vectorize farm profiles and disease detection records into Qdrant using local `all-MiniLM-L6-v2` embeddings.
4. Use the interactive chat to query crop health, recurring patterns, and treatments powered by Google Gemini 3.5 Flash grounded on Qdrant context hits.

For full architecture and API details, see [DOCUMENTATION.md](DOCUMENTATION.md).

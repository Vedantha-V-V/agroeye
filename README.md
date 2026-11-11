# AgroEye

AI-powered UAV crop disease detection and real-time monitoring system.

## Quick Start Guide

### 1. Run the Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

- Backend API: `http://localhost:8000`

### 2. Run the Frontend

```bash
cd frontend
npm install
npm run dev
```

- Frontend App: `http://localhost:5173`


### 3. Start Nginx RTMP for Windows

```ps1
C:\nginx-rtmp\nginx.exe
```

### 4. Start FFmpeg

```ps1
ffmpeg -i rtmp://localhost:1935/live/agroeye -vf fps=0.5 -strftime 1 path\to\store\images\frames\frame_%Y%m%d_%H%M%S.jpg
```

### 4. Running the Ingest & Inference Pipeline

1. Enter your Stream Key (e.g. `agroeye`) in the dashboard.
2. Click **Start Stream** — this automatically:
   - Starts the Nginx RTMP server (`C:\nginx-rtmp\nginx.exe`).
   - Starts `ffmpeg` to extract frames into `backend/frames/`.
   - Locks the stream key in the UI and streams live running logs to the dashboard.
3. Click the **Pipeline Logs** tab to view real-time debug outputs from Nginx and FFmpeg.
4. Click **Stop Stream** — this stops FFmpeg first, then terminates the Nginx server.

For full architecture and API details, see [DOCUMENTATION.md](DOCUMENTATION.md).
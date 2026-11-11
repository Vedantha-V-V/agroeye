# AgroEye Documentation

## System Architecture

AgroEye is an automated crop leaf disease monitoring system that integrates live RTMP/video ingestion, Vision Transformer (ViT) classification models, FastAPI backend services, and a React web dashboard.

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
                                                             |
                                                             v
                                               +---------------------------+
                                               |  ViT Crop Classifier      |
                                               |   (finetuned / hub)       |
                                               +---------------------------+
```

---

## 1. Prerequisites

- Python 3.10+
- Node.js 18+ and npm
- `ffmpeg` installed and accessible in system PATH
- Nginx with RTMP module

---

## 2. Ingest & Streaming Pipeline Lifecycle

1. **Stream Start Sequence**:
   - User enters stream key (e.g. `agroeye`) and clicks **Start Stream**.
   - Backend first starts `C:\nginx-rtmp\nginx.exe` to bind the RTMP listener at port 1935.
   - After RTMP listener initialization, `ffmpeg` starts extracting frames at `0.5 fps` into `backend/frames/`.
   - Both Nginx and FFmpeg process logs are captured and broadcast to `GET /stream/logs`.
2. **Inference Loop**:
   - Frontend polls `GET /infer` to classify incoming frames with the ViT model.
3. **Stream Teardown Sequence**:
   - User clicks **Stop Stream**.
   - Backend first terminates `ffmpeg` to flush and release frame handles.
   - Backend then stops `nginx.exe` cleanly (`nginx -s stop`).

---

## 3. Running the Backend Server

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Start the FastAPI server:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

### API Endpoints

- `POST /auth/login`: Authenticates user against `backend/db/profiles.json`.
- `GET /auth/profile`: Returns active user profile.
- `POST /stream/start`: Starts Nginx RTMP server, then starts FFmpeg frame extraction.
- `POST /stream/stop`: Stops FFmpeg first, then stops Nginx server.
- `GET /stream/status`: Returns streaming state.
- `GET /stream/logs`: Returns live stdout/stderr log lines for Nginx and FFmpeg.
- `GET /infer`: Performs inference on latest frame in `backend/frames/`.
- `GET /health`: Health status of model and server.

---

## 4. Running the Frontend Dashboard

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

2. Open `http://localhost:5173`.
   - Login with the credentials at profile.json
   - Enter stream key and click **Start Stream**.
   - Switch between **Results Obtained** and **Pipeline Logs** tabs to monitor both Nginx RTMP and FFmpeg in real-time.

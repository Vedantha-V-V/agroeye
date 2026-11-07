# AgroEye Documentation

## System Architecture

AgroEye is an automated crop leaf disease monitoring system that integrates live RTMP/video ingestion, Vision Transformer (ViT) classification models, FastAPI backend services, and a React web dashboard.

```
+------------------+         RTMP Feed          +----------------------+
|  Drone / Camera  | ------------------------> | FFMPEG Frame Ingest  |
+------------------+                           +----------------------+
                                                          |
                                                          v (0.5 fps)
+------------------+         JSON / Base64     +----------------------+
| React Dashboard  | <------------------------ |   FastAPI Backend    |
+------------------+        /infer endpoint    |      (main.py)       |
                                               +----------------------+
                                                          |
                                                          v
                                               +----------------------+
                                               |  ViT Crop Classifier |
                                               |   (finetuned / hub)  |
                                               +----------------------+
```

---

## 1. Prerequisites

- Python 3.10+
- Node.js 18+ and npm
- `ffmpeg` installed and accessible in system PATH

---

## 2. Running the Backend Server

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Activate virtual environment (if using one):
   ```bash
   # Windows PowerShell:
   ..\.venv\Scripts\Activate.ps1
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the FastAPI server:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

The backend server exposes the following endpoints:
- `POST /auth/login`: Authenticates user against `backend/db/profiles.json`.
- `GET /auth/profile`: Returns active user profile.
- `POST /stream/start`: Starts background `ffmpeg` process capturing from RTMP stream key (`rtmp://localhost:1935/live/<stream_key>`) to `frames/`.
- `POST /stream/stop`: Terminates active `ffmpeg` process.
- `GET /stream/status`: Returns current streaming status.
- `GET /infer`: Performs inference on latest frame in `backend/frames/` and returns detection results, health score, confidence, and base64 image frame.
- `GET /health`: Health status of the model and inference server.

---

## 3. Running the Frontend Dashboard

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start development server:
   ```bash
   npm run dev
   ```

4. Open the browser at `http://localhost:5173`.
   - Sign in using credentials from `backend/db/profiles.json`:
     - **Username**: `agroeyeadmin`
     - **Password**: `agroeye@123`
   - Enter your stream key (e.g. `agroeye`) and click **Start Stream**.
   - The stream key input locks and real-time frames with model inferences are displayed on the dashboard.

---

## 4. Live Video Streaming with RTMP & FFMPEG

To stream into the pipeline from OBS, phone camera (e.g., Larix Broadcaster), or drone feed:
- RTMP Server URL: `rtmp://localhost:1935/live`
- Stream Key: `agroeye` (or custom key entered in dashboard)
- Frames are captured at 0.5 FPS into `backend/frames/` and analyzed automatically.

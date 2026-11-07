# AgroEye

AI-powered UAV crop disease detection and real-time monitoring system.

## Tech Stack
- ReactJS
- FastAPI
- FFMPEG

## Local Development

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

- Backend API: `http://localhost:8000`

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

- Frontend App: `http://localhost:5173`

### 3. Login Credentials

### 4. Inference Pipeline

1. Log in on the frontend.
2. Enter your Stream Key in the dashboard.
3. Click **Start Stream** — this automatically triggers the backend `ffmpeg` image processing.
4. The dashboard locks the stream key and polls `GET /infer` to display real-time video frames and classification results (crop health score, disease name, confidence, and anomalies).
5. Click **Stop Stream** to terminate the ffmpeg process.

For full architecture and API details, see [DOCUMENTATION.md](DOCUMENTATION.md).

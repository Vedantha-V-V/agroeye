import { useState, useEffect, useRef } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import './Home.css'

export default function Home() {
  const [streamKey, setStreamKey] = useState('')
  const [isStreaming, setIsStreaming] = useState(false)
  const [displayName, setDisplayName] = useState('Admin')
  const [currentFrame, setCurrentFrame] = useState(null)
  const [latestResult, setLatestResult] = useState(null)
  const [statusMessage, setStatusMessage] = useState('')
  const pollTimerRef = useRef(null)
  const navigate = useNavigate()

  useEffect(() => {
    try {
      const stored = localStorage.getItem('agroeye_user')
      if (stored) {
        const parsed = JSON.parse(stored)
        if (parsed.display) setDisplayName(parsed.display)
      }
    } catch {
      // fallback
    }

    // Check backend stream status on mount
    fetch('http://localhost:8000/stream/status')
      .then(res => res.json())
      .then(data => {
        if (data.is_streaming) {
          setIsStreaming(true)
          if (data.stream_key) setStreamKey(data.stream_key)
        }
      })
      .catch(() => {})

    return () => {
      if (pollTimerRef.current) clearInterval(pollTimerRef.current)
    }
  }, [])

  // Poll /infer when streaming
  useEffect(() => {
    if (isStreaming) {
      const pollInfer = async () => {
        try {
          const res = await fetch('http://localhost:8000/infer')
          if (res.ok) {
            const data = await res.json()
            setLatestResult(data)
            setStatusMessage('')
            if (data.frame_base64) {
              setCurrentFrame(`data:image/jpeg;base64,${data.frame_base64}`)
            }

            // Save to past inferences cache
            try {
              const existing = JSON.parse(localStorage.getItem('agroeye_inferences') || '[]')
              const alreadyLogged = existing.some(item => item.timestamp === data.timestamp)
              if (!alreadyLogged) {
                const updated = [
                  {
                    id: Date.now(),
                    image: `data:image/jpeg;base64,${data.frame_base64}`,
                    cropHealthScore: data.crop_health_score,
                    diseaseDetected: data.disease_detected ? 'Yes' : 'No',
                    diseaseName: data.disease_name || 'None',
                    confidence: data.confidence,
                    anomalyFlags: (data.anomaly_flags || []).join(', ') || 'none',
                    timestamp: data.timestamp,
                    sourceFrame: data.source_frame,
                    modelConnected: data.model_connected ? 'Yes' : 'No'
                  },
                  ...existing
                ].slice(0, 30)
                localStorage.setItem('agroeye_inferences', JSON.stringify(updated))
              }
            } catch {
              // ignore storage errors
            }
          } else if (res.status === 404) {
            setStatusMessage('Stream active. Waiting for frames')
          }
        } catch {
          setStatusMessage('Waiting for server connection...')
        }
      }

      pollInfer()
      pollTimerRef.current = setInterval(pollInfer, 2000)
    } else {
      if (pollTimerRef.current) clearInterval(pollTimerRef.current)
    }

    return () => {
      if (pollTimerRef.current) clearInterval(pollTimerRef.current)
    }
  }, [isStreaming])

  const handleStartStream = async () => {
    if (!streamKey.trim()) {
      alert('Please enter a stream key before starting stream.')
      return
    }

    try {
      const res = await fetch('http://localhost:8000/stream/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ stream_key: streamKey.trim() })
      })
      if (res.ok) {
        setIsStreaming(true)
        setStatusMessage('Starting ffmpeg ingest pipeline...')
      } else {
        const err = await res.json()
        alert(err.detail || 'Failed to start stream')
      }
    } catch {
      alert('Could not connect to FastAPI server at http://localhost:8000')
    }
  }

  const handleStopStream = async () => {
    try {
      await fetch('http://localhost:8000/stream/stop', { method: 'POST' })
    } catch {
      // ignore
    }
    setIsStreaming(false)
    setStatusMessage('')
  }

  const handleLogout = () => {
    localStorage.removeItem('agroeye_user')
    navigate('/auth')
  }

  return (
    <div className="dashboard">
      {/* Left Column */}
      <div className="dash-left">
        {/* Stream Preview */}
        <div className="stream-preview">
          {currentFrame ? (
            <img
              src={currentFrame}
              alt="Live feed frame"
              style={{ width: '100%', height: '100%', objectFit: 'cover' }}
            />
          ) : (
            <div className="stream-placeholder">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#444" strokeWidth="1.5">
                <rect x="2" y="2" width="20" height="20" rx="2" />
                <circle cx="8" cy="8" r="2" />
                <path d="M21 15l-5-5L5 21" />
              </svg>
              <p>Image obtained from FastAPI server</p>
              <p className="stream-sub">
                {statusMessage || (isStreaming ? 'Streaming active. Ingesting frames...' : 'Enter stream key and click Start Stream')}
              </p>
            </div>
          )}
        </div>

        {/* Results Obtained */}
        <div className="results-card">
          <div className="card-header-row">
            <h3 className="card-title">Results Obtained</h3>
            <span className={`status-dot ${isStreaming ? 'online' : 'offline'}`}></span>
          </div>
          {latestResult ? (
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '4px 12px', marginTop: '4px' }}>
              <p className="results-muted">
                <strong>Score:</strong> <span style={{ color: 'var(--green-primary)' }}>{latestResult.crop_health_score}</span>
              </p>
              <p className="results-muted">
                <strong>Confidence:</strong> {latestResult.confidence}
              </p>
              <p className="results-muted">
                <strong>Disease:</strong> {latestResult.disease_name || 'None detected'}
              </p>
              <p className="results-muted">
                <strong>Anomaly:</strong> {(latestResult.anomaly_flags || []).join(', ') || 'None'}
              </p>
              <p className="results-muted" style={{ gridColumn: 'span 2', fontSize: '10px' }}>
                <strong>Frame:</strong> {latestResult.source_frame} | {latestResult.timestamp}
              </p>
            </div>
          ) : (
            <div className="results-placeholder">
              <p className="results-muted">
                {isStreaming
                  ? (statusMessage || 'Processing incoming frames with Vision model...')
                  : 'No results yet. Start a stream to get AI inference results.'}
              </p>
            </div>
          )}
        </div>

        {/* Stream Controls */}
        <div className="stream-controls">
          <button
            className={`stream-btn ${isStreaming ? 'streaming' : ''}`}
            onClick={isStreaming ? handleStopStream : handleStartStream}
          >
            {isStreaming ? '⏹ Stop Stream' : '▶ Start Stream'}
          </button>
          <div className="stream-key-input">
            <input
              type="text"
              placeholder="Enter Stream Key"
              value={streamKey}
              disabled={isStreaming}
              onChange={(e) => setStreamKey(e.target.value)}
            />
          </div>
        </div>
      </div>

      {/* Right Column */}
      <div className="dash-right">
        {/* Profile Banner */}
        <div className="profile-banner">
          <div className="profile-avatar-sm">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#22c55e" strokeWidth="2">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
              <circle cx="12" cy="7" r="4" />
            </svg>
          </div>
          <div style={{ flex: 1 }}>
            <p className="profile-label">Welcome back,</p>
            <h2 className="profile-name-text">{displayName}</h2>
          </div>
          <button
            onClick={handleLogout}
            title="Log out"
            style={{
              background: 'transparent',
              border: 'none',
              color: 'var(--text-muted)',
              cursor: 'pointer',
              padding: '6px',
              display: 'flex',
              alignItems: 'center'
            }}
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
              <polyline points="16 17 21 12 16 7" />
              <line x1="21" y1="12" x2="9" y2="12" />
            </svg>
          </button>
        </div>

        {/* Government Scheme */}
        <div className="info-card govt-card">
          <div className="card-header-row">
            <div className="card-icon-wrap">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#22c55e" strokeWidth="2">
                <rect x="2" y="3" width="20" height="14" rx="2" />
                <line x1="8" y1="21" x2="16" y2="21" />
                <line x1="12" y1="17" x2="12" y2="21" />
              </svg>
            </div>
            <h3 className="card-title">Government Schemes</h3>
          </div>
          <div className="scheme-list">
            <div className="scheme-item">
              <span className="scheme-name">PM-KISAN</span>
              <span className="scheme-tag active-tag">Active</span>
            </div>
            <div className="scheme-item">
              <span className="scheme-name">Fasal Bima Yojana</span>
              <span className="scheme-tag active-tag">Active</span>
            </div>
            <div className="scheme-item">
              <span className="scheme-name">Kisan Credit Card</span>
              <span className="scheme-tag pending-tag">Apply</span>
            </div>
            <div className="scheme-item">
              <span className="scheme-name">Soil Health Card</span>
              <span className="scheme-tag active-tag">Active</span>
            </div>
          </div>
        </div>

        {/* Weather Info */}
        <div className="info-card weather-card">
          <div className="card-header-row">
            <div className="card-icon-wrap">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#22c55e" strokeWidth="2">
                <path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z" />
              </svg>
            </div>
            <h3 className="card-title">Weather Info</h3>
          </div>
          <div className="weather-body">
            <div className="weather-main">
              <span className="weather-temp">28°C</span>
              <span className="weather-desc">Partly Cloudy</span>
            </div>
            <div className="weather-details">
              <div className="weather-detail-item">
                <span className="wd-label">Humidity</span>
                <span className="wd-value">72%</span>
              </div>
              <div className="weather-detail-item">
                <span className="wd-label">Wind</span>
                <span className="wd-value">12 km/h</span>
              </div>
              <div className="weather-detail-item">
                <span className="wd-label">Rain</span>
                <span className="wd-value">20%</span>
              </div>
            </div>
          </div>
        </div>

        {/* Past Inferences */}
        <Link to="/inferences" className="info-card past-inf-card">
          <div className="card-header-row">
            <div className="card-icon-wrap">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#22c55e" strokeWidth="2">
                <circle cx="12" cy="12" r="10" />
                <polyline points="12 6 12 12 16 14" />
              </svg>
            </div>
            <h3 className="card-title">Past Inferences</h3>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#666" strokeWidth="2" style={{ marginLeft: 'auto' }}>
              <polyline points="9 18 15 12 9 6" />
            </svg>
          </div>
          <p className="past-inf-sub">View previous AI scan results</p>
        </Link>
      </div>
    </div>
  )
}

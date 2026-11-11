import { useState, useEffect, useRef } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import './Home.css'

export default function Home() {
  const [streamKey, setStreamKey] = useState('')
  const [isStreaming, setIsStreaming] = useState(false)
  const [displayName, setDisplayName] = useState('Admin')
  const [city, setCity] = useState('Bengaluru')
  const [weather, setWeather] = useState({
    temp: 28,
    description: 'Partly Cloudy',
    humidity: 72,
    wind: 12,
    rain: 20,
    city: 'Bengaluru'
  })
  const [currentFrame, setCurrentFrame] = useState(null)
  const [latestResult, setLatestResult] = useState(null)
  const [statusMessage, setStatusMessage] = useState('')
  const [logs, setLogs] = useState([])
  const [activeTab, setActiveTab] = useState('results')
  const pollTimerRef = useRef(null)
  const logContainerRef = useRef(null)
  const navigate = useNavigate()

  useEffect(() => {
    try {
      const stored = localStorage.getItem('agroeye_user')
      if (stored) {
        const parsed = JSON.parse(stored)
        if (parsed.display) setDisplayName(parsed.display)
        if (parsed.location) setCity(parsed.location)
      }
    } catch {
      // fallback
    }

    // Fetch profile location from backend profiles.json
    fetch('http://localhost:8000/auth/profile')
      .then(res => res.json())
      .then(data => {
        if (data.display) setDisplayName(data.display)
        if (data.location) setCity(data.location)
      })
      .catch(() => {})

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

    // Initial logs fetch
    fetchLogs()

    return () => {
      if (pollTimerRef.current) clearInterval(pollTimerRef.current)
    }
  }, [])

  // Fetch OpenWeatherMap 4.0 OneCall data for the user's city
  useEffect(() => {
    if (!city) return

    const apiKey = import.meta.env.VITE_API_KEY || import.meta.env.VITE_OPENWEATHER_API_KEY || 'bc869ebd65ae7fb0f9f55e83ddb08e69'

    const KNOWN_COORDS = {
      bengaluru: { lat: 12.9716, lon: 77.5946, name: 'Bengaluru' },
      bangalore: { lat: 12.9716, lon: 77.5946, name: 'Bengaluru' },
      delhi: { lat: 28.6139, lon: 77.2090, name: 'Delhi' },
      mumbai: { lat: 19.0760, lon: 72.8777, name: 'Mumbai' },
      chennai: { lat: 13.0827, lon: 80.2707, name: 'Chennai' },
      kolkata: { lat: 22.5726, lon: 88.3639, name: 'Kolkata' },
      hyderabad: { lat: 17.3850, lon: 78.4867, name: 'Hyderabad' },
      pune: { lat: 18.5204, lon: 73.8567, name: 'Pune' },
    }

    const key = city.trim().toLowerCase()
    const fallback = KNOWN_COORDS[key] || { lat: 12.9716, lon: 77.5946, name: city }

    const fetchOneCall = (lat, lon, cityName) => {
      const url = `https://api.openweathermap.org/data/4.0/onecall/current?lat=${lat}&lon=${lon}&appid=${apiKey}`
      return fetch(url)
        .then(res => {
          if (!res.ok) throw new Error(`Weather 4.0 HTTP ${res.status}`)
          return res.json()
        })
        .then(resData => {
          const item = (resData.data && resData.data[0]) ? resData.data[0] : (resData.current || resData)
          const rawTemp = item.temp ?? 28
          const tempC = rawTemp > 150 ? Math.round(rawTemp - 273.15) : Math.round(rawTemp)
          const rawFeels = item.feels_like ?? rawTemp
          const feelsC = rawFeels > 150 ? Math.round(rawFeels - 273.15) : Math.round(rawFeels)
          const desc = item.weather?.[0]?.description
            ? item.weather[0].description.replace(/\b\w/g, l => l.toUpperCase())
            : (item.weather?.[0]?.main || 'Clear')
          const windKmH = Math.round((item.wind_speed ?? 3.5) * 3.6)
          const rainVal = item.rain
            ? (typeof item.rain === 'number' ? item.rain : (item.rain['1h'] || item.rain['3h'] || 0))
            : (item.clouds ?? 20)

          setWeather({
            temp: tempC,
            feelsLike: feelsC,
            description: desc,
            humidity: item.humidity ?? 58,
            wind: windKmH,
            rain: Math.round(rainVal),
            city: cityName
          })
        })
    }

    fetch(`https://api.openweathermap.org/geo/1.0/direct?q=${encodeURIComponent(city)}&limit=1&appid=${apiKey}`)
      .then(r => (r.ok ? r.json() : []))
      .then(geoList => {
        if (Array.isArray(geoList) && geoList.length > 0 && geoList[0].lat != null && geoList[0].lon != null) {
          return fetchOneCall(geoList[0].lat, geoList[0].lon, geoList[0].name || city)
        }
        return fetchOneCall(fallback.lat, fallback.lon, fallback.name)
      })
      .catch(() => {
        return fetchOneCall(fallback.lat, fallback.lon, fallback.name)
          .catch(() => {
            fetch(`https://api.openweathermap.org/data/2.5/weather?q=${encodeURIComponent(city)}&units=metric&appid=${apiKey}`)
              .then(r => r.json())
              .then(w => {
                if (w && w.main) {
                  setWeather({
                    temp: Math.round(w.main.temp),
                    description: w.weather?.[0]?.description ? w.weather[0].description.replace(/\b\w/g, l => l.toUpperCase()) : 'Partly Cloudy',
                    humidity: w.main.humidity,
                    wind: Math.round((w.wind?.speed || 3) * 3.6),
                    rain: w.clouds?.all ?? 20,
                    city: w.name || city
                  })
                }
              })
              .catch(() => {})
          })
      })
  }, [city])

  const fetchLogs = async () => {
    try {
      const res = await fetch('http://localhost:8000/stream/logs')
      if (res.ok) {
        const data = await res.json()
        if (data.logs) {
          setLogs(data.logs)
        }
      }
    } catch {
      // ignore
    }
  }

  // Auto-scroll logs
  useEffect(() => {
    if (logContainerRef.current) {
      logContainerRef.current.scrollTop = logContainerRef.current.scrollHeight
    }
  }, [logs])

  // Poll /infer and /stream/logs when streaming
  useEffect(() => {
    if (isStreaming) {
      const pollData = async () => {
        // Fetch logs
        await fetchLogs()

        // Fetch inference
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
              // ignore
            }
          } else if (res.status === 404) {
            setStatusMessage('Waiting for incoming RTMP frames from FFmpeg...')
          }
        } catch {
          setStatusMessage('Waiting for server connection...')
        }
      }

      pollData()
      pollTimerRef.current = setInterval(pollData, 1500)
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
      setStatusMessage('Starting Nginx RTMP server and FFmpeg...')
      const res = await fetch('http://localhost:8000/stream/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ stream_key: streamKey.trim() })
      })
      if (res.ok) {
        setIsStreaming(true)
        fetchLogs()
      } else {
        const err = await res.json()
        alert(err.detail || 'Failed to start stream')
        fetchLogs()
      }
    } catch {
      alert('Could not connect to FastAPI server at http://localhost:8000')
    }
  }

  const handleStopStream = async () => {
    try {
      setStatusMessage('Stopping FFmpeg, then stopping Nginx...')
      await fetch('http://localhost:8000/stream/stop', { method: 'POST' })
    } catch {
      // ignore
    }
    setIsStreaming(false)
    setStatusMessage('')
    setTimeout(fetchLogs, 500)
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

        {/* Results / Live Logs Card */}
        <div className="results-card">
          <div className="card-header-row">
            <div className="tab-buttons">
              <button
                className={`tab-btn ${activeTab === 'results' ? 'active' : ''}`}
                onClick={() => setActiveTab('results')}
              >
                Results Obtained
              </button>
              <button
                className={`tab-btn ${activeTab === 'logs' ? 'active' : ''}`}
                onClick={() => setActiveTab('logs')}
              >
                Pipeline Logs ({logs.length})
              </button>
            </div>
            <span className={`status-dot ${isStreaming ? 'online' : 'offline'}`}></span>
          </div>

          {activeTab === 'results' ? (
            latestResult ? (
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '4px 12px', marginTop: '4px' }}>
                <p className="results-muted">
                  <strong>Score:</strong> <span style={{ color: 'var(--green-primary)' }}>{latestResult.crop_health_score ?? 'N/A'}</span>
                </p>
                <p className="results-muted">
                  <strong>Confidence:</strong> {latestResult.confidence}
                </p>
                <p className="results-muted">
                  <strong>Disease:</strong> {latestResult.disease_name || 'None detected'}
                  {latestResult.saved_to_db && (
                    <span style={{ background: 'rgba(239, 68, 68, 0.2)', color: '#ef4444', padding: '1px 5px', borderRadius: '4px', fontSize: '9px', fontWeight: 600, marginLeft: '6px' }}>
                      Archived to DB
                    </span>
                  )}
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
                    : 'No results yet. Start a stream to begin Nginx RTMP and FFmpeg pipeline.'}
                </p>
              </div>
            )
          ) : (
            <div className="logs-terminal" ref={logContainerRef}>
              {logs.length === 0 ? (
                <p className="log-empty">No pipeline logs yet.</p>
              ) : (
                logs.map((log, index) => (
                  <div
                    key={index}
                    className={`log-line ${log.includes('ERROR') ? 'log-err' : log.includes('NGINX') ? 'log-nginx' : log.includes('FFMPEG') ? 'log-ffmpeg' : 'log-info'}`}
                  >
                    {log}
                  </div>
                ))
              )}
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
            <div className="card-header-left">
              <div className="card-icon-wrap">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#22c55e" strokeWidth="2">
                  <rect x="2" y="3" width="20" height="14" rx="2" />
                  <line x1="8" y1="21" x2="16" y2="21" />
                  <line x1="12" y1="17" x2="12" y2="21" />
                </svg>
              </div>
              <h3 className="card-title">Government Schemes</h3>
            </div>
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
            <div className="card-header-left">
              <div className="card-icon-wrap">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#22c55e" strokeWidth="2">
                  <path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z" />
                </svg>
              </div>
              <h3 className="card-title">Weather Info</h3>
            </div>
            <span className="weather-city-badge">{weather.city}</span>
          </div>
          <div className="weather-body">
            <div className="weather-main">
              <span className="weather-temp">{weather.temp}°C</span>
              <span className="weather-desc">{weather.description}</span>
            </div>
            <div className="weather-details">
              <div className="weather-detail-item">
                <span className="wd-label">Humidity</span>
                <span className="wd-value">{weather.humidity}%</span>
              </div>
              <div className="weather-detail-item">
                <span className="wd-label">Wind</span>
                <span className="wd-value">{weather.wind} km/h</span>
              </div>
              <div className="weather-detail-item">
                <span className="wd-label">Rain</span>
                <span className="wd-value">{weather.rain}%</span>
              </div>
            </div>
          </div>
        </div>

        {/* Past Inferences */}
        <Link to="/inferences" className="info-card past-inf-card">
          <div className="card-header-row">
            <div className="card-header-left">
              <div className="card-icon-wrap">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#22c55e" strokeWidth="2">
                  <circle cx="12" cy="12" r="10" />
                  <polyline points="12 6 12 12 16 14" />
                </svg>
              </div>
              <h3 className="card-title">Past Inferences</h3>
            </div>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#666" strokeWidth="2">
              <polyline points="9 18 15 12 9 6" />
            </svg>
          </div>
          <p className="past-inf-sub">Previous crop scan results</p>
        </Link>

        {/* AI Insights */}
        <Link to="/insights" className="info-card past-inf-card">
          <div className="card-header-row">
            <div className="card-header-left">
              <div className="card-icon-wrap">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#22c55e" strokeWidth="2">
                  <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
                </svg>
              </div>
              <h3 className="card-title">AI Insights</h3>
            </div>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#666" strokeWidth="2">
              <polyline points="9 18 15 12 9 6" />
            </svg>
          </div>
          <p className="past-inf-sub">Farm Focused AI Insights</p>
        </Link>
      </div>
    </div>
  )
}

import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import './Inferences.css'

export default function Inferences() {
  const [inferences, setInferences] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const loadInferences = async () => {
      let combined = []

      // 1. Fetch persistent disease records from backend db/inferences.json
      try {
        const res = await fetch('http://localhost:8000/inferences')
        if (res.ok) {
          const data = await res.json()
          if (Array.isArray(data.inferences)) {
            combined = data.inferences.map(item => ({
              id: item.id || item.timestamp,
              image: item.image_url ? `http://localhost:8000${item.image_url}` : null,
              cropHealthScore: item.crop_health_score,
              diseaseDetected: item.disease_detected ? 'Yes' : 'No',
              diseaseName: item.disease_name || 'None',
              confidence: item.confidence,
              anomalyFlags: Array.isArray(item.anomaly_flags) ? item.anomaly_flags.join(', ') : (item.anomaly_flags || 'none'),
              timestamp: item.timestamp,
              sourceFrame: item.source_frame || item.filename,
              savedToDb: item.saved_to_db || true
            }))
          }
        }
      } catch {
        // backend offline
      }

      // 2. Merge local browser session history (avoid duplicates)
      try {
        const local = JSON.parse(localStorage.getItem('agroeye_inferences') || '[]')
        local.forEach(loc => {
          const exists = combined.some(c => c.timestamp === loc.timestamp || (c.sourceFrame && c.sourceFrame === loc.sourceFrame))
          if (!exists) {
            combined.push(loc)
          }
        })
      } catch {
        // ignore
      }

      setInferences(combined)
      setLoading(false)
    }

    loadInferences()
  }, [])

  return (
    <div className="inferences-page">
      <header className="inf-header">
        <Link to="/" className="back-btn">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <polyline points="15 18 9 12 15 6" />
          </svg>
        </Link>
        <div className="inf-header-title">
          <span className="inf-sparkle">✦</span>
          <h1>Past Inferences</h1>
        </div>
        <div style={{ width: 22 }}></div>
      </header>

      {loading ? (
        <div className="inf-empty">
          <p className="inf-empty-sub">Loading stored references...</p>
        </div>
      ) : inferences.length === 0 ? (
        <div className="inf-empty">
          <svg width="56" height="56" viewBox="0 0 24 24" fill="none" stroke="#333" strokeWidth="1.5">
            <circle cx="12" cy="12" r="10" />
            <polyline points="12 6 12 12 16 14" />
          </svg>
          <p className="inf-empty-title">No inferences recorded yet</p>
          <p className="inf-empty-sub">
            Frames flagged with high confidence disease symptoms are automatically archived to <code>db/images</code> and linked here.
          </p>
        </div>
      ) : (
        <div className="inf-list-scroll">
          {inferences.map((inf) => (
            <div className="inf-record-card" key={inf.id}>
              {inf.image ? (
                <div className="inf-thumb-wrap">
                  <img src={inf.image} alt={inf.diseaseName || 'Crop frame'} />
                  {inf.savedToDb && <span className="db-badge">Archived</span>}
                </div>
              ) : (
                <div className="inf-thumb-placeholder">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#555" strokeWidth="1.5">
                    <rect x="3" y="3" width="18" height="18" rx="2" />
                    <circle cx="8.5" cy="8.5" r="1.5" />
                    <polyline points="21 15 16 10 5 21" />
                  </svg>
                </div>
              )}
              <div className="inf-record-details">
                <div className="inf-record-row-top">
                  <span className="inf-disease-name">{inf.diseaseName}</span>
                  <span className="inf-conf-tag">Conf: {(inf.confidence * 100).toFixed(1)}%</span>
                </div>
                <div className="inf-meta-grid">
                  <div>
                    <span className="meta-lbl">Health Score:</span>{' '}
                    <span className={inf.cropHealthScore < 0.5 ? 'score-danger' : 'score-good'}>
                      {inf.cropHealthScore}
                    </span>
                  </div>
                  <div>
                    <span className="meta-lbl">Disease Detected:</span> {inf.diseaseDetected}
                  </div>
                  <div className="meta-full">
                    <span className="meta-lbl">Anomalies:</span> {inf.anomalyFlags}
                  </div>
                  <div className="meta-full meta-timestamp">
                    <span>{inf.sourceFrame}</span> • <span>{inf.timestamp}</span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

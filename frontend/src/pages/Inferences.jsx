import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import './Inferences.css'

export default function Inferences() {
  const [inferences, setInferences] = useState([])

  useEffect(() => {
    try {
      const data = JSON.parse(localStorage.getItem('agroeye_inferences') || '[]')
      setInferences(data)
    } catch {
      setInferences([])
    }
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

      {inferences.length === 0 ? (
        <div className="inf-empty">
          <svg width="56" height="56" viewBox="0 0 24 24" fill="none" stroke="#333" strokeWidth="1.5">
            <circle cx="12" cy="12" r="10" />
            <polyline points="12 6 12 12 16 14" />
          </svg>
          <p className="inf-empty-title">No inferences yet</p>
          <p className="inf-empty-sub">Past AI scan results will appear here once you run the live stream pipeline.</p>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', overflowY: 'auto', flex: 1, paddingRight: '4px' }}>
          {inferences.map((inf) => (
            <div
              key={inf.id}
              style={{
                display: 'flex',
                gap: '12px',
                background: 'var(--bg-card)',
                border: '1px solid var(--border-color)',
                borderRadius: '10px',
                padding: '10px',
                alignItems: 'center'
              }}
            >
              {inf.image && (
                <img
                  src={inf.image}
                  alt="Past inference"
                  style={{ width: '64px', height: '64px', objectFit: 'cover', borderRadius: '6px' }}
                />
              )}
              <div style={{ flex: 1, minWidth: 0, fontSize: '11px', color: 'var(--text-secondary)', lineHeight: 1.5 }}>
                <p style={{ color: 'var(--text-primary)', fontWeight: 600, fontSize: '12px' }}>
                  Health Score: <span style={{ color: 'var(--green-primary)' }}>{inf.cropHealthScore}</span> | Confidence: {inf.confidence}
                </p>
                <p>Disease: {inf.diseaseName} (Detected: {inf.diseaseDetected})</p>
                <p>Anomaly: {inf.anomalyFlags}</p>
                <p style={{ fontSize: '10px', color: 'var(--text-muted)' }}>{inf.timestamp} | {inf.sourceFrame}</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

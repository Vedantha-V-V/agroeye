import { useState, useEffect, useRef } from 'react'
import { Link } from 'react-router-dom'
import './Insights.css'

const API = 'http://localhost:8000'

const SUGGESTIONS = [
  'What diseases are most common in my crops?',
  'How can I improve my soil health?',
  'What treatment should I apply for the detected disease?',
  'Give me a summary of recent detections',
  'What preventive measures can I take this season?',
]

function formatTime(isoStr) {
  if (!isoStr) return ''
  try {
    const d = new Date(isoStr)
    return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  } catch {
    return ''
  }
}

export default function Insights() {
  const [embedStatus, setEmbedStatus] = useState(null) // null | 'ok' | 'err' | 'loading'
  const [embedMsg, setEmbedMsg]       = useState('')
  const [messages, setMessages]       = useState([])
  const [query, setQuery]             = useState('')
  const [loading, setLoading]         = useState(false)
  const [openCtx, setOpenCtx]         = useState({})

  const chatEndRef = useRef(null)

  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: 'smooth' })
    }
  }, [messages, loading])

  const handleEmbed = async () => {
    setEmbedStatus('loading')
    setEmbedMsg('Embedding data into Qdrant...')
    try {
      const res = await fetch(`${API}/insights/embed`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.detail || 'Embed failed')
      const r = data.result || {}
      const pCount = r.profile?.embedded ?? 0
      const iCount = r.inferences?.embedded ?? 0
      setEmbedMsg(`✓ Embedded: ${pCount} profile + ${iCount} inferences`)
      setEmbedStatus('ok')
    } catch (e) {
      setEmbedMsg(e.message)
      setEmbedStatus('err')
    }
  }

  const sendQuery = async (q) => {
    const text = (q || query).trim()
    if (!text || loading) return
    setQuery('')
    setMessages(prev => [...prev, { role: 'user', text, ts: new Date().toISOString() }])
    setLoading(true)
    try {
      const res = await fetch(`${API}/insights/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: text }),
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.detail || 'Query failed')
      setMessages(prev => [
        ...prev,
        { role: 'ai', text: data.answer, ts: data.timestamp, context: data.context_used || [] },
      ])
    } catch (e) {
      setMessages(prev => [
        ...prev,
        { role: 'ai', text: `Error: ${e.message}`, ts: new Date().toISOString(), context: [] },
      ])
    } finally {
      setLoading(false)
    }
  }

  const toggleCtx = (i) => setOpenCtx(prev => ({ ...prev, [i]: !prev[i] }))

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendQuery()
    }
  }

  return (
    <div className="insights-page">
      {/* Header */}
      <header className="ins-header">
        <Link to="/" className="ins-back-btn">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <polyline points="15 18 9 12 15 6" />
          </svg>
        </Link>
        <div className="ins-header-title">
          <span className="ins-sparkle">✦</span>
          <h1>AI Insights</h1>
        </div>
        <div style={{ width: 22 }} />
      </header>

      {/* Embed */}
      <div className="ins-api-row">
        <button
          className="ins-embed-btn"
          onClick={handleEmbed}
          disabled={embedStatus === 'loading'}
        >
          {embedStatus === 'loading' ? 'Syncing...' : '⬆ Sync Data'}
        </button>
        {embedMsg && (
          <span className={`ins-embed-status ${embedStatus === 'ok' ? 'ok' : embedStatus === 'err' ? 'err' : ''}`}>
            {embedMsg}
          </span>
        )}
      </div>

      {/* Chat */}
      <div className="ins-chat-area">
        {messages.length === 0 && !loading ? (
          <div className="ins-empty">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
            </svg>
            <span>Ask anything about your farm, crops, or past disease detections</span>
          </div>
        ) : (
          messages.map((msg, i) => (
            <div key={i} className={`ins-msg ${msg.role}`}>
              <div className="ins-bubble">{msg.text}</div>
              <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                <span className="ins-msg-time">{formatTime(msg.ts)}</span>
                {msg.role === 'ai' && msg.context && msg.context.length > 0 && (
                  <button className="ins-ctx-toggle" onClick={() => toggleCtx(i)}>
                    {openCtx[i] ? 'hide context' : `${msg.context.length} sources`}
                  </button>
                )}
              </div>
              {msg.role === 'ai' && openCtx[i] && msg.context && (
                <div className="ins-ctx-panel">
                  {msg.context.map((h, j) => (
                    <div key={j} className="ins-ctx-hit">
                      <span className="ins-ctx-score">{(h.score * 100).toFixed(1)}%</span>
                      <span>[{h.payload?.type}] {h.payload?.text?.slice(0, 120)}...</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))
        )}

        {loading && (
          <div className="ins-loading">
            <span className="ins-dot" />
            <span className="ins-dot" />
            <span className="ins-dot" />
            <span>Generating insight...</span>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>

      {/* Suggestions */}
      {messages.length === 0 && (
        <div className="ins-suggestions">
          {SUGGESTIONS.map((s, i) => (
            <button key={i} className="ins-suggestion-chip" onClick={() => sendQuery(s)}>
              {s}
            </button>
          ))}
        </div>
      )}

      {/* Input */}
      <div className="ins-input-row">
        <textarea
          className="ins-query-input"
          rows={1}
          placeholder="Ask about your crops, diseases, or farm data..."
          value={query}
          onChange={e => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
        />
        <button
          className="ins-send-btn"
          onClick={() => sendQuery()}
          disabled={loading || !query.trim()}
        >
          Ask
        </button>
      </div>
    </div>
  )
}

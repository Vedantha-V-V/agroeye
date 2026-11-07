import { Routes, Route, Navigate } from 'react-router-dom'
import Home from './pages/Home.jsx'
import Inferences from './pages/Inferences.jsx'
import Auth from './pages/Auth.jsx'

function ProtectedRoute({ children }) {
  const user = localStorage.getItem('agroeye_user')
  if (!user) {
    return <Navigate to="/auth" replace />
  }
  return children
}

function App() {
  return (
    <Routes>
      <Route path="/auth" element={<Auth />} />
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <Home />
          </ProtectedRoute>
        }
      />
      <Route
        path="/inferences"
        element={
          <ProtectedRoute>
            <Inferences />
          </ProtectedRoute>
        }
      />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}

export default App

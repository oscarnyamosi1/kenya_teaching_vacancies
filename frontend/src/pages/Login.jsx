import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

const BRAND_IMG = 'https://storage.googleapis.com/banani-generated-images/generated-images/7e24eac0-f1c2-48ed-b5c4-9014633f40e9.jpg'
const AVATAR_IMG = 'https://storage.googleapis.com/banani-avatars/avatar%2Ffemale%2F25-35%2FAfrican%2F4'

export default function Login() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({ username: '', password: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      await login(form)
      navigate('/')
    } catch (err) {
      setError(err.response?.data?.error || 'Login failed. Please check your credentials.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="split-layout">
      <div className="brand-side">
        <img className="brand-image" src={BRAND_IMG} alt="Teachers" />
        <div className="brand-overlay" />
        <div className="brand-content">
          <div style={{ fontSize: 20, fontWeight: 600, marginBottom: 12, color: '#fff' }}>
            "This platform transformed how I found my teaching placement in Nairobi."
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            <img
              src={AVATAR_IMG}
              alt="Sarah"
              style={{ width: 40, height: 40, borderRadius: '50%', border: '2px solid white', objectFit: 'cover' }}
            />
            <div style={{ color: '#fff' }}>
              <div style={{ fontWeight: 600, fontSize: 14 }}>Sarah Omondi</div>
              <div style={{ fontSize: 12, opacity: 0.8 }}>English Teacher, Riara Group of Schools</div>
            </div>
          </div>
        </div>
      </div>

      <div className="form-side">
        <div className="auth-form-container">
          <div style={{ textAlign: 'center', marginBottom: 32 }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 8, marginBottom: 20 }}>
              <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
                <rect width="32" height="32" rx="8" fill="var(--primary)" opacity="0.2" />
                <path d="M8 22L16 10L24 22H8Z" fill="var(--primary)" />
              </svg>
              <span style={{ fontWeight: 700, fontSize: 16, color: 'var(--foreground)' }}>Kenya Teaching Vacancies</span>
            </div>
            <h1 style={{ margin: '0 0 8px', fontSize: 26, fontWeight: 700, color: 'var(--foreground)' }}>Welcome back</h1>
            <p style={{ margin: 0, color: 'var(--muted-foreground)', fontSize: 14 }}>
              Enter your details to access your account.
            </p>
          </div>

          <div className="social-grid">
            <button className="btn-social">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="#1877f2">
                <path d="M18 2h-3a5 5 0 00-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 011-1h3z" />
              </svg>
              Facebook
            </button>
            <button className="btn-social">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="#0a66c2">
                <path d="M16 8a6 6 0 016 6v7h-4v-7a2 2 0 00-2-2 2 2 0 00-2 2v7h-4v-7a6 6 0 016-6zM2 9h4v12H2z" />
                <circle cx="4" cy="4" r="2" />
              </svg>
              LinkedIn
            </button>
          </div>

          <div className="divider">Or continue with email</div>

          {error && <div className="error-msg">{error}</div>}

          <form onSubmit={handleSubmit}>
            <div className="input-group">
              <label className="input-label">Username or Email</label>
              <input
                className="input-field"
                placeholder="mwalimu@example.com"
                value={form.username}
                onChange={e => setForm({ ...form, username: e.target.value })}
                required
              />
            </div>
            <div className="input-group">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <label className="input-label">Password</label>
                <a href="#" className="link" style={{ fontSize: 12 }}>Forgot password?</a>
              </div>
              <input
                type="password"
                className="input-field"
                placeholder="••••••••"
                value={form.password}
                onChange={e => setForm({ ...form, password: e.target.value })}
                required
              />
            </div>
            <button type="submit" className="btn btn-primary" disabled={loading} style={{ width: '100%', justifyContent: 'center', padding: '12px', marginTop: 8 }}>
              {loading ? 'Signing in…' : 'Sign in'}
            </button>
          </form>

          <div style={{ marginTop: 24, textAlign: 'center', fontSize: 14, color: 'var(--muted-foreground)' }}>
            Don't have an account? <Link to="/register" className="link">Sign up</Link>
          </div>

          <div style={{ marginTop: 32, textAlign: 'center', fontSize: 12, color: 'var(--muted-foreground)' }}>
            <Link to="/privacy" style={{ color: 'var(--muted-foreground)', marginRight: 12 }}>Privacy</Link>
            <Link to="/terms" style={{ color: 'var(--muted-foreground)', marginRight: 12 }}>Terms</Link>
            <Link to="/pricing" style={{ color: 'var(--muted-foreground)', marginRight: 12 }}>Pricing</Link>
            <Link to="/contact" style={{ color: 'var(--muted-foreground)' }}>Contact</Link>
          </div>
        </div>
      </div>
    </div>
  )
}

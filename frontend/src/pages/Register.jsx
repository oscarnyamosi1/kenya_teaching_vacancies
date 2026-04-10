import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

const BRAND_IMG = 'https://storage.googleapis.com/banani-generated-images/generated-images/7e24eac0-f1c2-48ed-b5c4-9014633f40e9.jpg'

export default function Register() {
  const { register } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({ username: '', email: '', password: '', password2: '', role: 'teacher' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (form.password !== form.password2) {
      setError('Passwords do not match.')
      return
    }
    setLoading(true)
    setError('')
    try {
      await register(form)
      navigate('/')
    } catch (err) {
      const data = err.response?.data
      if (data) {
        const msg = Object.values(data).flat().join(' ')
        setError(msg)
      } else {
        setError('Registration failed. Please try again.')
      }
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
          <div style={{ fontSize: 20, fontWeight: 600, marginBottom: 8, color: '#fff' }}>
            Join thousands of teachers finding their dream school.
          </div>
          <div style={{ fontSize: 14, color: 'rgba(255,255,255,0.8)' }}>
            Connect with top schools across Kenya.
          </div>
        </div>
      </div>

      <div className="form-side">
        <div className="auth-form-container">
          <div style={{ textAlign: 'center', marginBottom: 28 }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 8, marginBottom: 16 }}>
              <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
                <rect width="32" height="32" rx="8" fill="var(--primary)" opacity="0.2" />
                <path d="M8 22L16 10L24 22H8Z" fill="var(--primary)" />
              </svg>
              <span style={{ fontWeight: 700, fontSize: 16, color: 'var(--foreground)' }}>Kenya Teaching Vacancies</span>
            </div>
            <h1 style={{ margin: '0 0 6px', fontSize: 24, fontWeight: 700, color: 'var(--foreground)' }}>Create your account</h1>
            <p style={{ margin: 0, color: 'var(--muted-foreground)', fontSize: 14 }}>Start your teaching journey today.</p>
          </div>

          <div style={{ display: 'flex', gap: 8, marginBottom: 20 }}>
            {['teacher', 'employer'].map(r => (
              <button
                key={r}
                type="button"
                className={`btn ${form.role === r ? 'btn-primary' : 'btn-outline'}`}
                style={{ flex: 1, justifyContent: 'center', textTransform: 'capitalize' }}
                onClick={() => setForm({ ...form, role: r })}
              >
                {r === 'teacher' ? '🧑‍🏫 Teacher' : '🏫 Employer'}
              </button>
            ))}
          </div>

          {error && <div className="error-msg">{error}</div>}

          <form onSubmit={handleSubmit}>
            <div className="input-group">
              <label className="input-label">Username</label>
              <input
                className="input-field"
                placeholder="mwalimu_omondi"
                value={form.username}
                onChange={e => setForm({ ...form, username: e.target.value })}
                required
              />
            </div>
            <div className="input-group">
              <label className="input-label">Email address</label>
              <input
                type="email"
                className="input-field"
                placeholder="mwalimu@example.com"
                value={form.email}
                onChange={e => setForm({ ...form, email: e.target.value })}
              />
            </div>
            <div className="input-group">
              <label className="input-label">Password</label>
              <input
                type="password"
                className="input-field"
                placeholder="At least 8 characters"
                value={form.password}
                onChange={e => setForm({ ...form, password: e.target.value })}
                required
              />
            </div>
            <div className="input-group">
              <label className="input-label">Confirm password</label>
              <input
                type="password"
                className="input-field"
                placeholder="••••••••"
                value={form.password2}
                onChange={e => setForm({ ...form, password2: e.target.value })}
                required
              />
            </div>
            <button type="submit" className="btn btn-primary" disabled={loading} style={{ width: '100%', justifyContent: 'center', padding: '12px', marginTop: 8 }}>
              {loading ? 'Creating account…' : 'Create Account'}
            </button>
          </form>

          <div style={{ marginTop: 20, textAlign: 'center', fontSize: 14, color: 'var(--muted-foreground)' }}>
            Already have an account? <Link to="/login" className="link">Sign in</Link>
          </div>
        </div>
      </div>
    </div>
  )
}

import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

export default function NavBar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = async () => {
    await logout()
    navigate('/login')
  }

  return (
    <nav className="top-nav">
      <Link to="/" className="logo-area">
        <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
          <rect width="32" height="32" rx="8" fill="var(--primary)" opacity="0.15" />
          <path d="M8 22L16 10L24 22H8Z" fill="var(--primary)" />
        </svg>
        <span>Kenya Teaching Vacancies</span>
      </Link>

      <div className="nav-links">
        <Link to="/" className="nav-link">Feed</Link>
        <Link to="/schools" className="nav-link">Schools</Link>
        <Link to="/jobs/saved" className="nav-link">Saved</Link>

        {user ? (
          <>
            <Link to="/profile" className="nav-link">Profile</Link>
            <button className="btn btn-outline" onClick={handleLogout} style={{ fontSize: 13 }}>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4M16 17l5-5-5-5M21 12H9" />
              </svg>
              {user.username}
            </button>
          </>
        ) : (
          <>
            <Link to="/login" className="btn btn-outline" style={{ fontSize: 13 }}>Log In</Link>
            <Link to="/register" className="btn btn-primary" style={{ fontSize: 13 }}>Sign Up</Link>
          </>
        )}
      </div>
    </nav>
  )
}

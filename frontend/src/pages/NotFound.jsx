import { useNavigate } from 'react-router-dom'
import Layout from '../components/Layout'

export default function NotFound() {
  const navigate = useNavigate()
  return (
    <Layout>
      <div className="empty-state" style={{ paddingTop: 100 }}>
        <div style={{ fontSize: 80, marginBottom: 16 }}>404</div>
        <p style={{ fontWeight: 700, fontSize: 20, marginBottom: 8 }}>Page not found</p>
        <p style={{ fontSize: 14, marginBottom: 24 }}>The page you're looking for doesn't exist.</p>
        <button className="btn btn-primary" onClick={() => navigate('/')}>Go Home</button>
      </div>
    </Layout>
  )
}

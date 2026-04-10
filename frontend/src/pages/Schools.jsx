import { useState, useEffect } from 'react'
import { schoolsApi } from '../api/client'
import Layout from '../components/Layout'

const FALLBACK_IMG = 'https://storage.googleapis.com/banani-avatars/avatar%2Fmale%2F35-50%2FAfrican%2F2'

function SchoolCard({ school }) {
  return (
    <div className="glass card" style={{ padding: 20, display: 'flex', alignItems: 'center', gap: 16 }}>
      <img
        src={school.logo || FALLBACK_IMG}
        alt={school.name}
        style={{ width: 56, height: 56, borderRadius: '50%', objectFit: 'cover', border: '2px solid var(--border)', flexShrink: 0 }}
        onError={e => { e.target.src = FALLBACK_IMG }}
      />
      <div style={{ flex: 1 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 4 }}>
          <h3 style={{ margin: 0, fontSize: 15, fontWeight: 700 }}>{school.name}</h3>
          {school.is_verified && (
            <svg width="16" height="16" viewBox="0 0 24 24" fill="var(--primary)">
              <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          )}
        </div>
        <p style={{ margin: 0, fontSize: 13, color: 'var(--muted-foreground)' }}>
          {school.location}
          {school.category?.title ? ` · ${school.category.title}` : ''}
        </p>
      </div>
      <button className="btn btn-outline" style={{ fontSize: 12 }}>Follow</button>
    </div>
  )
}

export default function Schools() {
  const [schools, setSchools] = useState([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')

  const fetchSchools = () => {
    setLoading(true)
    const params = search ? { search } : {}
    schoolsApi.list(params)
      .then(res => setSchools(res.data.results || res.data))
      .catch(() => {})
      .finally(() => setLoading(false))
  }

  useEffect(() => { fetchSchools() }, [])

  const handleSearch = (e) => {
    e.preventDefault()
    fetchSchools()
  }

  return (
    <Layout>
      <h2 className="section-title">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--primary)" strokeWidth="2" style={{ marginRight: 8, verticalAlign: 'middle' }}>
          <path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z" />
          <polyline points="9,22 9,12 15,12 15,22" />
        </svg>
        Schools in Kenya
      </h2>

      <form onSubmit={handleSearch} style={{ marginBottom: 20 }}>
        <div className="search-bar">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--muted-foreground)" strokeWidth="2">
            <circle cx="11" cy="11" r="8" /><line x1="21" y1="21" x2="16.65" y2="16.65" />
          </svg>
          <input
            placeholder="Search schools by name or location…"
            value={search}
            onChange={e => setSearch(e.target.value)}
          />
          <button type="submit" className="btn btn-primary" style={{ padding: '6px 16px' }}>Search</button>
        </div>
      </form>

      {loading ? (
        <div className="loading-center"><div className="spinner" /></div>
      ) : schools.length === 0 ? (
        <div className="empty-state">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
            <path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z" />
          </svg>
          <p style={{ fontWeight: 600 }}>No schools found</p>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
          {schools.map(school => (
            <SchoolCard key={school.id} school={school} />
          ))}
        </div>
      )}
    </Layout>
  )
}

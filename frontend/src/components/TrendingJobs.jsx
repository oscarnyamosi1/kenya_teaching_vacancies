import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { jobsApi } from '../api/client'

export default function TrendingJobs() {
  const [jobs, setJobs] = useState([])
  const navigate = useNavigate()

  useEffect(() => {
    jobsApi.trending()
      .then(res => setJobs(res.data.results || res.data))
      .catch(() => {})
  }, [])

  if (!jobs.length) return null

  return (
    <div className="glass card" style={{ marginBottom: 16 }}>
      <h4 className="section-title" style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--primary)" strokeWidth="2">
          <polyline points="23 6 13.5 15.5 8.5 10.5 1 18" />
          <polyline points="17 6 23 6 23 12" />
        </svg>
        Trending Jobs
      </h4>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
        {jobs.slice(0, 6).map((job, i) => (
          <button
            key={job.id}
            className="btn-ghost"
            onClick={() => navigate(`/jobs/${job.id}`)}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 10,
              padding: '8px 10px',
              borderRadius: 'var(--radius-md)',
              textAlign: 'left',
              width: '100%',
              background: 'transparent',
              border: 'none',
              cursor: 'pointer',
              color: 'var(--foreground)',
            }}
          >
            <span style={{
              minWidth: 24,
              height: 24,
              borderRadius: '50%',
              background: 'var(--glass-bg)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: 11,
              fontWeight: 700,
              color: i < 3 ? 'var(--primary)' : 'var(--muted-foreground)',
              flexShrink: 0,
            }}>
              {i + 1}
            </span>
            <div style={{ flex: 1, minWidth: 0 }}>
              <div style={{ fontSize: 13, fontWeight: 600, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                {job.job_title}
              </div>
              <div style={{ fontSize: 11, color: 'var(--muted-foreground)' }}>
                {job.county?.title || ''} · {job.total_applications} applicants
              </div>
            </div>
          </button>
        ))}
      </div>
    </div>
  )
}

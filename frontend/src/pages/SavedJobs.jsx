import { useState, useEffect } from 'react'
import { jobsApi } from '../api/client'
import { useAuth } from '../contexts/AuthContext'
import { useNavigate } from 'react-router-dom'
import Layout from '../components/Layout'
import JobCard from '../components/JobCard'

export default function SavedJobs() {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [jobs, setJobs] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!user) { navigate('/login'); return }
    jobsApi.saved()
      .then(res => setJobs(res.data.results || res.data))
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [user])

  return (
    <Layout>
      <h2 className="section-title" style={{ marginBottom: 20 }}>
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--primary)" strokeWidth="2" style={{ marginRight: 8, verticalAlign: 'middle' }}>
          <path d="M19 21l-7-5-7 5V5a2 2 0 012-2h10a2 2 0 012 2z" />
        </svg>
        Saved Jobs
      </h2>

      {loading ? (
        <div className="loading-center"><div className="spinner" /></div>
      ) : jobs.length === 0 ? (
        <div className="empty-state">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
            <path d="M19 21l-7-5-7 5V5a2 2 0 012-2h10a2 2 0 012 2z" />
          </svg>
          <p style={{ fontWeight: 600, fontSize: 16, marginBottom: 8 }}>No saved jobs yet</p>
          <p style={{ fontSize: 14, marginBottom: 20 }}>Browse teaching vacancies and save the ones you like.</p>
          <button className="btn btn-primary" onClick={() => navigate('/')}>Browse Jobs</button>
        </div>
      ) : (
        <>
          <p style={{ fontSize: 13, color: 'var(--muted-foreground)', marginBottom: 16 }}>
            {jobs.length} saved {jobs.length === 1 ? 'job' : 'jobs'}
          </p>
          {jobs.map(job => (
            <JobCard key={job.id} job={job} initialSaved={true} />
          ))}
        </>
      )}
    </Layout>
  )
}

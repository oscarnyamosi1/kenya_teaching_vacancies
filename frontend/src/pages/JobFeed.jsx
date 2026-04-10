import { useState, useEffect, useCallback } from 'react'
import { jobsApi } from '../api/client'
import { useAuth } from '../contexts/AuthContext'
import Layout from '../components/Layout'
import JobCard from '../components/JobCard'
import { useNavigate } from 'react-router-dom'

const CURRICULUM_TYPES = ['IGCSE', '8-4-4', 'CBC/JSS', 'ECDE', 'High School']

export default function JobFeed() {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [jobs, setJobs] = useState([])
  const [savedIds, setSavedIds] = useState([])
  const [loading, setLoading] = useState(true)
  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const [search, setSearch] = useState('')
  const [filters, setFilters] = useState({ county: '', curriculum: '', tsc: false, urgent: false })

  const fetchJobs = useCallback(async () => {
    setLoading(true)
    try {
      const params = { page }
      if (search) params.search = search
      if (filters.county) params.county = filters.county
      if (filters.curriculum) params.curriculum = filters.curriculum
      if (filters.tsc) params.tsc = true
      if (filters.urgent) params.urgent = true
      const res = await jobsApi.list(params)
      const data = res.data
      setJobs(data.results || data)
      if (data.count) setTotalPages(Math.ceil(data.count / 20))
    } catch (err) {
      setJobs([])
    } finally {
      setLoading(false)
    }
  }, [page, search, filters])

  useEffect(() => { fetchJobs() }, [fetchJobs])

  useEffect(() => {
    if (user) {
      jobsApi.savedIds()
        .then(res => setSavedIds(res.data.saved_job_ids || []))
        .catch(() => {})
    }
  }, [user])

  const handleSearch = (e) => {
    e.preventDefault()
    setPage(1)
    fetchJobs()
  }

  return (
    <Layout>
      {/* Search Bar */}
      <form onSubmit={handleSearch}>
        <div className="search-bar">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--muted-foreground)" strokeWidth="2">
            <circle cx="11" cy="11" r="8" /><line x1="21" y1="21" x2="16.65" y2="16.65" />
          </svg>
          <input
            placeholder="Search teaching jobs, subjects, locations…"
            value={search}
            onChange={e => setSearch(e.target.value)}
          />
          <button type="submit" className="btn btn-primary" style={{ padding: '6px 16px' }}>Search</button>
        </div>
      </form>

      {/* Filters */}
      <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', marginBottom: 20 }}>
        <select
          className="input-field"
          style={{ flex: '1', minWidth: 140, padding: '8px 12px', fontSize: 13 }}
          value={filters.curriculum}
          onChange={e => { setFilters({ ...filters, curriculum: e.target.value }); setPage(1) }}
        >
          <option value="">All Curricula</option>
          {CURRICULUM_TYPES.map(c => <option key={c} value={c}>{c}</option>)}
        </select>

        <input
          className="input-field"
          style={{ flex: '1', minWidth: 140, padding: '8px 12px', fontSize: 13 }}
          placeholder="Filter by county…"
          value={filters.county}
          onChange={e => { setFilters({ ...filters, county: e.target.value }); setPage(1) }}
        />

        <button
          className={`btn ${filters.tsc ? 'btn-primary' : 'btn-outline'}`}
          onClick={() => { setFilters({ ...filters, tsc: !filters.tsc }); setPage(1) }}
        >
          TSC Required
        </button>
        <button
          className={`btn ${filters.urgent ? 'btn-primary' : 'btn-outline'}`}
          onClick={() => { setFilters({ ...filters, urgent: !filters.urgent }); setPage(1) }}
        >
          🔥 Urgent
        </button>
      </div>

      {/* Results */}
      {loading ? (
        <div className="loading-center"><div className="spinner" /></div>
      ) : jobs.length === 0 ? (
        <div className="empty-state">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
            <circle cx="11" cy="11" r="8" /><line x1="21" y1="21" x2="16.65" y2="16.65" />
          </svg>
          <p style={{ fontWeight: 600, fontSize: 16, marginBottom: 8 }}>No jobs found</p>
          <p style={{ fontSize: 14 }}>Try adjusting your filters or search terms.</p>
        </div>
      ) : (
        <>
          <p style={{ fontSize: 13, color: 'var(--muted-foreground)', marginBottom: 16 }}>
            Showing teaching vacancies in Kenya
          </p>
          {jobs.map(job => (
            <JobCard
              key={job.id}
              job={job}
              initialSaved={savedIds.includes(job.id)}
            />
          ))}

          {totalPages > 1 && (
            <div className="pagination">
              <button
                className="btn btn-outline"
                onClick={() => setPage(p => Math.max(1, p - 1))}
                disabled={page === 1}
              >
                ← Previous
              </button>
              <span style={{ color: 'var(--muted-foreground)', fontSize: 13 }}>
                Page {page} of {totalPages}
              </span>
              <button
                className="btn btn-outline"
                onClick={() => setPage(p => Math.min(totalPages, p + 1))}
                disabled={page === totalPages}
              >
                Next →
              </button>
            </div>
          )}
        </>
      )}
    </Layout>
  )
}

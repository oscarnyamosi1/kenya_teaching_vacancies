import { useState } from 'react'
import { jobsApi } from '../api/client'
import { useAuth } from '../contexts/AuthContext'
import { useNavigate } from 'react-router-dom'

const FALLBACK_IMG = 'https://storage.googleapis.com/banani-avatars/avatar%2Fmale%2F35-50%2FAfrican%2F2'

export default function JobCard({ job, initialSaved = false, onApplied }) {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [saved, setSaved] = useState(initialSaved)
  const [applying, setApplying] = useState(false)
  const [applied, setApplied] = useState(false)
  const [error, setError] = useState('')

  const handleSave = async (e) => {
    e.stopPropagation()
    if (!user) { navigate('/login'); return }
    try {
      const res = await jobsApi.save(job.id)
      setSaved(res.data.saved)
    } catch {}
  }

  const handleApply = async (e) => {
    e.stopPropagation()
    if (!user) { navigate('/login'); return }
    setApplying(true)
    setError('')
    try {
      await jobsApi.apply(job.id)
      setApplied(true)
      if (onApplied) onApplied(job.id)
    } catch (err) {
      setError(err.response?.data?.error || 'Could not apply.')
    } finally {
      setApplying(false)
    }
  }

  const schoolName = job.employer?.school?.name || job.employer?.username || 'Unknown School'
  const schoolType = job.employer?.school?.category?.title || ''
  const countyName = job.county?.title || job.location || ''
  const logoUrl = FALLBACK_IMG

  return (
    <article className="job-card glass" onClick={() => navigate(`/jobs/${job.id}`)}>
      {job.is_promoted && <div className="promoted-badge">Promoted</div>}

      <div className="job-card-header">
        <img src={logoUrl} alt={schoolName} className="school-avatar" />
        <div className="school-info" style={{ flex: 1 }}>
          <h3>{schoolName}</h3>
          <p>{countyName}{schoolType ? ` · ${schoolType}` : ''}</p>
        </div>
        <span style={{ fontSize: 12, color: 'var(--muted-foreground)', whiteSpace: 'nowrap' }}>
          {job.days_posted} ago
        </span>
      </div>

      <h2 className="job-title">{job.job_title}</h2>

      <div className="job-tags">
        {job.employment_type?.title && <span className="tag">{job.employment_type.title}</span>}
        {job.carriculum_type && <span className="tag">{job.carriculum_type}</span>}
        {job.tsc_required && <span className="tag tag-warning">TSC Required</span>}
        {job.is_urgent && <span className="tag tag-warning">Urgent</span>}
        {job.convertSalaryMin && job.convertSalaryMax && (
          <span className="tag tag-success">KSh {job.convertSalaryMin}k – {job.convertSalaryMax}k</span>
        )}
        {job.total_applications > 500 && (
          <span className="tag">Competitive 500+ applicants</span>
        )}
        {job.subjects_required?.map(s => (
          <span key={s.id} className="tag tag-primary">{s.title}</span>
        ))}
      </div>

      {job.job_description && (
        <p className="job-description">
          {job.job_description.length > 140
            ? job.job_description.slice(0, 140) + '…'
            : job.job_description}
        </p>
      )}

      {error && <div className="error-msg" style={{ fontSize: 12, padding: '6px 10px', marginBottom: 10 }}>{error}</div>}

      <div className="job-actions" onClick={e => e.stopPropagation()}>
        <div className="action-group">
          <button className={`btn ${saved ? 'btn-primary' : ''}`} onClick={handleSave}>
            <svg width="15" height="15" viewBox="0 0 24 24" fill={saved ? 'currentColor' : 'none'} stroke="currentColor" strokeWidth="2">
              <path d="M19 21l-7-5-7 5V5a2 2 0 012-2h10a2 2 0 012 2z" />
            </svg>
            {saved ? 'Saved' : 'Save'}
          </button>
          <button className="btn btn-ghost" onClick={(e) => e.stopPropagation()}>
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="18" cy="5" r="3" /><circle cx="6" cy="12" r="3" /><circle cx="18" cy="19" r="3" />
              <line x1="8.59" y1="13.51" x2="15.42" y2="17.49" /><line x1="15.41" y1="6.51" x2="8.59" y2="10.49" />
            </svg>
            Share
          </button>
        </div>
        {applied ? (
          <span className="tag tag-success">Applied ✓</span>
        ) : (
          <button
            className="btn btn-primary"
            onClick={handleApply}
            disabled={applying}
          >
            {applying ? 'Applying…' : 'Apply Now'}
          </button>
        )}
      </div>
    </article>
  )
}

import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { jobsApi } from '../api/client'
import { useAuth } from '../contexts/AuthContext'
import Layout from '../components/Layout'

const FALLBACK_IMG = 'https://storage.googleapis.com/banani-avatars/avatar%2Fmale%2F35-50%2FAfrican%2F2'

export default function JobDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { user } = useAuth()
  const [job, setJob] = useState(null)
  const [loading, setLoading] = useState(true)
  const [saved, setSaved] = useState(false)
  const [applied, setApplied] = useState(false)
  const [applying, setApplying] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    jobsApi.detail(id)
      .then(res => {
        setJob(res.data)
        if (user) {
          jobsApi.savedIds()
            .then(r => setSaved((r.data.saved_job_ids || []).includes(res.data.id)))
            .catch(() => {})
        }
      })
      .catch(() => navigate('/'))
      .finally(() => setLoading(false))
  }, [id, user])

  const handleSave = async () => {
    if (!user) { navigate('/login'); return }
    try {
      const res = await jobsApi.save(job.id)
      setSaved(res.data.saved)
    } catch {}
  }

  const handleApply = async () => {
    if (!user) { navigate('/login'); return }
    setApplying(true)
    setError('')
    try {
      await jobsApi.apply(job.id)
      setApplied(true)
    } catch (err) {
      setError(err.response?.data?.error || 'Could not apply.')
    } finally {
      setApplying(false)
    }
  }

  if (loading) return (
    <Layout>
      <div className="loading-center"><div className="spinner" /></div>
    </Layout>
  )

  if (!job) return null

  const schoolName = job.employer?.school?.name || job.employer?.username || 'Unknown School'
  const countyName = job.county?.title || ''

  return (
    <Layout>
      <button onClick={() => navigate(-1)} className="btn btn-ghost" style={{ marginBottom: 16 }}>
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <line x1="19" y1="12" x2="5" y2="12" /><polyline points="12,19 5,12 12,5" />
        </svg>
        Back
      </button>

      <div className="glass card" style={{ padding: 28, marginBottom: 20 }}>
        {job.is_promoted && <div className="promoted-badge">Promoted</div>}

        <div style={{ display: 'flex', alignItems: 'flex-start', gap: 16, marginBottom: 20 }}>
          <img src={FALLBACK_IMG} alt={schoolName} className="school-avatar" style={{ width: 64, height: 64 }} />
          <div style={{ flex: 1 }}>
            <h1 style={{ margin: '0 0 4px', fontSize: 24, fontWeight: 700, color: 'var(--foreground)' }}>{job.job_title}</h1>
            <div style={{ color: 'var(--muted-foreground)', fontSize: 14 }}>
              {schoolName} · {countyName}
            </div>
            <div style={{ fontSize: 12, color: 'var(--muted-foreground)', marginTop: 2 }}>
              Posted {job.days_posted} ago · {job.days_to_deadline} left to apply
            </div>
          </div>
        </div>

        <div className="job-tags" style={{ marginBottom: 20 }}>
          {job.employment_type?.title && <span className="tag">{job.employment_type.title}</span>}
          {job.carriculum_type && <span className="tag">{job.carriculum_type}</span>}
          {job.tsc_required && <span className="tag tag-warning">TSC Required</span>}
          {job.is_urgent && <span className="tag tag-warning">🔥 Urgent</span>}
          {job.is_featured && <span className="tag tag-primary">Featured</span>}
          {job.convertSalaryMin && job.convertSalaryMax && (
            <span className="tag tag-success">KSh {job.convertSalaryMin}k – {job.convertSalaryMax}k /month</span>
          )}
        </div>

        {error && <div className="error-msg">{error}</div>}

        <div style={{ display: 'flex', gap: 12, marginBottom: 28 }}>
          {applied ? (
            <span className="tag tag-success" style={{ padding: '10px 20px', fontSize: 14 }}>✓ Applied Successfully</span>
          ) : (
            <button
              className="btn btn-primary"
              style={{ padding: '10px 24px', fontSize: 15 }}
              onClick={handleApply}
              disabled={applying}
            >
              {applying ? 'Applying…' : 'Apply Now'}
            </button>
          )}
          <button className={`btn ${saved ? 'btn-primary' : 'btn-outline'}`} onClick={handleSave}>
            <svg width="15" height="15" viewBox="0 0 24 24" fill={saved ? 'currentColor' : 'none'} stroke="currentColor" strokeWidth="2">
              <path d="M19 21l-7-5-7 5V5a2 2 0 012-2h10a2 2 0 012 2z" />
            </svg>
            {saved ? 'Saved' : 'Save Job'}
          </button>
        </div>

        <hr style={{ border: 'none', borderTop: '1px solid var(--border)', margin: '20px 0' }} />

        <h3 style={{ fontSize: 16, fontWeight: 700, marginBottom: 12 }}>Job Description</h3>
        <p style={{ color: 'var(--muted-foreground)', lineHeight: 1.7, fontSize: 14, whiteSpace: 'pre-wrap' }}>
          {job.job_description || 'No description provided.'}
        </p>

        {job.subjects_required?.length > 0 && (
          <div style={{ marginTop: 20 }}>
            <h3 style={{ fontSize: 16, fontWeight: 700, marginBottom: 12 }}>Subjects Required</h3>
            <div className="job-tags">
              {job.subjects_required.map(s => (
                <span key={s.id} className="tag tag-primary">{s.title}</span>
              ))}
            </div>
          </div>
        )}

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16, marginTop: 24 }}>
          {[
            { label: 'Grade Level', value: job.grade_level },
            { label: 'Min Experience', value: job.min_experience ? `${job.min_experience} years` : 'Not specified' },
            { label: 'Location', value: `${countyName}${job.constituency ? `, ${job.constituency}` : ''}` },
            { label: 'Deadline', value: job.application_deadline ? new Date(job.application_deadline).toLocaleDateString() : 'N/A' },
            { label: 'Total Applicants', value: job.total_applications },
            { label: 'Specialization', value: job.specialization_required?.title || 'Any' },
          ].map(({ label, value }) => value && (
            <div key={label} style={{ padding: 14, borderRadius: 'var(--radius-md)', background: 'var(--glass-bg)', border: '1px solid var(--glass-border)' }}>
              <div style={{ fontSize: 11, color: 'var(--muted-foreground)', textTransform: 'uppercase', letterSpacing: 0.5, marginBottom: 4 }}>{label}</div>
              <div style={{ fontSize: 14, fontWeight: 600 }}>{value}</div>
            </div>
          ))}
        </div>
      </div>
    </Layout>
  )
}

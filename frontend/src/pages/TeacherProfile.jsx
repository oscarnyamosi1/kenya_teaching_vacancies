import { useState, useEffect } from 'react'
import { teacherApi } from '../api/client'
import { useAuth } from '../contexts/AuthContext'
import { useNavigate } from 'react-router-dom'
import Layout from '../components/Layout'

function ProfileField({ label, value, children }) {
  return (
    <div style={{ marginBottom: 16 }}>
      <div style={{ fontSize: 12, color: 'var(--muted-foreground)', textTransform: 'uppercase', letterSpacing: 0.5, marginBottom: 4 }}>{label}</div>
      <div style={{ fontSize: 14, fontWeight: 500 }}>{children || value || '—'}</div>
    </div>
  )
}

export default function TeacherProfile() {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [profile, setProfile] = useState(null)
  const [loading, setLoading] = useState(true)
  const [editing, setEditing] = useState(false)
  const [form, setForm] = useState({})
  const [saving, setSaving] = useState(false)
  const [success, setSuccess] = useState('')
  const [error, setError] = useState('')

  useEffect(() => {
    if (!user) { navigate('/login'); return }
    teacherApi.profile()
      .then(res => {
        setProfile(res.data)
        setForm(res.data)
      })
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [user])

  const handleSave = async (e) => {
    e.preventDefault()
    setSaving(true)
    setError('')
    setSuccess('')
    try {
      const res = await teacherApi.update({
        phone: form.phone,
        email: form.email,
        classification: form.classification,
        gender: form.gender,
        highest_education: form.highest_education,
        institution_attended: form.institution_attended,
        years_experience: form.years_experience,
        grade_levels: form.grade_levels,
        tsc_registered: form.tsc_registered,
        tsc_number: form.tsc_number,
        willing_to_relocate: form.willing_to_relocate,
        expected_salary_min: form.expected_salary_min,
        expected_salary_max: form.expected_salary_max,
        profile_visibility: form.profile_visibility,
      })
      setProfile(res.data)
      setEditing(false)
      setSuccess('Profile updated successfully!')
    } catch (err) {
      setError('Failed to save profile. Please try again.')
    } finally {
      setSaving(false)
    }
  }

  if (loading) return (
    <Layout>
      <div className="loading-center"><div className="spinner" /></div>
    </Layout>
  )

  if (!profile) return (
    <Layout>
      <div className="empty-state">
        <p style={{ fontWeight: 600 }}>No teacher profile found</p>
        <p style={{ fontSize: 14 }}>Your account doesn't have a teacher profile yet.</p>
      </div>
    </Layout>
  )

  const username = profile.user?.username || user?.username || ''
  const fullName = [profile.user?.first_name, profile.user?.last_name].filter(Boolean).join(' ') || username

  return (
    <Layout>
      <div className="glass card" style={{ padding: 28, marginBottom: 20 }}>
        <div className="profile-header">
          <div style={{
            width: 72, height: 72, borderRadius: '50%',
            background: 'linear-gradient(135deg, var(--primary), #7c3aed)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontSize: 28, fontWeight: 700, color: 'white', flexShrink: 0,
          }}>
            {username.charAt(0).toUpperCase()}
          </div>
          <div style={{ flex: 1 }}>
            <h2 style={{ margin: '0 0 4px', fontSize: 22, fontWeight: 700 }}>{fullName}</h2>
            <p style={{ margin: 0, color: 'var(--muted-foreground)', fontSize: 14 }}>@{username}</p>
            <div style={{ display: 'flex', gap: 8, marginTop: 8 }}>
              {profile.tsc_registered && <span className="tag tag-success">TSC Registered</span>}
              {profile.verified_badge && <span className="tag tag-primary">✓ Verified</span>}
              {profile.profile_visibility ? <span className="tag">Visible</span> : <span className="tag">Hidden</span>}
            </div>
          </div>
          <button
            className={`btn ${editing ? 'btn-outline' : 'btn-primary'}`}
            onClick={() => { setEditing(!editing); setSuccess(''); setError('') }}
          >
            {editing ? 'Cancel' : 'Edit Profile'}
          </button>
        </div>

        {success && <div className="success-msg">{success}</div>}
        {error && <div className="error-msg">{error}</div>}

        {editing ? (
          <form onSubmit={handleSave}>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
              {[
                { label: 'Phone', key: 'phone', type: 'tel' },
                { label: 'Email', key: 'email', type: 'email' },
                { label: 'Institution Attended', key: 'institution_attended' },
                { label: 'Years of Experience', key: 'years_experience', type: 'number' },
                { label: 'Grade Levels (e.g. F1-F4)', key: 'grade_levels' },
                { label: 'TSC Number', key: 'tsc_number' },
                { label: 'Expected Salary Min (KES)', key: 'expected_salary_min', type: 'number' },
                { label: 'Expected Salary Max (KES)', key: 'expected_salary_max', type: 'number' },
              ].map(({ label, key, type = 'text' }) => (
                <div key={key} className="input-group" style={{ marginBottom: 0 }}>
                  <label className="input-label">{label}</label>
                  <input
                    type={type}
                    className="input-field"
                    value={form[key] || ''}
                    onChange={e => setForm({ ...form, [key]: e.target.value })}
                  />
                </div>
              ))}
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 16, marginTop: 16 }}>
              <div className="input-group" style={{ marginBottom: 0 }}>
                <label className="input-label">Classification</label>
                <select className="input-field" value={form.classification || ''} onChange={e => setForm({ ...form, classification: e.target.value })}>
                  {['Humanities', 'Sciences', 'Arts', 'Math'].map(c => <option key={c}>{c}</option>)}
                </select>
              </div>
              <div className="input-group" style={{ marginBottom: 0 }}>
                <label className="input-label">Gender</label>
                <select className="input-field" value={form.gender || ''} onChange={e => setForm({ ...form, gender: e.target.value })}>
                  <option value="">Select…</option>
                  {['Male', 'Female', 'Rather not say'].map(g => <option key={g}>{g}</option>)}
                </select>
              </div>
              <div className="input-group" style={{ marginBottom: 0 }}>
                <label className="input-label">Highest Education</label>
                <select className="input-field" value={form.highest_education || ''} onChange={e => setForm({ ...form, highest_education: e.target.value })}>
                  {['Degree', 'Diploma', 'Doctorate', 'Masters'].map(e => <option key={e}>{e}</option>)}
                </select>
              </div>
            </div>

            <div style={{ display: 'flex', gap: 16, marginTop: 16 }}>
              <label style={{ display: 'flex', alignItems: 'center', gap: 8, cursor: 'pointer', fontSize: 14 }}>
                <input type="checkbox" checked={!!form.tsc_registered} onChange={e => setForm({ ...form, tsc_registered: e.target.checked })} />
                TSC Registered
              </label>
              <label style={{ display: 'flex', alignItems: 'center', gap: 8, cursor: 'pointer', fontSize: 14 }}>
                <input type="checkbox" checked={!!form.willing_to_relocate} onChange={e => setForm({ ...form, willing_to_relocate: e.target.checked })} />
                Willing to Relocate
              </label>
              <label style={{ display: 'flex', alignItems: 'center', gap: 8, cursor: 'pointer', fontSize: 14 }}>
                <input type="checkbox" checked={!!form.profile_visibility} onChange={e => setForm({ ...form, profile_visibility: e.target.checked })} />
                Profile Visible
              </label>
            </div>

            <div style={{ marginTop: 24, display: 'flex', gap: 12 }}>
              <button type="submit" className="btn btn-primary" disabled={saving}>
                {saving ? 'Saving…' : 'Save Changes'}
              </button>
              <button type="button" className="btn btn-outline" onClick={() => { setEditing(false); setForm(profile) }}>
                Cancel
              </button>
            </div>
          </form>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 0 }}>
            <div style={{ padding: '0 24px 0 0', borderRight: '1px solid var(--border)' }}>
              <h4 style={{ color: 'var(--primary)', fontSize: 13, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, marginBottom: 16 }}>Personal Info</h4>
              <ProfileField label="Phone" value={profile.phone} />
              <ProfileField label="Email" value={profile.email} />
              <ProfileField label="Gender" value={profile.gender} />
              <ProfileField label="Date of Birth" value={profile.date_of_birth} />
              <ProfileField label="TSC Number" value={profile.tsc_number} />
            </div>
            <div style={{ padding: '0 0 0 24px' }}>
              <h4 style={{ color: 'var(--primary)', fontSize: 13, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, marginBottom: 16 }}>Professional</h4>
              <ProfileField label="Classification" value={profile.classification} />
              <ProfileField label="Highest Education" value={profile.highest_education} />
              <ProfileField label="Institution Attended" value={profile.institution_attended} />
              <ProfileField label="Years of Experience" value={profile.years_experience ? `${profile.years_experience} years` : null} />
              <ProfileField label="Grade Levels" value={profile.grade_levels} />
              <ProfileField label="Expected Salary">
                {profile.expected_salary_min && profile.expected_salary_max
                  ? `KSh ${(profile.expected_salary_min / 1000).toFixed(0)}k – ${(profile.expected_salary_max / 1000).toFixed(0)}k`
                  : '—'}
              </ProfileField>
              <ProfileField label="Willing to Relocate" value={profile.willing_to_relocate ? 'Yes' : 'No'} />
            </div>
          </div>
        )}
      </div>

      {!editing && profile.subjects_taught?.length > 0 && (
        <div className="glass card" style={{ padding: 20, marginBottom: 16 }}>
          <h4 className="section-title">Subjects Taught</h4>
          <div className="job-tags">
            {profile.subjects_taught.map(s => (
              <span key={s.id} className="tag tag-primary">{s.title}</span>
            ))}
          </div>
        </div>
      )}

      {!editing && profile.preferred_locations?.length > 0 && (
        <div className="glass card" style={{ padding: 20 }}>
          <h4 className="section-title">Preferred Locations</h4>
          <div className="job-tags">
            {profile.preferred_locations.map(c => (
              <span key={c.id} className="tag">{c.name}</span>
            ))}
          </div>
        </div>
      )}
    </Layout>
  )
}

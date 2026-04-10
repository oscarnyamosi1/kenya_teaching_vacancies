import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  withCredentials: true,
  headers: { 'Content-Type': 'application/json' },
})

// Attach CSRF token to mutating requests
api.interceptors.request.use(async (config) => {
  if (['post', 'put', 'patch', 'delete'].includes(config.method)) {
    let csrfToken = getCookie('csrftoken')
    if (!csrfToken) {
      try {
        const res = await axios.get('/api/csrf/', { withCredentials: true })
        csrfToken = res.data.csrfToken
      } catch (e) {}
    }
    if (csrfToken) {
      config.headers['X-CSRFToken'] = csrfToken
    }
  }
  return config
})

function getCookie(name) {
  const value = `; ${document.cookie}`
  const parts = value.split(`; ${name}=`)
  if (parts.length === 2) return parts.pop().split(';').shift()
  return null
}

// Auth
export const authApi = {
  login: (data) => api.post('/auth/login/', data),
  logout: () => api.post('/auth/logout/'),
  register: (data) => api.post('/auth/register/', data),
  me: () => api.get('/auth/me/'),
}

// Jobs
export const jobsApi = {
  list: (params) => api.get('/jobs/', { params }),
  detail: (id) => api.get(`/jobs/${id}/`),
  trending: () => api.get('/jobs/trending/'),
  saved: () => api.get('/jobs/saved/'),
  savedIds: () => api.get('/jobs/saved-ids/'),
  save: (id) => api.post(`/jobs/${id}/save/`),
  apply: (id) => api.post(`/jobs/${id}/apply/`),
}

// Applications
export const applicationsApi = {
  list: () => api.get('/applications/'),
  withdraw: (jobId) => api.delete(`/applications/${jobId}/withdraw/`),
}

// Teacher
export const teacherApi = {
  profile: () => api.get('/teacher/profile/'),
  update: (data) => api.patch('/teacher/profile/', data),
}

// Schools
export const schoolsApi = {
  list: (params) => api.get('/schools/', { params }),
}

// Metadata
export const metaApi = {
  get: () => api.get('/metadata/'),
}

export default api

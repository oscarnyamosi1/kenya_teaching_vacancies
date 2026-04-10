import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import Login from './pages/Login'
import Register from './pages/Register'
import JobFeed from './pages/JobFeed'
import JobDetail from './pages/JobDetail'
import SavedJobs from './pages/SavedJobs'
import MyApplications from './pages/MyApplications'
import TeacherProfile from './pages/TeacherProfile'
import Schools from './pages/Schools'
import NotFound from './pages/NotFound'

function PrivateRoute({ children }) {
  const { user, loading } = useAuth()
  if (loading) return <div style={{ display: 'flex', justifyContent: 'center', paddingTop: 100 }}><div className="spinner" /></div>
  return user ? children : <Navigate to="/login" replace />
}

function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<JobFeed />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/jobs/:id" element={<JobDetail />} />
      <Route path="/jobs/saved" element={<SavedJobs />} />
      <Route path="/schools" element={<Schools />} />
      <Route path="/applications" element={<PrivateRoute><MyApplications /></PrivateRoute>} />
      <Route path="/profile" element={<PrivateRoute><TeacherProfile /></PrivateRoute>} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </BrowserRouter>
  )
}

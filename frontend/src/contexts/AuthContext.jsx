import { createContext, useContext, useState, useEffect } from 'react'
import { authApi } from '../api/client'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [teacher, setTeacher] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    authApi.me()
      .then((res) => {
        setUser(res.data.user)
        setTeacher(res.data.teacher)
      })
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  const login = async (credentials) => {
    const res = await authApi.login(credentials)
    setUser(res.data.user)
    setTeacher(res.data.teacher)
    return res.data
  }

  const logout = async () => {
    await authApi.logout()
    setUser(null)
    setTeacher(null)
  }

  const register = async (data) => {
    const res = await authApi.register(data)
    setUser(res.data.user)
    return res.data
  }

  return (
    <AuthContext.Provider value={{ user, teacher, loading, login, logout, register }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}

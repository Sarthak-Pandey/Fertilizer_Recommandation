import { createContext, useContext, useState, useEffect } from 'react'
import type { ReactNode } from 'react'
import { api } from '../services/api'
import type { UserProfile, UserLoginPayload, UserRegisterPayload } from '../services/api'

interface AuthContextType {
  user: UserProfile | null
  token: string | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (data: UserLoginPayload) => Promise<void>
  register: (data: UserRegisterPayload) => Promise<void>
  logout: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<UserProfile | null>(() => {
    const savedUser = localStorage.getItem('auth_user')
    return savedUser ? JSON.parse(savedUser) : null
  })
  const [token, setToken] = useState<string | null>(() => localStorage.getItem('auth_token'))
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const initAuth = async () => {
      const storedToken = localStorage.getItem('auth_token')
      if (storedToken) {
        try {
          const profile = await api.getMe()
          setUser(profile)
          localStorage.setItem('auth_user', JSON.stringify(profile))
        } catch {
          // Token is expired or invalid
          localStorage.removeItem('auth_token')
          localStorage.removeItem('auth_user')
          setToken(null)
          setUser(null)
        }
      }
      setIsLoading(false)
    }

    initAuth()
  }, [])

  const login = async (data: UserLoginPayload) => {
    const res = await api.login(data)
    setToken(res.access_token)
    setUser(res.user)
    localStorage.setItem('auth_token', res.access_token)
    localStorage.setItem('auth_user', JSON.stringify(res.user))
  }

  const register = async (data: UserRegisterPayload) => {
    const res = await api.register(data)
    setToken(res.access_token)
    setUser(res.user)
    localStorage.setItem('auth_token', res.access_token)
    localStorage.setItem('auth_user', JSON.stringify(res.user))
  }

  const logout = async () => {
    try {
      await api.logout()
    } catch {
      // Ignore network errors during logout
    } finally {
      localStorage.removeItem('auth_token')
      localStorage.removeItem('auth_user')
      setToken(null)
      setUser(null)
    }
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isAuthenticated: !!user && !!token,
        isLoading,
        login,
        register,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

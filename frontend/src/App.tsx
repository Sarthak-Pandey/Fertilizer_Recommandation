import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import Navbar from './components/Navbar'
import MobileNav from './components/MobileNav'
import OverviewPage from './pages/OverviewPage'
import PredictionHistoryPage from './pages/PredictionHistoryPage'
import ModelAuditPage from './pages/ModelAuditPage'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Navbar />
        <Routes>
          <Route path="/" element={<OverviewPage />} />
          <Route path="/overview" element={<OverviewPage />} />
          <Route path="/history" element={<PredictionHistoryPage />} />
          <Route path="/audit" element={<ModelAuditPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="*" element={<Navigate to="/overview" replace />} />
        </Routes>
        <MobileNav />
      </AuthProvider>
    </BrowserRouter>
  )
}

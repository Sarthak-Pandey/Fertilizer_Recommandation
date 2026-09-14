import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import MobileNav from './components/MobileNav'
import OverviewPage from './pages/OverviewPage'
import PredictionHistoryPage from './pages/PredictionHistoryPage'
import ModelAuditPage from './pages/ModelAuditPage'

export default function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<OverviewPage />} />
        <Route path="/history" element={<PredictionHistoryPage />} />
        <Route path="/audit" element={<ModelAuditPage />} />
      </Routes>
      <MobileNav />
    </BrowserRouter>
  )
}

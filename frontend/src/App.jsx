import { useState, useEffect } from 'react'
import { Shield, Zap, RotateCcw, CreditCard, BarChart3, Activity } from 'lucide-react'
import Dashboard from './components/Dashboard.jsx'
import FraudDetector from './components/FraudDetector.jsx'
import ReturnScorer from './components/ReturnScorer.jsx'
import ChargebackResponder from './components/ChargebackResponder.jsx'
import MetricsPanel from './components/MetricsPanel.jsx'

const TABS = [
  { id: 'dashboard',   label: 'Dashboard',   icon: Activity },
  { id: 'fraud',       label: 'Fraud Detector', icon: Zap },
  { id: 'return',      label: 'Return Scorer',  icon: RotateCcw },
  { id: 'chargeback',  label: 'Chargeback AI',  icon: CreditCard },
  { id: 'metrics',     label: 'ML Metrics',     icon: BarChart3 },
]

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard')

  return (
    <div className="min-h-screen flex flex-col">
      {/* ── Header ─────────────────────────────────────────────── */}
      <header className="border-b border-slate-800 bg-slate-950/80 backdrop-blur sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-blue-600 flex items-center justify-center">
              <Shield size={20} className="text-white" />
            </div>
            <div>
              <span className="text-lg font-bold text-white tracking-tight">RazorShield</span>
              <span className="ml-2 text-xs text-slate-500 font-medium">AI Risk Manager</span>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            <span className="text-xs text-slate-400">Live</span>
          </div>
        </div>
        {/* Tabs */}
        <div className="max-w-7xl mx-auto px-6 flex gap-1 pb-0">
          {TABS.map(({ id, label, icon: Icon }) => (
            <button
              key={id}
              onClick={() => setActiveTab(id)}
              className={`flex items-center gap-2 px-4 py-2.5 text-sm font-medium rounded-t-lg transition-all ${
                activeTab === id ? 'tab-active' : 'tab-inactive'
              }`}
            >
              <Icon size={15} />
              {label}
            </button>
          ))}
        </div>
      </header>

      {/* ── Main ────────────────────────────────────────────────── */}
      <main className="max-w-7xl mx-auto px-6 py-8 w-full flex-1">
        {activeTab === 'dashboard'  && <Dashboard onNavigate={setActiveTab} />}
        {activeTab === 'fraud'      && <FraudDetector />}
        {activeTab === 'return'     && <ReturnScorer />}
        {activeTab === 'chargeback' && <ChargebackResponder />}
        {activeTab === 'metrics'    && <MetricsPanel />}
      </main>

      {/* ── Footer ──────────────────────────────────────────────── */}
      <footer className="border-t border-slate-800 text-center py-4 text-xs text-slate-600">
        RazorShield v1.0 · Built for Razorpay AI Risk Manager Track · Defense-only · 2025
      </footer>
    </div>
  )
}

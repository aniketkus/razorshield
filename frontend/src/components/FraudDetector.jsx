import { useState } from 'react'
import axios from 'axios'
import { Zap, AlertTriangle, CheckCircle, Loader2, RefreshCw } from 'lucide-react'

const RISK_CONFIG = {
  LOW:      { bg: 'bg-emerald-500/10', border: 'border-emerald-500/30', text: 'text-emerald-400', icon: CheckCircle },
  MEDIUM:   { bg: 'bg-amber-500/10',   border: 'border-amber-500/30',   text: 'text-amber-400',   icon: AlertTriangle },
  HIGH:     { bg: 'bg-orange-500/10',  border: 'border-orange-500/30',  text: 'text-orange-400',  icon: AlertTriangle },
  CRITICAL: { bg: 'bg-red-500/10',     border: 'border-red-500/30',     text: 'text-red-400',     icon: AlertTriangle },
}

const HIGH_RISK_PRESET = {
  txn_id: 'pay_DEMO001', customer_id: 'cust_000001', merchant_id: 'merch_0001',
  category: 'electronics', amount: 75000, payment_method: 'card', state: 'MH',
  device_type: 'mobile', browser: 'unknown', device_fp: 'abc123xyz',
  hour: 2, day_of_week: 5, txn_velocity_24h: 15, amount_velocity_24h: 200000,
  device_fp_count: 25,
}

const LOW_RISK_PRESET = {
  txn_id: 'pay_DEMO002', customer_id: 'cust_000099', merchant_id: 'merch_0010',
  category: 'groceries', amount: 450, payment_method: 'upi', state: 'KA',
  device_type: 'mobile', browser: 'chrome', device_fp: 'def456uvw',
  hour: 10, day_of_week: 1, txn_velocity_24h: 1, amount_velocity_24h: 450,
  device_fp_count: 1,
}

function ScoreGauge({ score }) {
  const r = 60, circ = 2 * Math.PI * r
  const offset = circ * (1 - score)
  const color = score < 0.2 ? '#10b981' : score < 0.45 ? '#f59e0b' : score < 0.7 ? '#f97316' : '#ef4444'
  return (
    <div className="flex flex-col items-center">
      <svg width="160" height="160" className="-rotate-90">
        <circle cx="80" cy="80" r={r} fill="none" stroke="#1e293b" strokeWidth="12" />
        <circle cx="80" cy="80" r={r} fill="none" stroke={color} strokeWidth="12"
          strokeDasharray={circ} strokeDashoffset={offset}
          strokeLinecap="round" className="score-ring" />
      </svg>
      <div className="-mt-24 flex flex-col items-center">
        <span className="text-4xl font-bold" style={{ color }}>{(score * 100).toFixed(1)}</span>
        <span className="text-xs text-slate-500 mt-1">Fraud Score</span>
      </div>
    </div>
  )
}

export default function FraudDetector() {
  const [form, setForm] = useState(LOW_RISK_PRESET)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const set = (k, v) => setForm(f => ({ ...f, [k]: v }))

  const submit = async () => {
    setLoading(true); setError(null); setResult(null)
    try {
      const { data } = await axios.post('/api/v1/fraud/score', form)
      setResult(data)
    } catch (e) {
      setError(e.response?.data?.detail || 'API error — is the backend running?')
    } finally {
      setLoading(false)
    }
  }

  const cfg = result ? RISK_CONFIG[result.risk_level] || RISK_CONFIG.LOW : null

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-blue-500/10 flex items-center justify-center">
          <Zap size={20} className="text-blue-400" />
        </div>
        <div>
          <h1 className="text-xl font-bold text-white">Fraud Spike Detector</h1>
          <p className="text-sm text-slate-400">Real-time ML scoring per transaction · Random Forest + SMOTE</p>
        </div>
        <div className="ml-auto flex gap-2">
          <button onClick={() => setForm(HIGH_RISK_PRESET)} className="text-xs px-3 py-1.5 bg-red-500/10 text-red-400 border border-red-500/30 rounded-lg hover:bg-red-500/20 transition-all">
            High-Risk Preset
          </button>
          <button onClick={() => setForm(LOW_RISK_PRESET)} className="text-xs px-3 py-1.5 bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 rounded-lg hover:bg-emerald-500/20 transition-all">
            Low-Risk Preset
          </button>
        </div>
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        {/* Input Form */}
        <div className="card space-y-4">
          <h2 className="font-semibold text-white">Transaction Details</h2>
          <div className="grid grid-cols-2 gap-3">
            {[
              ['txn_id',       'Transaction ID',    'text'],
              ['customer_id',  'Customer ID',       'text'],
              ['amount',       'Amount (₹)',         'number'],
              ['category',     'Category',          'text'],
            ].map(([k, label, type]) => (
              <div key={k}>
                <label className="text-xs text-slate-400 mb-1 block">{label}</label>
                <input type={type} value={form[k]} onChange={e => set(k, type === 'number' ? +e.target.value : e.target.value)}
                  className="input-field" />
              </div>
            ))}
          </div>
          <div className="grid grid-cols-2 gap-3">
            {[
              ['payment_method', 'Payment Method', ['upi','card','netbanking','wallet','emi']],
              ['device_type',    'Device Type',    ['mobile','desktop','tablet']],
              ['state',          'State',          ['MH','DL','KA','TN','WB','UP','GJ']],
              ['browser',        'Browser',        ['chrome','firefox','safari','edge','unknown']],
            ].map(([k, label, opts]) => (
              <div key={k}>
                <label className="text-xs text-slate-400 mb-1 block">{label}</label>
                <select value={form[k]} onChange={e => set(k, e.target.value)} className="input-field">
                  {opts.map(o => <option key={o} value={o}>{o}</option>)}
                </select>
              </div>
            ))}
          </div>
          <div className="grid grid-cols-3 gap-3">
            {[
              ['hour',                'Hour (0-23)',     'number'],
              ['txn_velocity_24h',    'Txn Velocity 24h','number'],
              ['device_fp_count',     'Device FP Count', 'number'],
            ].map(([k, label, type]) => (
              <div key={k}>
                <label className="text-xs text-slate-400 mb-1 block">{label}</label>
                <input type={type} value={form[k]} onChange={e => set(k, +e.target.value)} className="input-field" />
              </div>
            ))}
          </div>
          <button onClick={submit} disabled={loading} className="btn-primary w-full flex items-center justify-center gap-2">
            {loading ? <><Loader2 size={16} className="animate-spin" /> Scoring…</> : <><Zap size={16} /> Score Transaction</>}
          </button>
          {error && <div className="text-red-400 text-sm bg-red-500/10 rounded-xl p-3 border border-red-500/20">{error}</div>}
        </div>

        {/* Result */}
        <div className="card">
          <h2 className="font-semibold text-white mb-4">Risk Assessment</h2>
          {!result && !loading && (
            <div className="flex flex-col items-center justify-center h-64 text-slate-600 text-sm">
              <Zap size={40} className="mb-3 opacity-30" />
              Submit a transaction to see the fraud score
            </div>
          )}
          {loading && (
            <div className="flex flex-col items-center justify-center h-64 text-slate-400 gap-3">
              <Loader2 size={32} className="animate-spin text-blue-400" />
              <span className="text-sm">Running ML inference…</span>
            </div>
          )}
          {result && cfg && (
            <div className="space-y-4">
              <div className={`rounded-2xl border p-4 ${cfg.bg} ${cfg.border}`}>
                <div className="flex items-start justify-between">
                  <div>
                    <div className={`text-sm font-semibold ${cfg.text} flex items-center gap-1.5`}>
                      <cfg.icon size={15} /> {result.risk_level} RISK
                    </div>
                    <div className="text-2xl font-bold text-white mt-1">{result.txn_id}</div>
                    <div className="text-sm text-slate-400 mt-0.5">
                      Threshold: {(result.threshold_used * 100).toFixed(0)}% · Flagged: {result.is_fraud ? '✅ YES' : '❌ NO'}
                    </div>
                  </div>
                  <ScoreGauge score={result.fraud_score} />
                </div>
              </div>
              <div>
                <h3 className="text-sm font-semibold text-slate-300 mb-2">Risk Factors</h3>
                <div className="space-y-1.5">
                  {result.explanation.map((e, i) => (
                    <div key={i} className="flex items-start gap-2 text-sm text-slate-400">
                      <span className={`mt-0.5 ${cfg.text}`}>▸</span> {e}
                    </div>
                  ))}
                </div>
              </div>
              <div className="flex gap-3 text-xs text-slate-500 border-t border-slate-800 pt-3">
                <span>Score: <span className="text-white font-semibold">{result.fraud_score}</span></span>
                <span>·</span>
                <span>Threshold: <span className="text-white font-semibold">{result.threshold_used}</span></span>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

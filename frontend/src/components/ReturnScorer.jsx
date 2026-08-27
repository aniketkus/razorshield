import { useState } from 'react'
import axios from 'axios'
import { RotateCcw, Loader2, AlertTriangle, CheckCircle, Package } from 'lucide-react'

const HIGH_RETURN_PRESET = {
  order_id: 'ord_DEMO001', customer_id: 'cust_000002',
  category: 'fashion', amount: 4500, payment_method: 'upi', state: 'DL',
  device_type: 'mobile', browser: 'chrome', hour: 23, day_of_week: 6,
  txn_velocity_24h: 3, amount_velocity_24h: 15000, device_fp_count: 1,
  customer_return_rate: 0.45,
}

const LOW_RETURN_PRESET = {
  order_id: 'ord_DEMO002', customer_id: 'cust_000010',
  category: 'groceries', amount: 650, payment_method: 'emi', state: 'KA',
  device_type: 'desktop', browser: 'firefox', hour: 11, day_of_week: 2,
  txn_velocity_24h: 1, amount_velocity_24h: 650, device_fp_count: 1,
  customer_return_rate: 0.05,
}

function ProbBar({ prob }) {
  const color = prob < 0.3 ? '#10b981' : prob < 0.6 ? '#f59e0b' : '#ef4444'
  return (
    <div>
      <div className="flex justify-between text-xs text-slate-400 mb-1">
        <span>Return Probability</span>
        <span className="font-semibold" style={{ color }}>{(prob * 100).toFixed(1)}%</span>
      </div>
      <div className="h-3 bg-slate-800 rounded-full overflow-hidden">
        <div className="h-full rounded-full transition-all duration-1000"
          style={{ width: `${prob * 100}%`, background: color }} />
      </div>
    </div>
  )
}

export default function ReturnScorer() {
  const [form, setForm] = useState(LOW_RETURN_PRESET)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const set = (k, v) => setForm(f => ({ ...f, [k]: v }))

  const submit = async () => {
    setLoading(true); setError(null); setResult(null)
    try {
      const { data } = await axios.post('/api/v1/return/score', form)
      setResult(data)
    } catch (e) {
      setError(e.response?.data?.detail || 'API error — is the backend running?')
    } finally {
      setLoading(false)
    }
  }

  const riskColor = {
    LOW: 'text-emerald-400', MEDIUM: 'text-amber-400', HIGH: 'text-red-400'
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-amber-500/10 flex items-center justify-center">
          <RotateCcw size={20} className="text-amber-400" />
        </div>
        <div>
          <h1 className="text-xl font-bold text-white">Return Risk Scorer</h1>
          <p className="text-sm text-slate-400">Pre-fulfillment return probability · Gradient Boosting</p>
        </div>
        <div className="ml-auto flex gap-2">
          <button onClick={() => setForm(HIGH_RETURN_PRESET)} className="text-xs px-3 py-1.5 bg-red-500/10 text-red-400 border border-red-500/30 rounded-lg hover:bg-red-500/20 transition-all">
            High-Risk Preset
          </button>
          <button onClick={() => setForm(LOW_RETURN_PRESET)} className="text-xs px-3 py-1.5 bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 rounded-lg hover:bg-emerald-500/20 transition-all">
            Low-Risk Preset
          </button>
        </div>
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        <div className="card space-y-4">
          <h2 className="font-semibold text-white">Order Details</h2>
          <div className="grid grid-cols-2 gap-3">
            {[
              ['order_id',    'Order ID',   'text'],
              ['customer_id', 'Customer ID','text'],
              ['amount',      'Amount (₹)', 'number'],
            ].map(([k, label, type]) => (
              <div key={k}>
                <label className="text-xs text-slate-400 mb-1 block">{label}</label>
                <input type={type} value={form[k]} onChange={e => set(k, type === 'number' ? +e.target.value : e.target.value)} className="input-field" />
              </div>
            ))}
            <div>
              <label className="text-xs text-slate-400 mb-1 block">Customer Return Rate (%)</label>
              <input type="number" min="0" max="1" step="0.01" value={form.customer_return_rate}
                onChange={e => set('customer_return_rate', +e.target.value)} className="input-field" />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-3">
            {[
              ['category',       'Category',       ['electronics','fashion','groceries','travel','food','health','jewelry','gaming','books','home']],
              ['payment_method', 'Payment Method', ['upi','card','netbanking','wallet','emi']],
              ['device_type',    'Device',         ['mobile','desktop','tablet']],
              ['state',          'State',          ['MH','DL','KA','TN','WB','UP','GJ']],
            ].map(([k, label, opts]) => (
              <div key={k}>
                <label className="text-xs text-slate-400 mb-1 block">{label}</label>
                <select value={form[k]} onChange={e => set(k, e.target.value)} className="input-field">
                  {opts.map(o => <option key={o} value={o}>{o}</option>)}
                </select>
              </div>
            ))}
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-xs text-slate-400 mb-1 block">Hour (0-23)</label>
              <input type="number" min="0" max="23" value={form.hour} onChange={e => set('hour', +e.target.value)} className="input-field" />
            </div>
            <div>
              <label className="text-xs text-slate-400 mb-1 block">Day of Week (0=Mon)</label>
              <input type="number" min="0" max="6" value={form.day_of_week} onChange={e => set('day_of_week', +e.target.value)} className="input-field" />
            </div>
          </div>
          <button onClick={submit} disabled={loading} className="btn-primary w-full flex items-center justify-center gap-2" style={{ background: '#d97706', '--tw-ring-color': '#d97706' }}
            onMouseEnter={e => e.currentTarget.style.background = '#b45309'}
            onMouseLeave={e => e.currentTarget.style.background = '#d97706'}>
            {loading ? <><Loader2 size={16} className="animate-spin" /> Scoring…</> : <><RotateCcw size={16} /> Score Return Risk</>}
          </button>
          {error && <div className="text-red-400 text-sm bg-red-500/10 rounded-xl p-3 border border-red-500/20">{error}</div>}
        </div>

        <div className="card space-y-5">
          <h2 className="font-semibold text-white">Return Risk Assessment</h2>
          {!result && !loading && (
            <div className="flex flex-col items-center justify-center h-64 text-slate-600 text-sm">
              <Package size={40} className="mb-3 opacity-30" />
              Submit an order to see return probability
            </div>
          )}
          {loading && (
            <div className="flex flex-col items-center justify-center h-64 gap-3">
              <Loader2 size={32} className="animate-spin text-amber-400" />
              <span className="text-sm text-slate-400">Running ML inference…</span>
            </div>
          )}
          {result && (
            <>
              <ProbBar prob={result.return_probability} />

              <div className="flex items-center justify-between">
                <span className="text-sm text-slate-400">Risk Level</span>
                <span className={`font-bold text-lg ${riskColor[result.return_risk] || 'text-white'}`}>
                  {result.return_risk}
                </span>
              </div>

              <div className="bg-slate-800/60 rounded-xl p-4 border border-slate-700">
                <div className="text-xs text-slate-500 mb-1">Recommended Action</div>
                <div className="text-sm font-medium text-white">{result.suggested_action}</div>
              </div>

              <div className="bg-red-500/10 rounded-xl p-4 border border-red-500/20">
                <div className="text-xs text-slate-500 mb-1">Estimated Revenue At Risk</div>
                <div className="text-2xl font-bold text-red-400">
                  ₹{result.estimated_loss_inr.toLocaleString()}
                </div>
              </div>

              <div>
                <div className="text-sm font-semibold text-slate-300 mb-2">Risk Factors</div>
                <div className="space-y-1.5">
                  {result.risk_factors.map((f, i) => (
                    <div key={i} className="flex items-start gap-2 text-sm text-slate-400">
                      <span className="text-amber-400 mt-0.5">▸</span> {f}
                    </div>
                  ))}
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  )
}

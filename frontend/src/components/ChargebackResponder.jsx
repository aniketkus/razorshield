import { useState } from 'react'
import axios from 'axios'
import { CreditCard, Loader2, FileText, Trophy, Copy, Check } from 'lucide-react'

const PRESET = {
  txn_id: 'pay_DEMO002', customer_id: 'cust_000003', merchant_id: 'merch_0002',
  merchant_name: 'QuickElectronics Pvt Ltd', category: 'electronics', amount: 18000,
  payment_method: 'card', state: 'KA', device_type: 'desktop', browser: 'chrome',
  hour: 14, day_of_week: 2, txn_velocity_24h: 1, amount_velocity_24h: 18000,
  device_fp_count: 1, delivery_confirmed: true, ip_address: '103.21.56.78',
  shipping_address: 'Koramangala, Bangalore, KA 560034',
  dispute_reason: 'not_received', txn_timestamp: '2025-07-15 14:32:00 IST',
}

const DISPUTE_REASONS = ['not_received', 'unauthorized', 'duplicate', 'unknown']

export default function ChargebackResponder() {
  const [form, setForm] = useState(PRESET)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [copied, setCopied] = useState(false)

  const set = (k, v) => setForm(f => ({ ...f, [k]: v }))

  const submit = async () => {
    setLoading(true); setError(null); setResult(null)
    try {
      const { data } = await axios.post('/api/v1/chargeback/respond', form)
      setResult(data)
    } catch (e) {
      setError(e.response?.data?.detail || 'API error — is the backend running?')
    } finally {
      setLoading(false)
    }
  }

  const copyDoc = async () => {
    if (!result) return
    await navigator.clipboard.writeText(result.evidence_document)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const winPct = result ? Math.round(result.win_probability * 100) : 0
  const winColor = winPct >= 60 ? '#10b981' : winPct >= 40 ? '#f59e0b' : '#ef4444'

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-emerald-500/10 flex items-center justify-center">
          <CreditCard size={20} className="text-emerald-400" />
        </div>
        <div>
          <h1 className="text-xl font-bold text-white">Chargeback Evidence Responder</h1>
          <p className="text-sm text-slate-400">Auto-generated dispute response documents · Logistic Regression</p>
        </div>
        <button onClick={() => setForm(PRESET)} className="ml-auto text-xs px-3 py-1.5 bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 rounded-lg hover:bg-emerald-500/20 transition-all">
          Load Sample
        </button>
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        {/* Form */}
        <div className="card space-y-4">
          <h2 className="font-semibold text-white">Dispute Details</h2>
          <div className="grid grid-cols-2 gap-3">
            {[
              ['txn_id',        'Transaction ID', 'text'],
              ['merchant_name', 'Merchant Name',  'text'],
              ['amount',        'Amount (₹)',      'number'],
              ['category',      'Category',       'text'],
            ].map(([k, label, type]) => (
              <div key={k}>
                <label className="text-xs text-slate-400 mb-1 block">{label}</label>
                <input type={type} value={form[k]} onChange={e => set(k, type === 'number' ? +e.target.value : e.target.value)} className="input-field" />
              </div>
            ))}
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-xs text-slate-400 mb-1 block">Dispute Reason</label>
              <select value={form.dispute_reason} onChange={e => set('dispute_reason', e.target.value)} className="input-field">
                {DISPUTE_REASONS.map(r => <option key={r} value={r}>{r.replace('_', ' ')}</option>)}
              </select>
            </div>
            <div>
              <label className="text-xs text-slate-400 mb-1 block">Payment Method</label>
              <select value={form.payment_method} onChange={e => set('payment_method', e.target.value)} className="input-field">
                {['upi','card','netbanking'].map(r => <option key={r} value={r}>{r}</option>)}
              </select>
            </div>
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-xs text-slate-400 mb-1 block">IP Address</label>
              <input value={form.ip_address} onChange={e => set('ip_address', e.target.value)} className="input-field" />
            </div>
            <div>
              <label className="text-xs text-slate-400 mb-1 block">Txn Timestamp</label>
              <input value={form.txn_timestamp} onChange={e => set('txn_timestamp', e.target.value)} className="input-field" />
            </div>
          </div>
          <div>
            <label className="text-xs text-slate-400 mb-1 block">Shipping Address</label>
            <input value={form.shipping_address} onChange={e => set('shipping_address', e.target.value)} className="input-field" />
          </div>
          <div className="flex items-center gap-3">
            <input type="checkbox" id="delivery" checked={form.delivery_confirmed}
              onChange={e => set('delivery_confirmed', e.target.checked)}
              className="w-4 h-4 rounded accent-emerald-500" />
            <label htmlFor="delivery" className="text-sm text-slate-300">Delivery confirmed by logistics partner</label>
          </div>
          <button onClick={submit} disabled={loading}
            className="btn-primary w-full flex items-center justify-center gap-2"
            style={{ background: '#059669' }}
            onMouseEnter={e => e.currentTarget.style.background = '#047857'}
            onMouseLeave={e => e.currentTarget.style.background = '#059669'}>
            {loading ? <><Loader2 size={16} className="animate-spin" /> Generating…</> : <><FileText size={16} /> Generate Evidence Response</>}
          </button>
          {error && <div className="text-red-400 text-sm bg-red-500/10 rounded-xl p-3 border border-red-500/20">{error}</div>}
        </div>

        {/* Result */}
        <div className="card space-y-4">
          <h2 className="font-semibold text-white">Dispute Response</h2>
          {!result && !loading && (
            <div className="flex flex-col items-center justify-center h-64 text-slate-600 text-sm">
              <FileText size={40} className="mb-3 opacity-30" />
              Generate a response to see the evidence document
            </div>
          )}
          {loading && (
            <div className="flex flex-col items-center justify-center h-64 gap-3">
              <Loader2 size={32} className="animate-spin text-emerald-400" />
              <span className="text-sm text-slate-400">Analysing dispute…</span>
            </div>
          )}
          {result && (
            <>
              {/* Win probability */}
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-800/60 rounded-xl p-4 border border-slate-700">
                  <div className="text-xs text-slate-500 mb-1">Chargeback Risk</div>
                  <div className="text-2xl font-bold text-red-400">{(result.chargeback_risk * 100).toFixed(1)}%</div>
                </div>
                <div className="rounded-xl p-4 border" style={{ borderColor: winColor + '44', background: winColor + '11' }}>
                  <div className="text-xs text-slate-500 mb-1">Win Probability</div>
                  <div className="text-2xl font-bold flex items-center gap-1" style={{ color: winColor }}>
                    <Trophy size={18} /> {winPct}%
                  </div>
                </div>
              </div>

              <div className="bg-slate-800 rounded-xl p-3 border border-slate-700 text-sm font-medium text-white">
                {result.recommended_action}
              </div>

              {/* Evidence points */}
              <div>
                <div className="text-xs text-slate-400 mb-2 font-semibold uppercase tracking-wide">Evidence Points</div>
                <div className="space-y-1.5">
                  {result.evidence_points.map((p, i) => (
                    <div key={i} className="flex items-start gap-2 text-sm text-slate-300">
                      <span className="text-emerald-400 mt-0.5 shrink-0">✓</span> {p}
                    </div>
                  ))}
                </div>
              </div>

              {/* Document */}
              <div>
                <div className="flex items-center justify-between mb-2">
                  <div className="text-xs text-slate-400 font-semibold uppercase tracking-wide">Evidence Document</div>
                  <button onClick={copyDoc} className="flex items-center gap-1.5 text-xs text-slate-400 hover:text-white transition-colors">
                    {copied ? <><Check size={13} className="text-emerald-400" /> Copied!</> : <><Copy size={13} /> Copy</>}
                  </button>
                </div>
                <pre className="bg-slate-950 border border-slate-800 rounded-xl p-4 text-xs text-slate-300 overflow-auto max-h-64 whitespace-pre-wrap font-mono">
                  {result.evidence_document}
                </pre>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  )
}

import { useState, useEffect } from 'react'
import { TrendingDown, ShieldCheck, AlertTriangle, IndianRupee, Zap, RotateCcw, CreditCard, ArrowRight } from 'lucide-react'
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'

// Simulated live transaction feed
function generateLiveTxn(id) {
  const categories = ['electronics', 'fashion', 'groceries', 'travel', 'gaming']
  const methods    = ['upi', 'card', 'netbanking', 'wallet']
  const scores     = () => Math.random()
  const score = scores()
  return {
    id: `pay_${String(id).padStart(8, '0')}`,
    category: categories[Math.floor(Math.random() * categories.length)],
    method: methods[Math.floor(Math.random() * methods.length)],
    amount: Math.round(Math.random() * 50000 + 200),
    fraudScore: parseFloat(score.toFixed(3)),
    risk: score < 0.2 ? 'LOW' : score < 0.45 ? 'MEDIUM' : score < 0.7 ? 'HIGH' : 'CRITICAL',
    time: new Date().toLocaleTimeString(),
  }
}

const RISK_COLORS = { LOW: '#10b981', MEDIUM: '#f59e0b', HIGH: '#f97316', CRITICAL: '#ef4444' }

const SUMMARY_TREND = Array.from({ length: 12 }, (_, i) => ({
  month: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][i],
  fraud: Math.round(Math.random() * 40 + 60),
  returns: Math.round(Math.random() * 60 + 80),
  chargebacks: Math.round(Math.random() * 20 + 30),
}))

const PIE_DATA = [
  { name: 'Fraud Caught', value: 82, color: '#3b82f6' },
  { name: 'Returns Flagged', value: 73, color: '#f59e0b' },
  { name: 'Chargebacks Won', value: 68, color: '#10b981' },
]

export default function Dashboard({ onNavigate }) {
  const [feed, setFeed] = useState(() => Array.from({ length: 8 }, (_, i) => generateLiveTxn(i)))
  const [counter, setCounter] = useState(9)
  const [stats, setStats] = useState({ fraudBlocked: 1247, returnsFlagged: 3892, cbWon: 189 })

  useEffect(() => {
    const interval = setInterval(() => {
      setFeed(prev => [generateLiveTxn(counter), ...prev.slice(0, 9)])
      setCounter(c => c + 1)
      setStats(s => ({
        fraudBlocked: s.fraudBlocked + (Math.random() > 0.7 ? 1 : 0),
        returnsFlagged: s.returnsFlagged + (Math.random() > 0.5 ? 1 : 0),
        cbWon: s.cbWon + (Math.random() > 0.85 ? 1 : 0),
      }))
    }, 1800)
    return () => clearInterval(interval)
  }, [counter])

  const statCards = [
    {
      icon: Zap, label: 'Fraud Blocked', value: stats.fraudBlocked.toLocaleString(),
      sub: '↑ ₹2.4Cr saved this month', color: 'text-blue-400', bg: 'bg-blue-500/10',
      tab: 'fraud',
    },
    {
      icon: RotateCcw, label: 'Returns Flagged', value: stats.returnsFlagged.toLocaleString(),
      sub: '↑ ₹89L margin protected', color: 'text-amber-400', bg: 'bg-amber-500/10',
      tab: 'return',
    },
    {
      icon: CreditCard, label: 'Chargebacks Won', value: stats.cbWon.toLocaleString(),
      sub: '68% win rate · ₹34L recovered', color: 'text-emerald-400', bg: 'bg-emerald-500/10',
      tab: 'chargeback',
    },
    {
      icon: ShieldCheck, label: 'False-Positive Rate', value: '4.2%',
      sub: 'Below 5% industry threshold', color: 'text-purple-400', bg: 'bg-purple-500/10',
      tab: 'metrics',
    },
  ]

  return (
    <div className="space-y-8">
      {/* Hero */}
      <div className="text-center py-6">
        <h1 className="text-4xl font-bold text-white mb-2">
          🛡️ RazorShield
        </h1>
        <p className="text-slate-400 text-lg">AI-powered defense against fraud, returns & chargebacks for Indian merchants</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {statCards.map(({ icon: Icon, label, value, sub, color, bg, tab }) => (
          <button key={label} onClick={() => onNavigate(tab)}
            className="card text-left hover:border-slate-600 transition-all group cursor-pointer">
            <div className={`w-10 h-10 rounded-xl ${bg} flex items-center justify-center mb-4`}>
              <Icon size={20} className={color} />
            </div>
            <div className="text-2xl font-bold text-white">{value}</div>
            <div className="text-sm font-medium text-slate-300 mt-1">{label}</div>
            <div className="text-xs text-slate-500 mt-1">{sub}</div>
            <div className={`flex items-center gap-1 mt-3 text-xs ${color} opacity-0 group-hover:opacity-100 transition-opacity`}>
              Open module <ArrowRight size={12} />
            </div>
          </button>
        ))}
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        {/* Live Feed */}
        <div className="card lg:col-span-2">
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-semibold text-white flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
              Live Transaction Feed
            </h2>
            <span className="text-xs text-slate-500">auto-updating every 1.8s</span>
          </div>
          <div className="space-y-2 max-h-72 overflow-auto pr-1">
            {feed.map((txn, i) => (
              <div key={txn.id}
                className={`flex items-center justify-between p-3 rounded-xl border transition-all
                  ${i === 0 ? 'border-blue-500/40 bg-blue-500/5' : 'border-slate-800 bg-slate-900/40'}`}>
                <div className="flex items-center gap-3">
                  <span className="text-xs font-mono text-slate-500">{txn.id}</span>
                  <span className="text-xs text-slate-400 capitalize">{txn.category}</span>
                  <span className="text-xs text-slate-500 uppercase">{txn.method}</span>
                </div>
                <div className="flex items-center gap-3">
                  <span className="text-sm font-semibold text-white">₹{txn.amount.toLocaleString()}</span>
                  <span className={`text-xs font-bold px-2 py-0.5 rounded-full`}
                    style={{ color: RISK_COLORS[txn.risk], background: RISK_COLORS[txn.risk] + '22' }}>
                    {txn.risk}
                  </span>
                  <span className="text-xs text-slate-600">{txn.time}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Pie */}
        <div className="card">
          <h2 className="font-semibold text-white mb-4">Detection Rates</h2>
          <div className="flex justify-center">
            <PieChart width={180} height={180}>
              <Pie data={PIE_DATA} cx={90} cy={90} innerRadius={50} outerRadius={80}
                dataKey="value" stroke="none">
                {PIE_DATA.map((d, i) => <Cell key={i} fill={d.color} />)}
              </Pie>
            </PieChart>
          </div>
          <div className="space-y-2 mt-2">
            {PIE_DATA.map(d => (
              <div key={d.name} className="flex items-center justify-between text-sm">
                <div className="flex items-center gap-2">
                  <span className="w-2.5 h-2.5 rounded-full" style={{ background: d.color }} />
                  <span className="text-slate-400">{d.name}</span>
                </div>
                <span className="font-semibold text-white">{d.value}%</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Trend chart */}
      <div className="card">
        <h2 className="font-semibold text-white mb-6">Monthly Risk Events (Stopped)</h2>
        <ResponsiveContainer width="100%" height={200}>
          <AreaChart data={SUMMARY_TREND}>
            <defs>
              <linearGradient id="gFraud" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
              </linearGradient>
              <linearGradient id="gReturn" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#f59e0b" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="#f59e0b" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <XAxis dataKey="month" stroke="#475569" tick={{ fontSize: 11 }} />
            <YAxis stroke="#475569" tick={{ fontSize: 11 }} />
            <Tooltip contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: 12, fontSize: 12 }} />
            <Area type="monotone" dataKey="fraud" stroke="#3b82f6" fill="url(#gFraud)" strokeWidth={2} name="Fraud Blocked" />
            <Area type="monotone" dataKey="returns" stroke="#f59e0b" fill="url(#gReturn)" strokeWidth={2} name="Returns Flagged" />
            <Area type="monotone" dataKey="chargebacks" stroke="#10b981" fill="none" strokeWidth={2} name="Chargebacks Won" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}

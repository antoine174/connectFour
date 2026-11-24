import { useState } from 'react'

const BREAKDOWN_LABELS = [
  ['locked_fours', 'Locked 4s'],
  ['threats', '3-in-a-Row Threats'],
  ['open_twos', 'Open 2s'],
  ['position', 'Board Position'],
]

// Connected-4 counts, discs played and the live heuristic (with a collapsible breakdown).
export default function Scoreboard({ game }) {
  const [showBreakdown, setShowBreakdown] = useState(false)

  return (
    <div className="scoreboard">
      <div className="score-row">
        <div className="stat"><span>Human 4s</span><strong>{game.human_score}</strong></div>
        <div className="stat"><span>AI 4s</span><strong>{game.ai_score}</strong></div>
        <div className="stat"><span>Discs</span><strong>{game.discs_played} / 42</strong></div>
        <div className="stat"><span>Heuristic</span><strong>{game.current_heuristic}</strong></div>
      </div>

      <button className="link" onClick={() => setShowBreakdown(!showBreakdown)}>
        {showBreakdown ? '▼' : '▶'} Heuristic breakdown
      </button>
      {showBreakdown && (
        <ul className="breakdown">
          {BREAKDOWN_LABELS.map(([key, label]) => (
            <li key={key}><span>{label}</span><b>{game.heuristic_breakdown[key]}</b></li>
          ))}
          <li className="total"><span>Total</span><b>{game.heuristic_breakdown.total}</b></li>
        </ul>
      )}
    </div>
  )
}

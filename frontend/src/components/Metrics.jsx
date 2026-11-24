// Cards describing the AI's most recent search.
export default function Metrics({ aiMove, stats }) {
  const cards = [
    ['Chosen Column', aiMove ?? '-'],
    ['Nodes Expanded', stats?.nodes_expanded ?? '-'],
    ['Pruned Branches', stats?.pruned_branches ?? '-'],
    ['Time (ms)', stats?.execution_time_ms ?? '-'],
    ['Depth K', stats?.k ?? '-'],
  ]
  return (
    <div className="metrics">
      {cards.map(([label, value]) => (
        <div className="stat" key={label}><span>{label}</span><strong>{value}</strong></div>
      ))}
    </div>
  )
}

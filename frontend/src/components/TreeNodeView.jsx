import { useState } from 'react'

// One node of the minimax tree. Children render recursively.
// `expandSignal` = { version, open }: bumping it forces every node open/closed (Expand/Collapse All).
export default function TreeNodeView({ node, expandSignal }) {
  const [open, setOpen] = useState(node.depth <= 1)
  const [seenVersion, setSeenVersion] = useState(expandSignal.version)

  // React to a new Expand All / Collapse All click.
  if (seenVersion !== expandSignal.version) {
    setSeenVersion(expandSignal.version)
    setOpen(expandSignal.open)
  }

  const hasChildren = node.children.length > 0
  const label = node.move === null ? 'ROOT' : `Col ${node.move}`

  return (
    <div className="tree-node">
      <div className={`tree-row ${node.is_pruned ? 'pruned' : ''}`}>
        <button className="toggle" disabled={!hasChildren} onClick={() => setOpen(!open)}>
          {hasChildren ? (open ? '▼' : '▶') : '•'}
        </button>
        <strong>{label}</strong>
        <span className={`badge ${node.node_type.toLowerCase()}`}>{node.node_type}</span>
        {node.is_pruned && <span className="badge pruned-badge">PRUNED</span>}
        {node.is_leaf && <span className="badge leaf">LEAF (Heuristic: {node.heuristic_value})</span>}
        {!node.is_pruned && <span className="value">Val: {node.value}</span>}
        <span className="ab">α={String(node.alpha)} β={String(node.beta)}</span>
      </div>

      {open && hasChildren && (
        <div className="tree-children">
          {node.children.map((child, i) => (
            <TreeNodeView key={i} node={child} expandSignal={expandSignal} />
          ))}
        </div>
      )}
    </div>
  )
}

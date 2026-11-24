import { useState } from 'react'
import TreeNodeView from './TreeNodeView.jsx'

// Wrapper with the Expand All / Collapse All buttons.
export default function TreeViewer({ tree, searchId }) {
  const [signal, setSignal] = useState({ version: 0, open: true })
  const bump = (open) => setSignal({ version: signal.version + 1, open })

  if (!tree) return <p className="muted">The AI's search tree appears here after its first move.</p>

  return (
    <div className="tree-viewer">
      <div className="tree-buttons">
        <button onClick={() => bump(true)}>Expand All</button>
        <button onClick={() => bump(false)}>Collapse All</button>
      </div>
      {/* key = search number: a new AI search gets a fresh tree (depth 0-1 open) */}
      <TreeNodeView key={searchId} node={tree} expandSignal={signal} />
    </div>
  )
}

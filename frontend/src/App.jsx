import { useState } from 'react'
import { newGame, sendMove } from './api.js'
import Controls from './components/Controls.jsx'
import Board from './components/Board.jsx'
import Scoreboard from './components/Scoreboard.jsx'
import Metrics from './components/Metrics.jsx'
import TreeViewer from './components/TreeViewer.jsx'

export default function App() {
  const [settings, setSettings] = useState({ humanColor: 'red', firstPlayer: 'human', k: 4 })
  const [game, setGame] = useState(null)        // latest state from the backend
  const [tree, setTree] = useState(null)        // latest AI search tree
  const [stats, setStats] = useState(null)
  const [searchId, setSearchId] = useState(0)  // increments per AI search
  const [aiMove, setAiMove] = useState(null)
  const [busy, setBusy] = useState(false)       // true while waiting for the server
  const [error, setError] = useState('')

  // Store a backend response. Tree/stats only change when the AI actually searched.
  function applyResponse(data) {
    setGame(data)
    setAiMove(data.ai_move)
    if (data.search_tree) {
      setTree(data.search_tree)
      setSearchId((id) => id + 1)
      setStats(data.stats)
    }
  }

  async function startGame() {
    setBusy(true); setError('')
    setTree(null); setStats(null)
    try {
      applyResponse(await newGame({
        human_color: settings.humanColor, k: settings.k, first_player: settings.firstPlayer,
      }))
    } catch (e) { setError(e.message) }
    setBusy(false)
  }

  async function handleColumnClick(col) {
    // Show the human disc immediately, then wait for the AI's reply.
    const board = game.board.map((row) => [...row])
    for (let r = 5; r >= 0; r--) {
      if (board[r][col] === 0) { board[r][col] = 1; break }
    }
    setGame({ ...game, board })
    setAiMove(null)
    setBusy(true); setError('')
    try {
      applyResponse(await sendMove(col))
    } catch (e) { setError(e.message) }
    setBusy(false)
  }

  const winnerText = game?.winner === 'human' ? 'You win!' : game?.winner === 'ai' ? 'The AI wins!' : 'Draw!'

  return (
    <div className="app">
      <Controls settings={settings} onChange={setSettings} onStart={startGame} disabled={busy} />
      {error && <div className="error">{error} (is the backend running on port 5000?)</div>}

      {!game ? (
        <p className="muted center">Choose your settings and press “Start / New Game”.</p>
      ) : (
        <div className="dashboard">
          <section className="panel">
            <Scoreboard game={game} />
            <Board board={game.board} humanColor={settings.humanColor} aiMove={aiMove}
                   locked={busy || game.game_over} onColumnClick={handleColumnClick} />
            {busy && <p className="muted center">AI is thinking…</p>}
            {game.game_over && (
              <div className="banner">
                <h2>Game Over — {winnerText}</h2>
                <p>Human connected-4s: {game.human_score} · AI connected-4s: {game.ai_score}</p>
              </div>
            )}
          </section>

          <section className="panel">
            <h2>AI Metrics</h2>
            <Metrics aiMove={aiMove} stats={stats} />
            <h2>Minimax Tree</h2>
            <TreeViewer tree={tree} searchId={searchId} />
          </section>
        </div>
      )}
    </div>
  )
}

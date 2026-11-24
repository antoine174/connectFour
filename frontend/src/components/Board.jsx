import { useState } from 'react'

// 6x7 board. Cell values: 0 empty, 1 human, 2 AI.
export default function Board({ board, humanColor, aiMove, locked, onColumnClick }) {
  const [hoverCol, setHoverCol] = useState(null)
  const aiColor = humanColor === 'red' ? 'yellow' : 'red'
  const colorOf = (cell) => (cell === 1 ? humanColor : aiColor)

  // Row of the AI's last disc = the topmost filled cell in that column.
  const aiRow = aiMove == null ? -1 : board.findIndex((row) => row[aiMove] !== 0)

  const columnIsFull = (c) => board[0][c] !== 0

  return (
    <div className="board" onMouseLeave={() => setHoverCol(null)}>
      {[0, 1, 2, 3, 4, 5, 6].map((c) => {
        const canPlay = !locked && !columnIsFull(c)
        return (
          <div key={c}
               className={`column ${canPlay ? 'playable' : ''}`}
               onMouseEnter={() => setHoverCol(c)}
               onClick={() => canPlay && onColumnClick(c)}>
            {/* Hover preview of the human disc above the column */}
            <div className="cell preview">
              {canPlay && hoverCol === c && <div className={`disc ${humanColor} ghost`} />}
            </div>
            {board.map((row, r) => (
              <div key={r} className="cell">
                {row[c] !== 0 && (
                  <div className={`disc ${colorOf(row[c])} ${r === aiRow && c === aiMove ? 'last-ai' : ''}`} />
                )}
              </div>
            ))}
          </div>
        )
      })}
    </div>
  )
}

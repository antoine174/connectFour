// Thin wrapper around the Flask backend.
const API_URL = 'http://localhost:5000/api'

async function post(path, body) {
  const response = await fetch(`${API_URL}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  const data = await response.json()
  if (!response.ok) throw new Error(data.error || 'Request failed')
  return data
}

export const newGame = (settings) => post('/new-game', settings)
export const sendMove = (col) => post('/move', { col })

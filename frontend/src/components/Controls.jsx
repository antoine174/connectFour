// Top bar: pick colour, first player and depth K, then start a game.
export default function Controls({ settings, onChange, onStart, disabled }) {
  const set = (key, value) => onChange({ ...settings, [key]: value })

  return (
    <header className="controls">
      <h1>Connect 4 AI</h1>

      <label>
        Your color
        <select value={settings.humanColor} onChange={(e) => set('humanColor', e.target.value)}>
          <option value="red">Red</option>
          <option value="yellow">Yellow</option>
        </select>
      </label>

      <label>
        First player
        <select value={settings.firstPlayer} onChange={(e) => set('firstPlayer', e.target.value)}>
          <option value="human">Human</option>
          <option value="ai">Computer</option>
        </select>
      </label>

      <label>
        Depth K: <strong>{settings.k}</strong>
        <input type="range" min="1" max="6" value={settings.k}
               onChange={(e) => set('k', Number(e.target.value))} />
      </label>

      <button onClick={onStart} disabled={disabled}>Start / New Game</button>
    </header>
  )
}

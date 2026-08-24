const API_URL = "http://localhost:8000";

export async function startGame(playerName) {
  const res = await fetch(`${API_URL}/api/start`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ player_name: playerName }),
  });
  return res.json();
}

export async function nextTurn() {
  const res = await fetch(`${API_URL}/api/turn`, { method: "POST" });
  return res.json();
}

export async function resetGame() {
  const res = await fetch(`${API_URL}/api/reset`, { method: "POST" });
  return res.json();
}

export async function getState() {
  const res = await fetch(`${API_URL}/api/state`);
  return res.json();
}

export async function getWinner() {
  const res = await fetch(`${API_URL}/api/winner`);
  return res.json();
}

import { useState } from "react";

export default function MainMenu({ onStart, busy }) {
  const [name, setName] = useState("Player");

  return (
    <div className="menu-screen">
      <div className="menu-card">
        <h1>Cups</h1>
        <p>Beginner's luck...VERY important in Cups</p>

        <input
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Your name"
        />

        <button disabled={busy} onClick={() => onStart(name)}>
          {busy ? "Starting..." : "Start Game"}
        </button>
      </div>
    </div>
  );
}

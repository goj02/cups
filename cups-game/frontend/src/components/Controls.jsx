export default function Controls({ turn, deckCount, onNextTurn, onReset, busy, gameEnd }) {
  return (
    <div className="controls">
      <div>Turn: {turn}</div>
      <div>Deck: {deckCount}</div>

      {!gameEnd ? (
        <button disabled={busy} onClick={onNextTurn}>
          {busy ? "Working..." : "Deal Next Turn"}
        </button>
      ) : (
        <div className="game-over">Game Over</div>
      )}

      <button onClick={onReset}>Main Menu</button>
    </div>
  );
}

import HandView from "./HandView";
import Controls from "./Controls";
import EventLog from "./EventLog";
import DeckView from "./DeckView";

export default function GameTable({ gameState, onNextTurn, onReset, busy, customBack }) {
  const dealer = gameState.players?.Dealer;
  const player = gameState.players?.Player;

  return (
    <div
      className="table-wrap"
      style={{
        backgroundImage: `url(${gameState.background || "/assets/images/background.jpg"})`,
      }}
    >
      <div className="table-layout">
        <DeckView count={gameState.deck_count} customBack={customBack} />

        <div className="table-center">
          <HandView
            title={dealer?.name || "Dealer"}
            cards={dealer?.hand || []}
            facedown={false}
            customBack={customBack}
            dealer
          />

          <Controls
            turn={gameState.turn_number}
            deckCount={gameState.deck_count}
            onNextTurn={onNextTurn}
            onReset={onReset}
            busy={busy}
            gameEnd={gameState.game_end}
          />

          <EventLog events={gameState.last_events || []} />

          <HandView
            title={player?.name || "Player"}
            cards={player?.hand || []}
            facedown={false}
            customBack={customBack}
          />
        </div>
      </div>

      <div className="scoreboard">
        <div>{dealer?.name}: ${dealer?.money ?? 0}</div>
        <div>{player?.name}: ${player?.money ?? 0}</div>
      </div>
    </div>
  );
}



// import HandView from "./HandView";
// import Controls from "./Controls";
// import EventLog from "./EventLog";

// export default function GameTable({ gameState, onNextTurn, onReset, busy }) {
//   const dealer = gameState.players?.Dealer;
//   const player = gameState.players?.Player;

//   return (
//     <div className="table-wrap">
//       <div className="table">
//         <HandView title="Dealer" cards={dealer?.hand || []} facingDown />
//         <div className="center-panel">
//           <Controls
//             turn={gameState.turn_number}
//             deckCount={gameState.deck_count}
//             onNextTurn={onNextTurn}
//             onReset={onReset}
//             busy={busy}
//             gameEnd={gameState.game_end}
//           />
//           <EventLog events={gameState.last_events || []} />
//         </div>
//         <HandView title={player?.name || "Player"} cards={player?.hand || []} facingDown={false} />
//       </div>

//       <div className="scoreboard">
//         <div>{dealer?.name}: ${dealer?.money ?? 0}</div>
//         <div>{player?.name}: ${player?.money ?? 0}</div>
//       </div>
//     </div>
//   );
// }

import { useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import MainMenu from "./components/MainMenu";
import GameTable from "./components/GameTable";
import { startGame, nextTurn, resetGame } from "./api";

export default function App() {
  const [screen, setScreen] = useState("menu");
  const [playerName, setPlayerName] = useState("");
  const [gameState, setGameState] = useState(null);
  const [busy, setBusy] = useState(false);

  async function handleStart(name) {
    setBusy(true);
    const state = await startGame(name);
    setPlayerName(name);
    setGameState(state);
    setScreen("game");
    setBusy(false);
  }

  async function handleNextTurn() {
    setBusy(true);
    const state = await nextTurn();
    setGameState(state);
    setBusy(false);
  }

  async function handleReset() {
    setBusy(true);
    await resetGame();
    setGameState(null);
    setScreen("menu");
    setBusy(false);
  }

  return (
    <div className="app-shell">
      <AnimatePresence mode="wait">
        {screen === "menu" && (
          <motion.div
            key="menu"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.4 }}
          >
            <MainMenu onStart={handleStart} busy={busy} />
          </motion.div>
        )}

        {screen === "game" && gameState && (
          <motion.div
            key="game"
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 40 }}
            transition={{ duration: 0.4 }}
          >
            <GameTable
              gameState={gameState}
              onNextTurn={handleNextTurn}
              onReset={handleReset}
              busy={busy}
            />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

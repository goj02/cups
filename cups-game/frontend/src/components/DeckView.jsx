import { motion } from "framer-motion";

export default function DeckView({ count, customBack }) {
  const cards = Array.from({ length: Math.min(count, 10) });

  return (
    <div className="deck-wrap">
      <h3>Deck</h3>
      <motion.div className="deck-stack" layout>
        {cards.map((_, i) => (
          <motion.div
            key={i}
            className="deck-card"
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            style={{
              left: `${i * 2}px`,
              top: `${i * 2}px`,
              backgroundImage: `url(${customBack || "/assets/images/deck-back.png"})`,
              backgroundSize: "cover",
              backgroundPosition: "center",
              zIndex: i,
            }}
          />
        ))}
      </motion.div>
      <div className="deck-count">{count} left</div>
    </div>
  );
}

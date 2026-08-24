// import CardView from "./CardView";

// export default function HandView({ title, cards, facingDown }) {
//   return (
//     <div className={`hand-section ${facingDown ? "dealer" : "player"}`}>
//       <h2>{title}</h2>
//       <div className="hand">
//         {cards.map((card, i) => (
//           <CardView key={i} card={card} facedown={facingDown} index={i} />
//         ))}
//       </div>
//     </div>
//   );
// }

import CardView from "./CardView";
import { motion } from "framer-motion";

export default function HandView({ title, cards, facedown, customBack, dealer }) {
  return (
    <div className={`hand-section ${dealer ? "dealer" : "player"}`}>
      <h2>{title}</h2>
      <motion.div className="hand" layout>
        {cards.map((card, i) => (
          <CardView
            key={`${card.facevalue}-${card.suit}-${i}`}
            card={card}
            facedown={facedown}
            index={i}
            customBack={customBack}
          />
        ))}
      </motion.div>
    </div>
  );
}

import { motion } from "framer-motion";

export default function CardView({ card, facedown, index }) {
  
  // return (
  //   <motion.div
  //     className={`card ${facedown ? "facedown" : ""}`}
  //     initial={{ opacity: 0, y: -30, scale: 0.8 }}
  //     animate={{ opacity: 1, y: 0, scale: 1 }}
  //     transition={{ delay: index * 0.08, duration: 0.3 }}
  //   >
  //     {facedown ? "🂠" : `${card.facevalue}${card.suit}`}
  //   </motion.div>
  // );

  return (
    <motion.div
      className="card"
      initial={{ opacity: 0, y: -40, scale: 0.7, rotate: -8 }}
      animate={{ opacity: 1, y: 0, scale: 1, rotate: 0 }}
      transition={{ delay: index * 0.08, duration: 0.35, ease: "easeOut" }}
      style={
        facedown
          ? {
              backgroundImage: `url(${backImage})`,
              backgroundSize: "cover",
              backgroundPosition: "center",
              color: "transparent",
            }
          : {}
      }
    >
      {!facedown && `${card.facevalue}${card.suit}`}
    </motion.div>
  );

}

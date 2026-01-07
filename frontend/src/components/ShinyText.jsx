import React from "react";
import "./ShinyText.css";

export default function ShinyText({
  text = "",
  speed = 2,
  delay = 0,
  color = "#b5b5b5",
  shineColor = "#ffffff",
  spread = 120,
  direction = "left",
  yoyo = false,
  pauseOnHover = false,
}) {
  const animationDuration = `${speed}s`;
  const animationDelay = `${delay}s`;

  return (
    <span
      className={`shiny-text ${pauseOnHover ? "shiny-text-pause" : ""}`}
      style={{
        "--shiny-color": color,
        "--shiny-shine-color": shineColor,
        "--shiny-spread": `${spread}px`,
        "--shiny-duration": animationDuration,
        "--shiny-delay": animationDelay,
        "--shiny-direction": direction === "left" ? "normal" : "reverse",
        "--shiny-yoyo": yoyo ? "alternate" : "normal",
      }}
    >
      {text}
    </span>
  );
}

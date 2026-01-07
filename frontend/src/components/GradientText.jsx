import React from "react";
import "./GradientText.css";

export default function GradientText({
  children,
  colors = ["#40ffaa", "#4079ff", "#40ffaa", "#4079ff", "#40ffaa"],
  animationSpeed = 3,
  showBorder = false,
  className = "",
}) {
  const gradientString = colors.join(", ");
  const animationDuration = `${animationSpeed}s`;

  return (
    <span
      className={`gradient-text ${
        showBorder ? "gradient-text-border" : ""
      } ${className}`}
      style={{
        "--gradient-colors": gradientString,
        "--animation-speed": animationDuration,
      }}
    >
      {children}
    </span>
  );
}

import React from "react";
import "./Navbar.css";

export default function Navbar() {
  return (
    <header className="navShell">
      <div className="navContainer">
        <div className="navTitle">aayushbot</div>

        <nav className="navLinks" aria-label="Primary">
          <a className="navLink" href="#" target="_blank" rel="noreferrer">
            LinkedIn
          </a>
          <a className="navLink" href="#" target="_blank" rel="noreferrer">
            GitHub
          </a>
          <a className="navLink" href="#" target="_blank" rel="noreferrer">
            Resume
          </a>
        </nav>
      </div>
    </header>
  );
}

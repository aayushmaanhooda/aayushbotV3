import React from "react";
import "./Admin.css";
import { login, verifyAdmin, uploadAdminPdf, logout } from "../services/api.js";

export default function Admin() {
  const [username, setUsername] = React.useState("");
  const [password, setPassword] = React.useState("");
  const [isLoading, setIsLoading] = React.useState(false);
  const [error, setError] = React.useState("");
  const [success, setSuccess] = React.useState("");
  const [isAuthed, setIsAuthed] = React.useState(false);
  const [checking, setChecking] = React.useState(true);
  const [pdf, setPdf] = React.useState(null);

  React.useEffect(() => {
    let cancelled = false;
    async function run() {
      setChecking(true);
      setError("");
      try {
        await verifyAdmin();
        if (!cancelled) setIsAuthed(true);
      } catch {
        if (!cancelled) setIsAuthed(false);
      } finally {
        if (!cancelled) setChecking(false);
      }
    }
    run();
    return () => {
      cancelled = true;
    };
  }, []);

  async function onSubmit(e) {
    e.preventDefault();
    setError("");
    setSuccess("");
    setIsLoading(true);

    try {
      await login({ username, password });
      await verifyAdmin();
      setIsAuthed(true);
      setSuccess("Access granted.");
    } catch (err) {
      setError(err?.message || "Login failed");
    } finally {
      setIsLoading(false);
    }
  }

  async function onUpload(e) {
    e.preventDefault();
    setError("");
    setSuccess("");

    if (!pdf) {
      setError("Please choose a PDF file.");
      return;
    }

    setIsLoading(true);
    try {
      const res = await uploadAdminPdf(pdf);
      setSuccess(`Uploaded: ${res?.filename || "PDF"}`);
      setPdf(null);
      const input = document.getElementById("adminPdfInput");
      if (input) input.value = "";
    } catch (err) {
      setError(err?.message || "Upload failed");
    } finally {
      setIsLoading(false);
    }
  }

  async function onLogout() {
    setError("");
    setSuccess("");
    setIsLoading(true);
    try {
      await logout();
      setIsAuthed(false);
      setPdf(null);
      setUsername("");
      setPassword("");
      const input = document.getElementById("adminPdfInput");
      if (input) input.value = "";
      setSuccess("Logged out.");
    } catch (err) {
      setError(err?.message || "Logout failed");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="adminRoot">
      <div className="adminCard">
        <div className="adminHeader">
          <div className="adminHeaderRow">
            <div className="adminBadge">Admin</div>
            {isAuthed && !checking ? (
              <button
                type="button"
                className="adminLogout"
                onClick={onLogout}
                disabled={isLoading}
              >
                Logout
              </button>
            ) : null}
          </div>
          <h1 className="adminTitle">
            {checking
              ? "Checking access…"
              : isAuthed
              ? "Upload PDF"
              : "Sign in"}
          </h1>
          <p className="adminSubtitle">
            {checking
              ? "Verifying your session with the backend."
              : isAuthed
              ? "Choose a PDF and submit."
              : "Enter admin credentials to continue."}
          </p>
        </div>

        {isAuthed ? (
          <form className="adminForm" onSubmit={onUpload}>
            <label className="adminLabel">
              PDF
              <input
                id="adminPdfInput"
                className="adminFile"
                type="file"
                accept="application/pdf,.pdf"
                onChange={(e) => setPdf(e.target.files?.[0] || null)}
                disabled={checking || isLoading}
              />
            </label>

            {error ? (
              <div className="adminAlert adminAlertError">{error}</div>
            ) : null}
            {success ? (
              <div className="adminAlert adminAlertSuccess">{success}</div>
            ) : null}

            <button
              className="adminButton"
              type="submit"
              disabled={checking || isLoading}
            >
              {isLoading ? "Uploading…" : "Submit"}
            </button>
          </form>
        ) : (
          <form className="adminForm" onSubmit={onSubmit}>
            <label className="adminLabel">
              Username
              <input
                className="adminInput"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Username"
                autoComplete="username"
                required
                disabled={checking || isLoading}
              />
            </label>

            <label className="adminLabel">
              Password
              <input
                className="adminInput"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Password"
                autoComplete="current-password"
                required
                disabled={checking || isLoading}
              />
            </label>

            {error ? (
              <div className="adminAlert adminAlertError">{error}</div>
            ) : null}
            {success ? (
              <div className="adminAlert adminAlertSuccess">{success}</div>
            ) : null}

            <button
              className="adminButton"
              type="submit"
              disabled={checking || isLoading}
            >
              {isLoading ? "Signing in…" : "Access"}
            </button>
          </form>
        )}

        <div className="adminFooter">
          <a className="adminLink" href="/">
            ← Back to home
          </a>
        </div>
      </div>
    </div>
  );
}

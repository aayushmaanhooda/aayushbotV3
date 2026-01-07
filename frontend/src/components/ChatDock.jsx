import React from "react";
import "./ChatDock.css";
import { sendChatMessage } from "../services/api";

export default function ChatDock() {
  const [text, setText] = React.useState("");
  const [messages, setMessages] = React.useState([]);
  const [isLoading, setIsLoading] = React.useState(false);
  const [showWelcome, setShowWelcome] = React.useState(true);
  const messagesEndRef = React.useRef(null);
  const inputRef = React.useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  React.useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSuggestionClick = (suggestionText) => {
    setText(suggestionText);
    // Focus the input after a brief delay to ensure the text is set
    setTimeout(() => {
      inputRef.current?.focus();
    }, 100);
  };

  async function onSubmit(e) {
    e.preventDefault();
    const trimmed = text.trim();
    if (!trimmed || isLoading) return;

    // Fade out welcome message on first send
    if (showWelcome) {
      setShowWelcome(false);
    }

    // Add user message to UI
    const userMessage = { role: "user", content: trimmed };
    setMessages((prev) => [...prev, userMessage]);
    setText("");
    setIsLoading(true);

    try {
      // Send to backend
      const response = await sendChatMessage([...messages, userMessage]);

      // Add assistant response
      const assistantMessage = {
        role: "assistant",
        content: response.response,
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error("Chat error:", error);
      // Show error message
      const errorMessage = {
        role: "assistant",
        content: `❌ Error: ${error.message}`,
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div
      className="chatDockShell"
      role="contentinfo"
      aria-label="Chat interface"
    >
      {/* Welcome Card - Fades out when conversation starts */}
      {showWelcome && messages.length === 0 && (
        <div className="chatWelcomeCard">
          <div className="chatWelcomeContent">
            <img
              src="/profile.png"
              alt="Aayushmaan"
              className="chatWelcomeLogo"
            />
            <h3 className="chatWelcomeTitle">Ask me about Aayushmaan</h3>
            <p className="chatWelcomeSubtitle">
              GitHub repos, skills, experience, and more
            </p>

            {/* Suggestion Chips */}
            <div className="chatSuggestions">
              <button
                className="chatSuggestionChip"
                onClick={() => handleSuggestionClick("Summarize Aayushmaan")}
              >
                Summarize Aayushmaan
              </button>
              <button
                className="chatSuggestionChip"
                onClick={() =>
                  handleSuggestionClick("What's Aayushmaan's favorite F1 team?")
                }
              >
                Aayushmaan's fav F1 team
              </button>
              <button
                className="chatSuggestionChip"
                onClick={() =>
                  handleSuggestionClick(
                    "What's Aayushmaan's favorite AI framework?"
                  )
                }
              >
                Aayushmaan's fav AI framework
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Chat Container */}
      <div
        className={`chatContainer ${messages.length > 0 ? "chatActive" : ""}`}
      >
        {/* Messages Display */}
        {messages.length > 0 && (
          <div className="chatMessages">
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`chatMessage ${
                  msg.role === "user"
                    ? "chatMessageUser"
                    : "chatMessageAssistant"
                }`}
              >
                {/* Profile Picture */}
                <div className="chatAvatar">
                  {msg.role === "user" ? (
                    <img src="/cat.jpg" alt="You" className="chatAvatarUser" />
                  ) : (
                    <img
                      src="/profile.png"
                      alt="Aayushmaan"
                      className="chatAvatarBot"
                    />
                  )}
                </div>

                {/* Message Content */}
                <div className="chatMessageBubble">
                  <div className="chatMessageName">
                    {msg.role === "user" ? "You" : "Aayushmaan"}
                  </div>
                  <div className="chatMessageText">{msg.content}</div>
                </div>
              </div>
            ))}

            {/* Typing Indicator */}
            {isLoading && (
              <div className="chatMessage chatMessageAssistant">
                <div className="chatAvatar">
                  <img
                    src="/profile.png"
                    alt="Aayushmaan"
                    className="chatAvatarBot"
                  />
                </div>
                <div className="chatMessageBubble">
                  <div className="chatMessageName">Aayushmaan</div>
                  <div className="chatMessageText chatTyping">
                    <div className="typingDots">
                      <span className="typingDot"></span>
                      <span className="typingDot"></span>
                      <span className="typingDot"></span>
                    </div>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        )}

        {/* Input Form */}
        <form className="chatDockForm" onSubmit={onSubmit}>
          <input
            ref={inputRef}
            className="chatDockInput"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Ask me anything about Aayushmaan…"
            aria-label="Chat message"
            disabled={isLoading}
          />
          <button className="chatDockSend" type="submit" disabled={isLoading}>
            {isLoading ? "..." : "Send"}
          </button>
        </form>
      </div>
    </div>
  );
}

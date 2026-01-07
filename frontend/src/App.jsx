import React from "react";
import Admin from "./pages/Admin.jsx";
import Navbar from "./components/Navbar.jsx";
import ChatDock from "./components/ChatDock.jsx";
import Footer from "./components/Footer.jsx";
import ShinyText from "./components/ShinyText.jsx";
import GradientText from "./components/GradientText.jsx";
import "./App.css";

function usePathname() {
  const [pathname, setPathname] = React.useState(
    () => window.location.pathname
  );

  React.useEffect(() => {
    const onPopState = () => setPathname(window.location.pathname);
    window.addEventListener("popstate", onPopState);
    return () => window.removeEventListener("popstate", onPopState);
  }, []);

  return pathname;
}

const App = () => {
  const pathname = usePathname();

  if (pathname === "/admin") {
    return <Admin />;
  }

  return (
    <div className="appRoot">
      <Navbar />
      <main className="appMain"></main>
      <ChatDock />
      <Footer />
    </div>
  );
};

export default App;

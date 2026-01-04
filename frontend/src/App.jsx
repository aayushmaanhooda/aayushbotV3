import React from "react";
import Admin from "./pages/Admin.jsx";
import Navbar from "./components/Navbar.jsx";
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
      <main className="appMain">
        <h1 className="appHeading">Welcome to Chat Bot</h1>
      </main>
    </div>
  );
};

export default App;

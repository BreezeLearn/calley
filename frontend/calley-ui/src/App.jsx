import { useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Chat from "./pages/Chat";
import Create from "./pages/Create";
import Register from "./pages/Register";
import Auth from "./Auth";

function App() {
  const [count, setCount] = useState(0);

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route
          path="/dashboard"
          element={
            <Auth>
              <Dashboard />
            </Auth>
          }
        />
        <Route path="/c" element={<Chat />} />
        <Route
          path="/create-agent"
          element={
            <Auth>
              <Create />
            </Auth>
          }
        />
        <Route path="/signup" element={<Register />} />
      </Routes>
    </Router>
  );
}

export default App;

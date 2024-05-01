import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

function Auth({ children }) {
  const [isUserLoggedIn, setIsUserLoggedIn] = useState(false);
  const token = localStorage.getItem("token");
  const navigate = useNavigate();

  useEffect(() => {
    if (token) {
      setIsUserLoggedIn(true);
    } else {
      navigate("/login");
    }
  }, [token, navigate]);

  return isUserLoggedIn ? children : null;
}

export default Auth;

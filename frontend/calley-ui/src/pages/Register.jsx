import React, { useState } from "react";
import { Link } from "react-router-dom";

const Register = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleEmailChange = (e) => setEmail(e.target.value);
  const handlePasswordChange = (e) => setPassword(e.target.value);

  const handleSubmit = (e) => {
    e.preventDefault();
    // Add your login logic here
      console.log("Login with:", email, password);
      loginUser(email, password)
  };

  const loginUser = (email, password) => {
    // Add your login logic here
    if (email && password) {
      fetch("https://reqres.in/api/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
          password,
        }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.token) {
            localStorage.setItem("token", data.token);
            window.location.href = "/dashboard";
          } else {
            alert("Invalid credentials");
          }
        });
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <h2 className="text-2xl font-bold mb-4">Register</h2>
      <form
        className="w-full max-w-sm bg-white shadow-md rounded-xl py-16 px-8 mb-4"
        onSubmit={handleSubmit}
      >
        <div className="mb-4">
          <label
            htmlFor="email"
            className="block text-sm font-medium text-gray-700"
          >
            Email
          </label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={handleEmailChange}
            className="mt-1 p-2 block w-full border-gray-300 rounded-md shadow-sm  sm:text-sm bg-gray-100"
          />
        </div>
        <div className="mb-4">
          <label
            htmlFor="password"
            className="block text-sm font-medium text-gray-700"
          >
            Password
          </label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={handlePasswordChange}
            className="mt-1 p-2 block w-full border-gray-300 rounded-md shadow-sm  sm:text-sm bg-gray-100"
          />
        </div>
        <button
          type="submit"
          className="bg-[#36ce8c] text-white py-2 px-4 rounded-md hover:bg-[#36ce8c] focus:outline-none focus:ring-2 focus:ring-offset-2"
        >
          Signup
        </button>

        <Link
          to="/login"
          className="block text-sm font-medium text-slate-900 mt-4 underline"
        >
          Login
        </Link>
      </form>
    </div>
  );
};

export default Register;

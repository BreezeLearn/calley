import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { Trash2, Cog } from "lucide-react";

const Sidebar = () => {
  // const agents = [
  //   {
  //     id: 1,
  //     name: "Agent 1",
  //     image:
  //       "https://threedio-cdn.icons8.com/TBOahEGwvXbttOPimGnf4403_QjpUpq_JnDHEjtjRRI/rs:fit:256:256/czM6Ly90aHJlZWRp/by1wcm9kL3ByZXZp/ZXdzLzIwOC8yOTE2/ODMwNi1hYWU0LTQ5/NmYtYjdjNS02NDg1/NGNjOWUxYzIucG5n.png",
  //   },
  //   {
  //     id: 2,
  //     name: "Agent 2",
  //     image:
  //       "https://threedio-cdn.icons8.com/TBOahEGwvXbttOPimGnf4403_QjpUpq_JnDHEjtjRRI/rs:fit:256:256/czM6Ly90aHJlZWRp/by1wcm9kL3ByZXZp/ZXdzLzIwOC8yOTE2/ODMwNi1hYWU0LTQ5/NmYtYjdjNS02NDg1/NGNjOWUxYzIucG5n.png",
  //   },
  //   {
  //     id: 3,
  //     name: "Agent 3",
  //     image:
  //       "https://threedio-cdn.icons8.com/TBOahEGwvXbttOPimGnf4403_QjpUpq_JnDHEjtjRRI/rs:fit:256:256/czM6Ly90aHJlZWRp/by1wcm9kL3ByZXZp/ZXdzLzIwOC8yOTE2/ODMwNi1hYWU0LTQ5/NmYtYjdjNS02NDg1/NGNjOWUxYzIucG5n.png",
  //   },
  //   {
  //     id: 4,
  //     name: "Agent 4",
  //     image:
  //       "https://threedio-cdn.icons8.com/TBOahEGwvXbttOPimGnf4403_QjpUpq_JnDHEjtjRRI/rs:fit:256:256/czM6Ly90aHJlZWRp/by1wcm9kL3ByZXZp/ZXdzLzIwOC8yOTE2/ODMwNi1hYWU0LTQ5/NmYtYjdjNS02NDg1/NGNjOWUxYzIucG5n.png",
  //   },
  // ];
  const [agents, setAgents] = useState([]);
  const [uniqueId, setUniqueId] = useState(0);

  const handleDelete = (id) => {
    // Implement delete logic here
    console.log(`Deleting agent with id ${id}`);
  };

  const handleUpdate = (id) => {
    // Implement update logic here
    console.log(`Updating agent with id ${id}`);
  };

  const fetchAgents = () => {
    fetch("http://127.0.0.1:8000/bots", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    })
      .then((res) => res.json())
      .then((data) => {
        setAgents(data);
      });
  };

  useEffect(() => {
    fetchAgents();
  }, []);

  const setUniqueIdToLocalStorage = (id) => {
    localStorage.setItem("uniqueId", id);
  };

  return (
    <div className="bg-[#fff] w-[24rem] border-r text-slate-900 py-4 px-8 h-screen">
      <h3 className="font-bold text-lg mb-4">Active Agents</h3>
      <ul>
        {agents?.map((agent) => (
          <li
            key={agent.id}
            className="bg-gray-100 py-2 px-4 mb-2 rounded-lg flex justify-between items-center cursor-pointer"
            onClick={() => setUniqueIdToLocalStorage(agent.unique_id)}
          >
            <div className="flex gap-1 items-center">
              {" "}
              <img
                src="https://threedio-cdn.icons8.com/TBOahEGwvXbttOPimGnf4403_QjpUpq_JnDHEjtjRRI/rs:fit:256:256/czM6Ly90aHJlZWRp/by1wcm9kL3ByZXZp/ZXdzLzIwOC8yOTE2/ODMwNi1hYWU0LTQ5/NmYtYjdjNS02NDg1/NGNjOWUxYzIucG5n.png"
                alt={agent.name}
                style={{ width: "40px", height: "40px", borderRadius: "50%" }}
                className="rounded-full bg-slate-900"
              />
              <span>{agent.name}</span>
            </div>
            <div className="flex gap-3">
              <button onClick={() => handleUpdate(agent.id)}>
                <Cog size={18} />
              </button>
              <button onClick={() => handleDelete(agent.id)}>
                <Trash2 size={18} />
              </button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

const Content = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const handleInputChange = (event) => {
    setInput(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    if (input.trim() !== "") {
      setMessages((prevMessages) => [
        ...prevMessages,
        { content: input, role: "user" },
      ]);
      
      const uniqueId = localStorage.getItem("uniqueId");
      fetch("http://127.0.0.1:8000/bots/invoke", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify({ input: input, unique_id: uniqueId }),
      })
        .then((res) => res.json())
        .then((data) => {
          console.log(data);
          setMessages((prevMessages) => [
            ...prevMessages,
            { content: data.bot.output, role: "ai" },
          ]);
        })
        .catch((error) => {
          console.error("Error sending message:", error);
          
        });
  
      setInput("");
    }
  };
  


  
  
  return (
    <div className="w-full ">
      <div className="bg-gray-100 text-slate-900 h-[30rem] py-6 px-24 overflow-auto">
        <div className="text-lg font-bold mb-4">Chat History</div>
        {messages.map((message, index) => (
          <div
            key={index}
            className={`mb-4 p-2 rounded-md ${
              message.role === "ai"
                ? "text-left bg-[#fff]"
                : "bg-slate-900  text-white"
            }`}
          >
            {message.role === "ai" ? "AI: " : "User: "}
            {message.content}
          </div>
        ))}
      </div>
      <form
        onSubmit={handleSubmit}
        className="flex items-center justify-center bg-[#fff] bottom-0"
      >
        <div className="flex w-full px-24  py-4">
          <input
            type="text"
            value={input}
            onChange={handleInputChange}
            placeholder="Type your message..."
            style={{ width: "100%", marginTop: "10px", padding: "10px" }}
            className="border border-gray-300 rounded bg-gray-100 text-slate-900"
          />
          <button
            type="submit"
            style={{ marginTop: "10px", padding: "5px 10px" }}
          >
            Send
          </button>
        </div>
      </form>
    </div>
  );
};

function Dashboard() {
  return (
    <div className="bg-slate-900-200 h-screen">
      <div className="bg-[#fff] border-b  text-slate-900 py-4 px-8 flex justify-between items-center">
        <h1 className="font-bold text-3xl">Calley</h1>
        <div className="flex gap-4 text-lg justify-center items-center font-bold">
          <Link to="/create-agent" className="hover:underline">
            Create Agent
          </Link>
          
        </div>
      </div>

      <div>
        <div style={{ display: "flex" }}>
          <Sidebar />
          <Content />
        </div>
      </div>
    </div>
  );
}

export default Dashboard;

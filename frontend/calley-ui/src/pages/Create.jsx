import React, { useState } from "react";
import { Link } from "react-router-dom";
import { Trash2, Cog } from "lucide-react";

const Sidebar = () => {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [webSearch, setWebSearch] = useState(true);
  const [instruction, setInstruction] = useState("");

  const [documentName, setDocumentName] = useState("");
  const [documentContent, setDocumentContent] = useState("");

  const handleNameChange = (e) => setName(e.target.value);
  const handleDescriptionChange = (e) => setDescription(e.target.value);
  const handleWebSearchChange = (e) => setWebSearch(e.target.checked);
  const handleInstructionChange = (e) => setInstruction(e.target.value);
  const [activeTab, setActiveTab] = useState(0);

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log(name, description, webSearch, instruction);

    if (name && description) {
      fetch("http://127.0.0.1:8000/bots", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify({
          name: name,
          description: description,
          web_search: webSearch,
          instruction: instruction,
          tools: ["web_search"], //auto added from server
          unique_id: '77',// auto added from server this just a placeholder
          user_id: 0 // auto added from server this just a placeholder
        }),
      })
        .then((res) => res.json())
        .then((data) => {
          console.log(data);
          localStorage.setItem("uniqueId", data[0].unique_id);
          alert("Bot created successfully");
        })
        .catch((error) => {
          console.error("Error sending message:", error);
        });
    }
  };

  const handleDocumentNameChange = (e) => setDocumentName(e.target.value);
  const handleDocumentContentChange = (e) => setDocumentContent(e.target.value);

  const handleSubmitDocument = (e) => {
    e.preventDefault();

    if (documentName && documentContent) {
      fetch("http://127.0.0.1:8000/knowledge", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify({
          name: documentName,
          content: documentContent,
        }),
      }).then((res) => res.json());
    }
  };
  const setTab = (tab) => {
    setActiveTab(tab);
  };

  return (
    <>
      <div className="flex flex-col items-center justify-center  w-[26rem] p-8 border-r">
        <ul className=" flex gap-16 my-6 bg-gray-100 py-4 px-2 rounded-xl">
          <li className="hover:font-bold " onClick={() => setTab(0)}>
            Create{" "}
          </li>
          <li className="hover:font-bold " onClick={() => setTab(1)}>
            {" "}
            Add knowledge{" "}
          </li>
        </ul>
        <h2 className="text-2xl font-bold mb-4">Form</h2>

        {activeTab === 0 ? (
          <form className="w-full max-w-sm" onSubmit={handleSubmit}>
            <div className="mb-4">
              <label
                htmlFor="name"
                className="block text-sm font-medium text-gray-700"
              >
                Name
              </label>
              <input
                id="name"
                type="text"
                value={name}
                onChange={handleNameChange}
                className="mt-1 p-2 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              />
            </div>
            <div className="mb-4">
              <label
                htmlFor="description"
                className="block text-sm font-medium text-gray-700"
              >
                Description
              </label>
              <input
                id="description"
                type="text"
                value={description}
                onChange={handleDescriptionChange}
                className="mt-1 p-2 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              />
            </div>

            <div className="mb-4">
              <label
                htmlFor="instruction"
                className="block text-sm font-medium text-gray-700"
              >
                Instruction
              </label>
              <textarea
                id="instruction"
                value={instruction}
                onChange={handleInstructionChange}
                className="mt-1 p-2 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              ></textarea>
            </div>
            <div className="mb-4">
              <label htmlFor="webSearch" className="flex items-center">
                <input
                  id="webSearch"
                  type="checkbox"
                  checked={webSearch}
                  onChange={handleWebSearchChange}
                  className="form-checkbox h-5 w-5 text-indigo-600"
                />
                <span className="ml-2 text-sm text-gray-700">
                  Enable Web Search
                </span>
              </label>
            </div>
            <button
              type="submit"
              className="bg-[#36ce8c] text-white py-2 px-4 rounded-md hover:bg-[#36ce8c] focus:outline-none focus:ring-2  focus:ring-offset-2"
            >
              Submit
            </button>
          </form>
        ) : (
          <div>
            <form className="w-full max-w-sm" onSubmit={handleSubmitDocument}>
              <div className="mb-4">
                <label
                  htmlFor="document_name"
                  className="block text-sm font-medium text-gray-700"
                >
                  Name
                </label>
                <input
                  id="document_name"
                  type="text"
                  value={documentName}
                  onChange={handleDocumentNameChange}
                  className="mt-1 p-2 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                />
              </div>

              <div className="mb-4">
                <label
                  htmlFor="document_content"
                  className="block text-sm font-medium text-gray-700"
                >
                  Content
                </label>
                <textarea
                  id="document_content"
                  value={documentContent}
                  onChange={handleDocumentContentChange}
                  placeholder="Enter your content here"
                  className="mt-1 p-2 block w-full h-48 border-gray-300 rounded-md shadow-sm sm:text-sm"
                ></textarea>
              </div>
              {/* <div className="mb-4">
              <label htmlFor="webSearch" className="flex items-center">
                <input
                  id="webSearch"
                  type="checkbox"
                  checked={webSearch}
                  onChange={handleWebSearchChange}
                  className="form-checkbox h-5 w-5 text-indigo-600"
                />
                <span className="ml-2 text-sm text-gray-700">
                  Enable Web Search
                </span>
              </label>
            </div> */}
              <button
                type="submit"
                className="bg-[#36ce8c] text-white py-2 px-4 rounded-md hover:bg-[#36ce8c] focus:outline-none focus:ring-2  focus:ring-offset-2"
              >
                Submit
              </button>
            </form>
          </div>
        )}
      </div>
    </>
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

function Create() {
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

export default Create;

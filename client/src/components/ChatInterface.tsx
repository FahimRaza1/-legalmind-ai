"use client";
import { useState } from "react";

export default function ChatInterface() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");

  const askAI = async () => {
    const res = await fetch("http://localhost:8000/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: query }),
    });
    const data = await res.json();
    setResponse(data.answer);
  };

  return (
    <div className="w-full p-6 border rounded-xl bg-white shadow-lg">
      <input
        className="w-full p-3 border rounded-lg mb-4 text-black"
        placeholder="Ask a question about your document..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button
        onClick={askAI}
        className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700"
      >
        Ask LegalMind
      </button>
      {response && (
        <div className="mt-4 p-4 bg-gray-100 rounded text-black font-medium">
          {response}
        </div>
      )}
    </div>
  );
}

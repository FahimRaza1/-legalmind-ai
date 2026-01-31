"use client";
import { useState } from "react";

export default function ChatInterface() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  const askAI = async () => {
    setLoading(true);
    const res = await fetch("http://localhost:8000/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: query }),
    });
    const data = await res.json();
    setResponse(data.answer);
    setLoading(false);
  };

  const clearChat = () => {
    setQuery("");
    setResponse("");
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
        disabled={loading}
        className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
      >
        {loading ? "Searching..." : "Ask LegalMind"}
      </button>
      <button onClick={clearChat} className="ml-2 text-gray-400 hover:text-gray-600 underline text-sm">
        Clear
      </button>
      {response && (
        response.includes("not in the uploaded document") ? (
          <div className="mt-4 p-4 bg-orange-100 border-l-4 border-orange-500 rounded text-orange-800">
            <p className="text-xs font-bold uppercase mb-1">⚠️ Out of Scope</p>
            <p className="text-sm">{response}</p>
          </div>
        ) : (
          <div className="mt-4 p-4 bg-blue-50 border-l-4 border-blue-500 rounded text-black">
            <p className="text-xs font-bold text-blue-700 uppercase mb-1">Found in Document:</p>
            <p className="text-sm leading-relaxed italic">"{response}"</p>
          </div>
        )
      )}
    </div>
  );
}

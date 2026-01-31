"use client";
import { useState } from "react";

export default function FileUpload() {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<string>("");

  const handleUpload = async () => {
    if (!file) return alert("Please select a file first");

    const formData = new FormData();
    formData.append("file", file);

    try {
      setStatus("Uploading and processing...");
      const response = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
      });
      const result = await response.json();
      if (response.ok) {
        // Change the keys to match exactly what Developer A's backend sends
        setStatus(`✅ Success! Processed ${result.total_chars || 0} characters from ${result.filename || 'Document'}`);
      }
    } catch (error) {
      console.error("Upload failed", error);
      setStatus("Upload failed. Please try again.");
    }
  };

  return (
    <div className="p-10 border-2 border-dashed border-blue-200 rounded-2xl bg-white shadow-inner">
      <h3 className="text-lg font-semibold mb-4 text-gray-700">Upload Legal Document (PDF)</h3>
      <input 
        type="file" 
        accept=".pdf"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
        className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 mb-4"
      />
      <button 
        onClick={handleUpload}
        className="w-full py-3 bg-blue-600 text-white rounded-xl font-bold hover:bg-blue-700 transition-all"
      >
        Process Document
      </button>
      {status && (
        <p className="mt-4 text-sm text-center text-gray-700 font-medium">{status}</p>
      )}
    </div>
  );
}

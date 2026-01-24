"use client";
import { useState } from "react";

export default function FileUpload() {
  const [file, setFile] = useState<File | null>(null);

  const handleUpload = async () => {
    if (!file) return alert("Please select a file first");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
      });
      if (response.ok) alert("Upload Successful!");
    } catch (error) {
      console.error("Upload failed", error);
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
    </div>
  );
}

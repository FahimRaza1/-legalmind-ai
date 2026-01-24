"use client";
// Use relative paths instead of @/
import ConnectionStatus from "../components/ConnectionStatus";
import FileUpload from "../components/FileUpload";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center p-24 bg-gray-50">
      <h1 className="text-4xl font-extrabold mb-8 text-blue-900">LegalMind AI Dashboard</h1>
      
      <div className="w-full max-w-2xl space-y-8">
        {/* This is the status box you already see */}
        <ConnectionStatus />

        {/* Add this line to show the button on the screen */}
        <FileUpload /> 
      </div>
      
      <p className="mt-8 text-gray-500 text-sm italic">
        Systems are live. Ready for document ingestion.
      </p>
    </main>
  );
}

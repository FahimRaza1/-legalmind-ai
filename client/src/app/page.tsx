"use client";
import ConnectionStatus from "../components/ConnectionStatus";
import FileUpload from "../components/FileUpload";
import ChatInterface from "../components/ChatInterface";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center p-12 bg-gray-50 text-black">
      <h1 className="text-4xl font-extrabold mb-8 text-blue-900">LegalMind AI</h1>
      
      <div className="w-full max-w-2xl space-y-6">
        <ConnectionStatus />
        <FileUpload />
        <hr className="border-gray-300" />
        <h2 className="text-xl font-bold">Chat with Document</h2>
        <ChatInterface /> 
      </div>
    </main>
  );
}

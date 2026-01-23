"use client";
import { useEffect, useState } from "react";

export default function ConnectionStatus() {
  const [status, setStatus] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Use the Next.js rewrite proxy instead of direct localhost call
    fetch("/api/v1/health")
      .then((res) => res.json())
      .then((data) => {
        setStatus(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Connection failed:", err);
        setLoading(false);
      });
  }, []);

  if (loading) return <p className="p-4">Checking system vitals...</p>;

  return (
    <div className="p-6 m-4 border rounded-lg shadow-sm bg-slate-50">
      <h2 className="text-xl font-bold mb-4">System Status</h2>
      <ul className="space-y-2">
        <li>🟢 API: <span className="font-mono">{status?.api}</span></li>
        <li>🐘 Postgres: <span className={status?.postgres === "Connected" ? "text-green-600" : "text-red-600"}>{status?.postgres}</span></li>
        <li>🧠 ChromaDB: <span className={status?.chroma === "Connected" ? "text-green-600" : "text-red-600"}>{status?.chroma}</span></li>
      </ul>
    </div>
  );
}

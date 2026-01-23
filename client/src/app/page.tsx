import ConnectionStatus from "../components/ConnectionStatus";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <h1 className="text-4xl font-extrabold mb-8">LegalMind AI Dashboard</h1>
      <ConnectionStatus />
      <p className="mt-4 text-gray-500">
        If all status lights are green, Developer A and B are synced!
      </p>
    </main>
  );
}

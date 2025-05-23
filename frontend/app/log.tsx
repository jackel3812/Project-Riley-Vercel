"use client";

import { useState } from "react";

export default function LogPage() {
  const [logs, setLogs] = useState([
    { id: 1, message: "Module Not Found: Can't resolve '@/components/ui/button'", type: "Error" },
    { id: 2, message: "Missing 'use client' in /app/page.tsx", type: "Warning" },
  ]);

  return (
    <div className="p-6 bg-gray-900 text-white min-h-screen">
      <h1 className="text-xl font-bold">Error Log</h1>
      <ul className="mt-4 space-y-2">
        {logs.map((log) => (
          <li key={log.id} className="p-3 border-l-4 border-red-500 bg-gray-800">
            <strong>{log.type}:</strong> {log.message}
          </li>
        ))}
      </ul>
    </div>
  );
}

"use client";

import { useState } from "react";

export default function ConsolePage() {
  const [command, setCommand] = useState("");
  const [output, setOutput] = useState("");

  const executeCommand = async () => {
    try {
      // Simulating Bash execution
      if (command === "ls") setOutput("file1.txt\nfile2.tsx\ncomponents/");
      else if (command === "pwd") setOutput("/home/user/project");
      else setOutput("Unknown command");
    } catch (err) {
      setOutput("Error executing command");
    }
  };

  return (
    <div className="p-6 bg-gray-900 text-white min-h-screen">
      <h1 className="text-xl font-bold">Bash Console</h1>
      <input
        type="text"
        className="w-full p-2 bg-gray-800 border border-gray-700 mt-4"
        placeholder="Enter Bash command"
        value={command}
        onChange={(e) => setCommand(e.target.value)}
      />
      <button className="mt-3 p-2 bg-green-600" onClick={executeCommand}>Run</button>
      <pre className="mt-4 p-3 bg-gray-800 border-l-4 border-green-500">{output}</pre>
    </div>
  );
}

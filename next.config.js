/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  },
  images: {
    unoptimized: true,
   
    "use client";

import { useState } from "react";

export default function AutoGenFixPage() {
  const [errorLog, setErrorLog] = useState<string>("");
  const [fixedCode, setFixedCode] = useState<string>("");

  const detectError = async () => {
    try {
      const response = await fetch("/api/fix", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code: errorLog }),
      });
      const data = await response.json();
      setFixedCode(data.fixed_code);
    } catch (err) {
      setErrorLog("Error fetching AutoGen fix.");
    }
  };

  return (
    <div className="p-6 bg-gray-900 text-white min-h-screen">
      <h1 className="text-xl font-bold">AutoGen Debugging</h1>
      <button className="mt-4 p-2 bg-red-600" onClick={detectError}>Detect & Fix Error</button>
      <pre className="mt-4 p-3 bg-gray-800">{fixedCode || "No fix applied yet."}</pre>
    </div>
  );
}
  },
}



module.exports = nextConfig

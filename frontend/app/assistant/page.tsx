'use client';

import { useState } from "react";
import { Button } from "@/components/Button";
import { Card } from "@/components/Card";
import { API_BASE } from "@/lib/api";

export default function AssistantPage() {
  const [prompt, setPrompt] = useState("");
  const [response, setResponse] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [privacyMode, setPrivacyMode] = useState(false);

  async function submitPrompt() {
    setLoading(true);
    setResponse(null);

    try {
      const hashedData = btoa(unescape(encodeURIComponent(prompt))).slice(0, 64);
      const res = await fetch(`${API_BASE}/assistant/query`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          client_hashed_input: hashedData,
          privacy_mode: privacyMode,
        }),
      });
      if (!res.ok) throw new Error("Assistant API request failed");
      const payload = await res.json();
      setResponse(payload.assistant_response);
    } catch (err) {
      setResponse(String(err));
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 px-6 py-10">
      <div className="mx-auto flex max-w-4xl flex-col gap-8">
        <div className="space-y-2">
          <p className="text-sm uppercase tracking-[0.3em] text-brand-300">AI Assistant</p>
          <h1 className="text-4xl font-semibold text-white">Security guidance and recommendations</h1>
          <p className="text-slate-400">Ask the assistant about password health, credential hygiene, and account security.</p>
        </div>

        <Card>
          <label className="mb-3 block text-sm font-medium text-slate-300">Input prompt</label>
          <textarea
            value={prompt}
            onChange={(event) => setPrompt(event.target.value)}
            className="min-h-[160px] w-full rounded-3xl border border-slate-800 bg-slate-900/90 p-4 text-slate-100 outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-500/20"
          />
          <div className="mt-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <div className="flex items-center gap-3">
              <input
                id="privacy"
                type="checkbox"
                checked={privacyMode}
                onChange={(event) => setPrivacyMode(event.target.checked)}
                className="h-4 w-4 rounded border-slate-700 bg-slate-900 text-brand-500 focus:ring-brand-500"
              />
              <label htmlFor="privacy" className="text-sm text-slate-300">
                Privacy mode (client-side hashed data only)
              </label>
            </div>
            <Button onClick={submitPrompt} disabled={loading || !prompt.trim()}>{loading ? "Thinking..." : "Ask Assistant"}</Button>
          </div>
        </Card>

        {response ? (
          <Card className="whitespace-pre-wrap text-slate-100">{response}</Card>
        ) : null}
      </div>
    </main>
  );
}

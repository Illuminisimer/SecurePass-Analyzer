'use client';

import { useState, type FormEvent } from "react";
import { Button } from "@/components/Button";
import { FormField } from "@/components/FormField";
import { getAuthHeaders, API_BASE } from "@/lib/api";

interface CreateEntryProps {
  vaultId: number;
  onComplete: () => void;
}

export function CreateEntry({ vaultId, onComplete }: CreateEntryProps) {
  const [title, setTitle] = useState("");
  const [username, setUsername] = useState("");
  const [url, setUrl] = useState("");
  const [password, setPassword] = useState("");
  const [notes, setNotes] = useState("");
  const [masterPassword, setMasterPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setLoading(true);

    const token = localStorage.getItem("securepass_token");
    const response = await fetch(`${API_BASE}/vault/entry`, {
      method: "POST",
      headers: getAuthHeaders(token),
      body: JSON.stringify({
        title,
        username: username || null,
        url: url || null,
        password,
        notes: notes || null,
        master_password: masterPassword,
        vault_id: vaultId,
      }),
    });

    setLoading(false);
    if (!response.ok) {
      const body = await response.json();
      setError(body.detail || "Unable to create entry.");
      return;
    }

    onComplete();
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <FormField label="Title">
        <input
          value={title}
          onChange={(event) => setTitle(event.target.value)}
          required
          className="w-full rounded-3xl border border-slate-800 bg-slate-900/90 px-4 py-3 text-slate-100 outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-500/20"
        />
      </FormField>
      <FormField label="Username">
        <input
          value={username}
          onChange={(event) => setUsername(event.target.value)}
          className="w-full rounded-3xl border border-slate-800 bg-slate-900/90 px-4 py-3 text-slate-100 outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-500/20"
        />
      </FormField>
      <FormField label="URL">
        <input
          type="url"
          value={url}
          onChange={(event) => setUrl(event.target.value)}
          className="w-full rounded-3xl border border-slate-800 bg-slate-900/90 px-4 py-3 text-slate-100 outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-500/20"
        />
      </FormField>
      <FormField label="Password">
        <input
          type="password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
          required
          minLength={8}
          className="w-full rounded-3xl border border-slate-800 bg-slate-900/90 px-4 py-3 text-slate-100 outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-500/20"
        />
      </FormField>
      <FormField label="Notes">
        <textarea
          value={notes}
          onChange={(event) => setNotes(event.target.value)}
          className="w-full rounded-3xl border border-slate-800 bg-slate-900/90 px-4 py-3 text-slate-100 outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-500/20"
        />
      </FormField>
      <FormField label="Master Password">
        <input
          type="password"
          value={masterPassword}
          onChange={(event) => setMasterPassword(event.target.value)}
          required
          minLength={12}
          className="w-full rounded-3xl border border-slate-800 bg-slate-900/90 px-4 py-3 text-slate-100 outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-500/20"
        />
      </FormField>
      {error ? <p className="text-sm text-red-400">{error}</p> : null}
      <Button type="submit" disabled={loading}>{loading ? "Creating..." : "Create Entry"}</Button>
    </form>
  );
}

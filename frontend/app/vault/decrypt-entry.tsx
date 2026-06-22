'use client';

import { useState, type FormEvent } from "react";
import { Button } from "@/components/Button";
import { FormField } from "@/components/FormField";
import { API_BASE, getAuthHeaders } from "@/lib/api";

interface DecryptEntryFormProps {
  entry: { id: number; title: string };
  vaultId: number;
  onResult: (password: string) => void;
}

export function DecryptEntryForm({ entry, vaultId, onResult }: DecryptEntryFormProps) {
  const [masterPassword, setMasterPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setLoading(true);

    const token = localStorage.getItem("securepass_token");
    if (!token) {
      setError("Authentication required.");
      setLoading(false);
      return;
    }

    const response = await fetch(`${API_BASE}/vault/entry/decrypt`, {
      method: "POST",
      headers: getAuthHeaders(token),
      body: JSON.stringify({
        entry_id: entry.id,
        vault_id: vaultId,
        master_password: masterPassword,
      }),
    });

    setLoading(false);
    if (!response.ok) {
      const body = await response.json();
      setError(body.detail || "Unable to decrypt entry.");
      return;
    }

    const data = await response.json();
    onResult(data.password);
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <p className="text-sm text-slate-300">Decrypting: {entry.title}</p>
      </div>
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
      <Button type="submit" disabled={loading}>{loading ? "Decrypting..." : "Decrypt Password"}</Button>
    </form>
  );
}

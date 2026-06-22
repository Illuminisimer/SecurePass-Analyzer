'use client';

import { useState, type FormEvent } from "react";
import { Button } from "@/components/Button";
import { FormField } from "@/components/FormField";
import { API_BASE, getAuthHeaders } from "@/lib/api";

interface CreateVaultFormProps {
  onCreate: () => Promise<void>;
}

export function CreateVaultForm({ onCreate }: CreateVaultFormProps) {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
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

    const response = await fetch(`${API_BASE}/vault/`, {
      method: "POST",
      headers: getAuthHeaders(token),
      body: JSON.stringify({ name, description }),
    });

    setLoading(false);
    if (!response.ok) {
      const body = await response.json();
      setError(body.detail || "Unable to create vault.");
      return;
    }

    await onCreate();
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <FormField label="Vault name">
        <input
          value={name}
          onChange={(event) => setName(event.target.value)}
          required
          className="w-full rounded-3xl border border-slate-800 bg-slate-900/90 px-4 py-3 text-slate-100 outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-500/20"
        />
      </FormField>
      <FormField label="Description">
        <textarea
          value={description}
          onChange={(event) => setDescription(event.target.value)}
          className="w-full rounded-3xl border border-slate-800 bg-slate-900/90 px-4 py-3 text-slate-100 outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-500/20"
        />
      </FormField>
      {error ? <p className="text-sm text-red-400">{error}</p> : null}
      <Button type="submit" disabled={loading}>{loading ? "Creating vault..." : "Create Vault"}</Button>
    </form>
  );
}

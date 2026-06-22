'use client';

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/Button";
import { Card } from "@/components/Card";
import { Modal } from "@/components/Modal";
import { CreateEntry } from "@/app/vault/create-entry";
import { CreateVaultForm } from "@/app/vault/create-vault";
import { DecryptEntryForm } from "@/app/vault/decrypt-entry";
import { getAuthHeaders, API_BASE } from "@/lib/api";

interface VaultItem {
  id: number;
  name: string;
  description: string | null;
  created_at: string;
}

interface EntryItem {
  id: number;
  title: string;
  url: string | null;
  username: string | null;
  strength_score: number;
  breach_status: string;
}

interface DecryptEntryState {
  id: number;
  title: string;
}

export default function VaultPage() {
  const [vaults, setVaults] = useState<VaultItem[]>([]);
  const [selectedVault, setSelectedVault] = useState<VaultItem | null>(null);
  const [entries, setEntries] = useState<EntryItem[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [isCreateVaultOpen, setCreateVaultOpen] = useState(false);
  const [isAddEntryOpen, setAddEntryOpen] = useState(false);
  const [decryptEntry, setDecryptEntry] = useState<DecryptEntryState | null>(null);
  const [decryptedPassword, setDecryptedPassword] = useState<string | null>(null);
  const router = useRouter();

  async function loadVaults() {
    try {
      const token = localStorage.getItem("securepass_token");
      const response = await fetch(`${API_BASE}/vault/`, {
        headers: getAuthHeaders(token),
      });
      if (response.status === 401) {
        localStorage.removeItem("securepass_token");
        router.push("/login");
        return;
      }
      if (!response.ok) throw new Error("Failed to load vaults");
      setVaults(await response.json());
    } catch (err) {
      setError(String(err));
    }
  }

  async function loadEntries(vaultId: number) {
    try {
      const token = localStorage.getItem("securepass_token");
      const response = await fetch(`${API_BASE}/vault/${vaultId}/entries`, {
        headers: getAuthHeaders(token),
      });
      if (response.status === 401) {
        router.push("/login");
        return;
      }
      if (!response.ok) throw new Error("Failed to load entries");
      setEntries(await response.json());
    } catch (err) {
      setError(String(err));
    }
  }

  useEffect(() => {
    const token = localStorage.getItem("securepass_token");
    if (!token) {
      router.push("/login");
      return;
    }

    void loadVaults();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 px-6 py-10">
      <div className="mx-auto flex max-w-6xl flex-col gap-8">
        <div className="rounded-3xl border border-amber-300/10 bg-amber-300/5 p-4 text-amber-200">
          Keep your session token secure. This page requires authentication.
        </div>
        <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div>
            <p className="text-sm uppercase tracking-[0.3em] text-brand-300">Vaults</p>
            <h1 className="text-4xl font-semibold text-white">Your secure vaults</h1>
          </div>
          <div className="flex flex-wrap items-center gap-3">
            <Button variant="secondary" onClick={() => {
              localStorage.removeItem("securepass_token");
              router.push("/login");
            }}>
              Logout
            </Button>
            <Button onClick={() => setCreateVaultOpen(true)}>New vault</Button>
            <Button onClick={() => setAddEntryOpen(true)} disabled={!selectedVault}>
              Add entry
            </Button>
            <Button onClick={() => void loadVaults()}>Refresh</Button>
          </div>
        </div>

        {error ? (
          <Card className="border-red-500 bg-red-950/80 text-red-200">{error}</Card>
        ) : null}

        <div className="grid gap-6 lg:grid-cols-[1.2fr_1fr]">
          <Card>
            <div className="space-y-4">
              {vaults.map((vault) => (
                <button
                  key={vault.id}
                  onClick={() => {
                    setSelectedVault(vault);
                    void loadEntries(vault.id);
                  }}
                  className="w-full rounded-3xl border border-slate-800 bg-slate-900/80 p-5 text-left transition hover:border-brand-400"
                >
                  <h2 className="text-xl font-semibold text-slate-100">{vault.name}</h2>
                  <p className="mt-2 text-sm text-slate-400">{vault.description || "No description"}</p>
                  <span className="mt-3 inline-block text-xs uppercase tracking-[0.2em] text-slate-500">Created {new Date(vault.created_at).toLocaleDateString()}</span>
                </button>
              ))}
            </div>
          </Card>

          <Card>
            <div className="flex items-center justify-between gap-4">
              <div>
                <h2 className="text-2xl font-semibold text-white">Entries</h2>
                {selectedVault ? <p className="text-sm text-slate-400">Vault: {selectedVault.name}</p> : null}
              </div>
            </div>
            {selectedVault ? (
              <div className="mt-6 space-y-4">
                {entries.map((entry) => (
                  <div key={entry.id} className="rounded-3xl border border-slate-800 bg-slate-900/80 p-5">
                    <div className="flex items-start justify-between gap-4">
                      <div>
                        <h3 className="text-xl font-semibold text-slate-100">{entry.title}</h3>
                        <p className="mt-2 text-sm text-slate-400">{entry.username || "No username"}</p>
                        <p className="mt-1 text-sm text-slate-400">{entry.url || "No URL"}</p>
                      </div>
                      <div className="text-right text-sm text-slate-300">
                        <p>Score: {entry.strength_score}</p>
                        <p>Status: {entry.breach_status}</p>
                        <Button variant="secondary" onClick={() => setDecryptEntry({ id: entry.id, title: entry.title })}>
                          Decrypt
                        </Button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="mt-6 text-slate-400">Select a vault to view entries.</p>
            )}
          </Card>
          <Modal open={isCreateVaultOpen} title="Create Vault" onClose={() => setCreateVaultOpen(false)}>
            <CreateVaultForm
              onCreate={async () => {
                setCreateVaultOpen(false);
                await loadVaults();
              }}
            />
          </Modal>
          <Modal open={isAddEntryOpen} title="Add Entry" onClose={() => setAddEntryOpen(false)}>
            {selectedVault ? (
              <CreateEntry
                vaultId={selectedVault.id}
                onComplete={async () => {
                  setAddEntryOpen(false);
                  await loadEntries(selectedVault.id);
                }}
              />
            ) : (
              <p className="text-slate-300">Select a vault before adding an entry.</p>
            )}
          </Modal>
          <Modal open={decryptEntry !== null} title="Decrypt Entry" onClose={() => {
            setDecryptEntry(null);
            setDecryptedPassword(null);
          }}>
            {decryptEntry ? (
              <DecryptEntryForm
                entry={decryptEntry}
                vaultId={selectedVault?.id ?? 0}
                onResult={(password) => setDecryptedPassword(password)}
              />
            ) : null}
            {decryptedPassword ? (
              <div className="mt-4 rounded-3xl border border-emerald-500 bg-emerald-500/10 p-4 text-emerald-200">
                <p className="font-semibold">Decrypted password</p>
                <p className="mt-2 break-all">{decryptedPassword}</p>
              </div>
            ) : null}
          </Modal>
        </div>
      </div>
    </main>
  );
}

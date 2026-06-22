'use client';

import { useEffect, useState, type FormEvent } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/Button";
import { Card } from "@/components/Card";
import { API_BASE } from "@/lib/api";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isRegister, setIsRegister] = useState(false);
  const [confirmPassword, setConfirmPassword] = useState("");
  const [totpCode, setTotpCode] = useState("");
  const [backupCode, setBackupCode] = useState("");

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);

    if (isRegister && password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    const route = isRegister ? "/auth/register" : "/auth/login";
    const response = await fetch(`${API_BASE}${route}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email,
        master_password: password,
        totp_code: totpCode || undefined,
        backup_code: backupCode || undefined,
      }),
    });

    if (!response.ok) {
      const body = await response.json();
      setError(body.detail || "Authentication failed.");
      return;
    }

    const data = await response.json();
    localStorage.setItem("securepass_token", data.access_token);
    router.push("/vault");
  }

  useEffect(() => {
    if (typeof window !== "undefined" && localStorage.getItem("securepass_token")) {
      router.push("/vault");
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 px-6 py-10">
      <div className="mx-auto flex max-w-xl flex-col gap-8">
        <Card>
          <div className="flex items-center justify-between gap-4">
            <div>
              <h1 className="text-3xl font-semibold text-white">Sign in to SecurePass</h1>
              <p className="mt-2 text-slate-400">Use your email and master password to unlock your secure vault.</p>
            </div>
            <Button variant="secondary" onClick={() => setIsRegister((prev) => !prev)}>
              {isRegister ? "Switch to Login" : "Switch to Register"}
            </Button>
          </div>

          <form onSubmit={handleSubmit} className="mt-8 space-y-4">
            <label className="block text-sm text-slate-300">Email</label>
            <input
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              className="w-full rounded-3xl border border-slate-800 bg-slate-900/90 px-4 py-3 text-slate-100 outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-500/20"
              required
            />
            <label className="block text-sm text-slate-300">Master Password</label>
            <input
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              className="w-full rounded-3xl border border-slate-800 bg-slate-900/90 px-4 py-3 text-slate-100 outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-500/20"
              minLength={12}
              required
            />
            <label className="block text-sm text-slate-300">TOTP Code (optional)</label>
            <input
              type="text"
              value={totpCode}
              onChange={(event) => setTotpCode(event.target.value)}
              className="w-full rounded-3xl border border-slate-800 bg-slate-900/90 px-4 py-3 text-slate-100 outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-500/20"
              maxLength={6}
            />
            <label className="block text-sm text-slate-300">Backup Code (optional)</label>
            <input
              type="text"
              value={backupCode}
              onChange={(event) => setBackupCode(event.target.value)}
              className="w-full rounded-3xl border border-slate-800 bg-slate-900/90 px-4 py-3 text-slate-100 outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-500/20"
            />
            {isRegister ? (
              <>
                <label className="block text-sm text-slate-300">Confirm Password</label>
                <input
                  type="password"
                  value={confirmPassword}
                  onChange={(event) => setConfirmPassword(event.target.value)}
                  className="w-full rounded-3xl border border-slate-800 bg-slate-900/90 px-4 py-3 text-slate-100 outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-500/20"
                  minLength={12}
                  required
                />
              </>
            ) : null}
            {error ? <p className="text-sm text-red-400">{error}</p> : null}
            <Button type="submit">{isRegister ? "Create account" : "Sign in"}</Button>
          </form>
        </Card>
      </div>
    </main>
  );
}

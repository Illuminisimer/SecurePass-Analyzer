'use client';

import { useEffect, useState, type FormEvent } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/Button";
import { Card } from "@/components/Card";
import { API_BASE, getAuthHeaders } from "@/lib/api";

export default function TwoFactorPage() {
  const router = useRouter();
  const [secretUri, setSecretUri] = useState<string | null>(null);
  const [qrcodeUri, setQrcodeUri] = useState<string | null>(null);
  const [totpCode, setTotpCode] = useState("");
  const [masterPassword, setMasterPassword] = useState("");
  const [backupCodes, setBackupCodes] = useState<string[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (typeof window !== "undefined" && !localStorage.getItem("securepass_token")) {
      router.push("/login");
    }
  }, [router]);

  async function prepareSetup() {
    const token = localStorage.getItem("securepass_token");
    if (!token) {
      router.push("/login");
      return;
    }

    const response = await fetch(`${API_BASE}/auth/2fa/setup`, {
      method: "POST",
      headers: getAuthHeaders(token),
    });

    if (!response.ok) {
      const body = await response.json();
      setError(body.detail || "Unable to prepare 2FA setup.");
      return;
    }

    const data = await response.json();
    setSecretUri(data.otpauth_url);
    setQrcodeUri(data.qrcode_data_uri);
  }

  async function enableTotp(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);

    const token = localStorage.getItem("securepass_token");
    if (!token) {
      router.push("/login");
      return;
    }

    const response = await fetch(`${API_BASE}/auth/2fa/enable`, {
      method: "POST",
      headers: getAuthHeaders(token),
      body: JSON.stringify({
        master_password: masterPassword,
        totp_code: totpCode,
      }),
    });

    if (!response.ok) {
      const body = await response.json();
      setError(body.detail || "Unable to enable 2FA.");
      return;
    }

    const data = await response.json();
    setBackupCodes(data.backup_codes);
  }

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 px-6 py-10">
      <div className="mx-auto flex max-w-4xl flex-col gap-8">
        <div className="space-y-2">
          <p className="text-sm uppercase tracking-[0.3em] text-brand-300">Two-factor authentication</p>
          <h1 className="text-4xl font-semibold text-white">Secure your account with TOTP</h1>
          <p className="text-slate-400">Set up 2FA to protect your master credentials and generate recovery codes.</p>
        </div>

        <Card>
          <div className="space-y-4">
            <Button variant="secondary" onClick={prepareSetup}>Prepare 2FA Setup</Button>
            {qrcodeUri ? (
              <div className="rounded-3xl border border-slate-800 bg-slate-900/90 p-4">
                <p className="text-slate-300">Scan this QR code with your authenticator app:</p>
                <img src={qrcodeUri} alt="TOTP QR code" className="mt-4 w-full max-w-xs rounded-3xl" />
              </div>
            ) : null}
            <form onSubmit={enableTotp} className="space-y-4">
              <label className="block text-sm text-slate-300">TOTP Code</label>
              <input
                value={totpCode}
                onChange={(event) => setTotpCode(event.target.value)}
                minLength={6}
                maxLength={6}
                className="w-full rounded-3xl border border-slate-800 bg-slate-900/90 px-4 py-3 text-slate-100 outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-500/20"
              />
              {error ? <p className="text-sm text-red-400">{error}</p> : null}
              <Button type="submit">Enable 2FA</Button>
            </form>

            {backupCodes ? (
              <div className="rounded-3xl border border-emerald-500 bg-emerald-500/10 p-4 text-slate-100">
                <p className="font-semibold text-emerald-200">Backup codes</p>
                <ul className="mt-3 space-y-2 text-sm text-slate-200">
                  {backupCodes.map((code) => (
                    <li key={code} className="rounded-2xl bg-slate-950/90 p-3">{code}</li>
                  ))}
                </ul>
              </div>
            ) : null}
          </div>
        </Card>
      </div>
    </main>
  );
}

import "./globals.css";
import Link from "next/link";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "SecurePass Analyzer",
  description: "Enterprise password manager with secure vaults and AI assistance.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <header className="border-b border-slate-800 bg-slate-950/95 backdrop-blur-xl">
          <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-6 py-4">
            <Link href="/" className="text-lg font-semibold text-white">
              SecurePass Analyzer
            </Link>
            <nav className="flex flex-wrap items-center gap-3 text-sm text-slate-300">
              <Link href="/login" className="rounded-full border border-slate-800 bg-slate-900/90 px-4 py-2 transition hover:border-brand-400 hover:text-white">
                Login
              </Link>
              <Link href="/vault" className="rounded-full border border-slate-800 bg-slate-900/90 px-4 py-2 transition hover:border-brand-400 hover:text-white">
                Vault
              </Link>
              <Link href="/assistant" className="rounded-full border border-slate-800 bg-slate-900/90 px-4 py-2 transition hover:border-brand-400 hover:text-white">
                Assistant
              </Link>
              <Link href="/2fa" className="rounded-full border border-slate-800 bg-slate-900/90 px-4 py-2 transition hover:border-brand-400 hover:text-white">
                2FA
              </Link>
            </nav>
          </div>
        </header>
        {children}
      </body>
    </html>
  );
}

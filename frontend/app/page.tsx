import Link from "next/link";
import { ArrowRight, ShieldCheck, Sparkles, Terminal } from "lucide-react";

export default function Home() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-100">
      <div className="mx-auto flex min-h-screen max-w-6xl flex-col gap-12 px-6 py-10">
        <header className="rounded-3xl border border-slate-800 bg-slate-900/90 p-10 shadow-soft backdrop-blur-xl">
          <div className="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
            <div>
              <p className="text-sm uppercase tracking-[0.3em] text-brand-300">SecurePass Analyzer</p>
              <h1 className="mt-4 max-w-2xl text-4xl font-semibold tracking-tight text-slate-50 sm:text-5xl">
                Enterprise password manager with secure vaults, AI guidance, and multi-factor protection.
              </h1>
              <p className="mt-6 max-w-2xl text-lg text-slate-400">
                Built with Next.js, Tailwind CSS, Electron packaging, OpenAI recommendations, and strong backend encryption.
              </p>
            </div>
            <div className="grid gap-4 sm:grid-cols-2">
              <Link href="/vault" className="rounded-3xl bg-brand-500 px-6 py-4 text-center text-base font-semibold text-white shadow-soft transition hover:bg-brand-400">
                Open Vault Dashboard
              </Link>
              <Link href="/assistant" className="rounded-3xl border border-slate-800 px-6 py-4 text-center text-base font-semibold text-slate-100 transition hover:bg-slate-900/80">
                Open AI Assistant
              </Link>
            </div>
          </div>
        </header>

        <section className="grid gap-6 lg:grid-cols-2">
          <article className="rounded-3xl border border-slate-800 bg-slate-900/80 p-8 shadow-soft">
            <div className="flex items-start gap-4 text-brand-300">
              <ShieldCheck className="h-6 w-6" />
              <div>
                <h2 className="text-2xl font-semibold text-slate-50">Secure vault encryption</h2>
                <p className="mt-2 text-slate-400">
                  Master password derived keys protect every entry, while secure SQLite storage protects your credential data at rest.
                </p>
              </div>
            </div>
          </article>
          <article className="rounded-3xl border border-slate-800 bg-slate-900/80 p-8 shadow-soft">
            <div className="flex items-start gap-4 text-brand-300">
              <Sparkles className="h-6 w-6" />
              <div>
                <h2 className="text-2xl font-semibold text-slate-50">AI-powered recommendations</h2>
                <p className="mt-2 text-slate-400">
                  Password strength analysis with local ML fallback and optional OpenAI guidance for secure credential hygiene.
                </p>
              </div>
            </div>
          </article>
        </section>

        <section className="rounded-3xl border border-slate-800 bg-slate-900/80 p-8 shadow-soft">
          <div className="flex items-start gap-4 text-brand-300">
            <Terminal className="h-6 w-6" />
            <div>
              <h2 className="text-2xl font-semibold text-slate-50">What you can do</h2>
              <ul className="mt-4 space-y-3 text-slate-400">
                <li className="flex items-center gap-3">
                  <ArrowRight className="h-4 w-4 text-brand-400" /> Create and manage encrypted vaults.
                </li>
                <li className="flex items-center gap-3">
                  <ArrowRight className="h-4 w-4 text-brand-400" /> Analyze password strength and receive recommendations.
                </li>
                <li className="flex items-center gap-3">
                  <ArrowRight className="h-4 w-4 text-brand-400" /> Enable 2FA and recovery codes for secure login.
                </li>
              </ul>
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}

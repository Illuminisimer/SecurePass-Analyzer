export default function NotFound() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 px-6 py-10">
      <div className="mx-auto max-w-3xl rounded-3xl border border-slate-800 bg-slate-900/90 p-10 text-center">
        <h1 className="text-4xl font-semibold text-white">Page not found</h1>
        <p className="mt-4 text-slate-400">The page you requested does not exist. Use the site navigation to continue.</p>
      </div>
    </main>
  );
}

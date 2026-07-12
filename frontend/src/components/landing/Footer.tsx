export default function Footer() {
  return (
    <footer className="border-t border-zinc-800 py-10">

      <div className="mx-auto flex max-w-6xl items-center justify-between px-8">

        <span className="text-zinc-500">
          © 2026 AI Research Assistant
        </span>

        <span className="text-zinc-500">
          Built with FastAPI • PostgreSQL • Next.js
        </span>

      </div>

    </footer>
  );
}
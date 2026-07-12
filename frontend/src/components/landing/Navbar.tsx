export default function Navbar() {
  return (
    <header className="border-b border-zinc-800">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-8">

        <h1 className="text-xl font-bold">
          AI Research Assistant
        </h1>

        <div className="flex items-center gap-3">

          <button className="rounded-lg px-4 py-2 hover:bg-zinc-800 transition">
            Login
          </button>

          <button className="rounded-lg bg-white px-4 py-2 font-medium text-black hover:bg-zinc-200 transition">
            Sign Up
          </button>

        </div>

      </div>
    </header>
  );
}
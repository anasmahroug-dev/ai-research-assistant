import Link from "next/link"

export default function Hero() {
  return (
    <section className="mx-auto flex max-w-6xl flex-col items-center px-8 py-28 text-center">

      <h1 className="max-w-4xl text-6xl font-bold leading-tight">
        Chat with your research papers.
      </h1>

      <p className="mt-8 max-w-2xl text-lg text-zinc-400">
        Upload PDFs, ask questions in natural language, and receive grounded
        answers with clickable citations powered by Retrieval-Augmented
        Generation.
      </p>

      <div className="mt-12 flex gap-4">

        <button className="rounded-xl bg-white px-6 py-3 font-semibold text-black hover:bg-zinc-200 transition">
          Continue as Guest
        </button>

        <Link href="/login"
        className="rounded-xl border border-zinc-700 px-6 py-3 hover:bg-zinc-900 transition">
          Sign In
        </Link>

      </div>

    </section>
  );
}
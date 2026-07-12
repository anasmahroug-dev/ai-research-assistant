import { FileText, Brain, Search, MessageSquare } from "lucide-react";

export default function Features() {
  return (
    <section className="mx-auto max-w-6xl px-8 py-20">

      <h2 className="mb-12 text-center text-4xl font-bold">
        Features
      </h2>

      <div className="grid gap-6 md:grid-cols-2">

        <Feature
          icon={<FileText />}
          title="Upload PDFs"
          description="Upload research papers and organize them by conversation."
        />

        <Feature
          icon={<Search />}
          title="Semantic Search"
          description="Retrieve the most relevant passages using vector embeddings."
        />

        <Feature
          icon={<MessageSquare />}
          title="Grounded Answers"
          description="Receive answers backed by citations from your documents."
        />

        <Feature
          icon={<Brain />}
          title="AI Assistant"
          description="Ask complex questions in natural language."
        />

      </div>

    </section>
  );
}

function Feature({
  icon,
  title,
  description,
}: {
  icon: React.ReactNode;
  title: string;
  description: string;
}) {
  return (
    <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-6">

      <div className="mb-5 inline-flex rounded-lg bg-zinc-800 p-3">
        {icon}
      </div>

      <h3 className="text-xl font-semibold">
        {title}
      </h3>

      <p className="mt-3 text-zinc-400">
        {description}
      </p>

    </div>
  );
}
import { FileText, ChevronRight, Eye } from "lucide-react";
import ReactMarkdown from "react-markdown";

type Props = {
  content: string;

  onCitationClick: (
    filename: string,
    pages: number[],
    chunkId: number
  ) => void;
};

export default function MessageContent({
  content,
  onCitationClick,
}: Props) {
  const parts = content.split(
    /(\[Source:.*?\])/
  );

  return (
    <div className="whitespace-pre-wrap">
      {parts.map((part, index) => {
        const match = part.match(
          /\[Source:\s*(.*?),\s*Page:\s*([\d,\s]+),\s*Chunk:\s*(\d+)\]/
        );

        if (!match) {
          return (
            <ReactMarkdown key={index}
            components={{
              p: ({ children}) => <span>{children}</span>
            }}>
              {part}
            </ReactMarkdown>
          );
        }

        const filename = match[1];
        const pageString = match[2];
        const chunkId = Number(match[3]);

        const pages = pageString
          .split(",")
          .map((p) => Number(p.trim()));

        return (
          <button
            key={index}
            onClick={() =>
              onCitationClick(filename, pages, chunkId)
            }
            className="
              inline-flex
              items-center
              gap-2
              mx-1
              my-1
              px-3
              py-2
              rounded-full
              border
              border-zinc-700
              bg-zinc-900
              text-zinc-200
              hover:bg-zinc-800
              hover:border-zinc-500
              hover:scale-105
              active:scale-95
              transition-all
              duration-150
              cursor-pointer
            "
          >
            <FileText
              size={15}
              className="text-zinc-400 shrink-0"
            />

            <span className="max-w-44 truncate text-sm font-medium">
              {filename.replace(".pdf", "")}
            </span>

            <span className="text-xs text-zinc-500 whitespace-nowrap">
              {pages.length === 1
                ? `p.${pages[0]}`
                : `pp.${pages.join(", ")}`}
            </span>

            <Eye
              size={13}
              className="text-zinc-500 shrink-0"
            />
          </button>
        );
      })}
    </div>
  );
}
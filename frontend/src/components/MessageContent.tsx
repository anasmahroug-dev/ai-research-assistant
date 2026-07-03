type Props = {
  content: string;

  onCitationClick: (
    filename: string,
    pages: number[]
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
    <div>
      {parts.map((part, index) => {

        const match = part.match(
          /\[Source: (.*?), Pages?: ([\d,\s]+)\]/
        );

        if (!match) {
          return (
            <span key={index}>
              {part}
            </span>
          );
        }

        const filename = match[1];

        const pageString = match[2];

        const pages = pageString
          .split(",")
          .map((p) => Number(p.trim()));

        return (
          <button
            key={index}
            onClick={() =>
              onCitationClick(filename, pages)
            }
            className="text-blue-400 underline"
          >
            {part}
          </button>
        );
      })}
    </div>
  );
}
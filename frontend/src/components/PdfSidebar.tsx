"use client";

import { useState } from "react";

type Props = {
  pdfs: any[];
};

export default function PdfSidebar({pdfs}: Props) {
  const [open, setOpen] = useState(true);

  

  return (
    <div className="flex h-screen">

      {}
      <button
        onClick={() => setOpen(!open)}
        className="h-12 w-12 bg-zinc-800 text-white hover:bg-zinc-700"
      >
        {open ? "→" : "←"}
      </button>

      {}
      <aside
        className={`
          bg-zinc-900 text-white
          transition-all duration-300
          overflow-hidden
          flex flex-col
          ${open ? "w-72 p-4" : "w-0 p-0"}
        `}
      >

        <h2 className="text-xl font-bold mb-4">
          PDFs
        </h2>

        {}
        <div className="flex-1 overflow-y-auto space-y-2 pr-1">

          {pdfs.map((pdf) => (
            <button
              key={pdf.id}
              className="
                w-full
                text-left
                bg-zinc-800
                hover:bg-zinc-700
                p-3
                rounded-lg
                cursor-pointer
                transition
              "
            >
              📄 {pdf.filename}
            </button>
          ))}

        </div>

      </aside>

    </div>
  );
}
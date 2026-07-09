"use client";

import { useState } from "react";
import { ArrowLeft, ArrowRight, FileText, LoaderCircle } from "lucide-react";



type Props = {
  pdfs: any[];
  isUploading: Boolean;
};

export default function PdfSidebar({pdfs, isUploading}: Props) {
  const [open, setOpen] = useState(true);

  return (
    <div className="flex h-screen">

      {}
      <button
        onClick={() => setOpen(!open)}
        className="flex items-center justify-center h-12 w-8 bg-zinc-800 text-white hover:bg-zinc-700"
      >
        {open ? <ArrowRight size={20}/> : <ArrowLeft size={20}/>}
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

          {isUploading && (
            <div
              className="
                flex
                items-center
                gap-3
                w-full
                bg-zinc-800
                p-3
                rounded-lg
                opacity-80
              "
            >
              <FileText size={16} />

              <div className="flex-1">
                <p className="truncate text-sm">
                  Processing PDF...
                </p>

                <p className="text-xs text-zinc-400">
                  Chunking & generating embeddings
                </p>
              </div>

              <LoaderCircle
                size={18}
                className="animate-spin text-zinc-300"
              />
            </div>
          )}

          {pdfs.map((pdf) => (
            <button

              key={pdf.id}

              onClick={() => {
                window.open(`http://localhost:8000/uploads/${pdf.filename}`,
                  "_blank"
                );
              }}

              className="
                flex
                items-center
                gap-2
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
              <FileText size={16}/> <span className="truncate">{pdf.filename}</span>
            </button>
          ))}

        </div>

      </aside>

    </div>
  );
}
"use client";

import { useState } from "react";
import { ArrowLeft, ArrowRight, FileText } from "lucide-react";



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
              <FileText size={16}/> {pdf.filename}
            </button>
          ))}

        </div>

      </aside>

    </div>
  );
}
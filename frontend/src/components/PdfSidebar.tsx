"use client";
import { API_URL } from "@/lib/api";
import { useState } from "react";
import {
  ArrowLeft,
  ArrowRight,
  FileText,
  LoaderCircle,
  Trash2,
} from "lucide-react";
import ConfirmDialog from "./ConfirmDialog"

type Props = {
  pdfs: any[];
  isUploading: boolean;
  onDeletePdf: (id: number) => void;
};

export default function PdfSidebar({
  pdfs,
  isUploading,
  onDeletePdf,
}: Props) {
  const [open, setOpen] = useState(true);
  const [pdfToDelete, setPdfToDelete] = useState<any>(null);

  return (
    <>
      <div className="flex h-screen">

        <button
          onClick={() => setOpen(!open)}
          className="flex items-center justify-center h-12 w-8 bg-zinc-800 text-white hover:bg-zinc-700"
        >
          {open ? (
            <ArrowRight size={20} />
          ) : (
            <ArrowLeft size={20} />
          )}
        </button>

        <aside
          className={`
            bg-zinc-900
            text-white
            transition-all
            duration-300
            overflow-hidden
            flex
            flex-col
            ${open ? "w-72 p-4" : "w-0 p-0"}
          `}
        >
          <h2 className="text-xl font-bold mb-4">
            PDFs
          </h2>

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
              <div
                key={pdf.id}
                className="
                  group
                  flex
                  items-center
                  justify-between
                  bg-zinc-800
                  hover:bg-zinc-700
                  p-3
                  rounded-lg
                  transition
                "
              >
                <div
                  className="
                    flex
                    items-center
                    gap-2
                    flex-1
                    cursor-pointer
                    overflow-hidden
                  "
                  onClick={() => {
                    window.open(pdf.cloudinary_url, "_blank");
                  }}
                >
                  <FileText size={16} />

                  <span className="truncate">
                    {pdf.filename}
                  </span>
                </div>

                <div
                  className="
                    hidden
                    group-hover:flex
                    items-center
                    ml-2
                  "
                >
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      setPdfToDelete(pdf);
                    }}
                    className="
                      p-1
                      rounded
                      hover:bg-zinc-600
                    "
                  >
                    <Trash2 size={16} />
                  </button>
                </div>
              </div>
            ))}

          </div>
        </aside>
      </div>
            <ConfirmDialog
          open={pdfToDelete !== null}
          title="Delete PDF?"
          message="Are you sure you want to permanently delete"
          itemName={pdfToDelete?.filename}
          onCancel={() => setPdfToDelete(null)}
          onConfirm={() => {
            onDeletePdf(pdfToDelete.id);
            setPdfToDelete(null);
          }}
        />
      
    </>
  );
}
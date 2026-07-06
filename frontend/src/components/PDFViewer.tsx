"use client";

import { Document, Page, pdfjs } from "react-pdf";
import "react-pdf/dist/Page/TextLayer.css";
import "react-pdf/dist/Page/AnnotationLayer.css";

import {X} from "lucide-react";
import {useRef} from "react";

pdfjs.GlobalWorkerOptions.workerSrc =
  new URL(
    "pdfjs-dist/build/pdf.worker.min.mjs",
    import.meta.url
  ).toString();

type Props = {
    fileUrl: string;
    pages: number[];
    highlightWords: string[];
    onClose: () => void;
};

function escapeRegExp(text: string){
  return text.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

export default function PDFViewer({fileUrl, pages, highlightWords, onClose}: Props) {
  const pageRefs = useRef(new Map<number, HTMLDivElement>());
    return (

      

  <div
    className="
    w-[640px]
    h-full
    bg-zinc-900
    flex
    justify-center
    items-start
    p-6
    relative
    flex-shrink-0
    "
  >

    <button
      onClick={onClose}
      className="
      absolute
      top-4
      right-4
      z-50
      bg-zinc-800
      hover:bg-zinc-700
      p-2
      rounded-full
      "
    >
      <X size={20} className="text-white" />
    </button>

    <div
      className="
      h-full
      overflow-auto
      pr-2
      "
    >

      <Document file={fileUrl}>

        <div className="flex flex-col gap-4">

          {pages.map((page) => (

            <div
              key={page}
              ref={(e1)=> {
                if (e1) {
                  pageRefs.current.set(page, e1);
                }
              }}
              className="
              shadow-2xl
              rounded-lg
              overflow-hidden
              "
            >

              <Page
                pageNumber={page}
                width={600}
                customTextRenderer={({str})=>{
                  let result = str;
                  
                  highlightWords.forEach(word => {

                    const regex = new RegExp(`(${escapeRegExp(word)})`, "gi");

                    result = result.replace(
                      regex,
                      `<mark style="background:yellow">$1</mark>`
                    );



                  });

                  
                  return result;


                }}
              />

            </div>

          ))}

        </div>

      </Document>

    </div>

  </div>

);

}
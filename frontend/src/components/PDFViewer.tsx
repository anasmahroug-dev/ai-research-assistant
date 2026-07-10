"use client";

import { Document, Page, pdfjs } from "react-pdf";
import "react-pdf/dist/Page/TextLayer.css";
import "react-pdf/dist/Page/AnnotationLayer.css";
import { PDFPageProxy } from "pdfjs-dist";

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
    highlightChunk: string;
    onClose: () => void;
};

function escapeRegExp(text: string){
  return text.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function normalize(text: string){
  return text
    .toLowerCase()
    .replace(/[^\p{L}\p{N}\s]/gu, " ")
    .replace(/\s+/g, " ")
    .trim();

}



export default function PDFViewer({fileUrl, pages, highlightChunk, onClose}: Props) {
  const pageRefs = useRef(new Map<number, HTMLDivElement>());
  function handlePageLoaded(textLayer: HTMLDivElement){

    const pageText = textLayer.innerText;
    
    const chunkWords = normalize(highlightChunk).split(" ").filter(Boolean);

    const spans = Array.from(textLayer.querySelectorAll("span"));

    const spanWords: string[] = [];
    const wordToSpan: number[] = [];

    spans.forEach((span, spanIndex) =>{
      const words = normalize(span.textContent ?? "")
      .split(" ")
      .filter(Boolean);

      for (const word of words){
        spanWords.push(word);
        wordToSpan.push(spanIndex);
      }
    });

    const pageWords = spanWords;

    let bestIndex = 0;
    let bestScore = -1;

    for(
      let start = 0;
      start <= pageWords.length - chunkWords.length;
      start++
    ) {
      let score = 0;

      for(let i = 0; i< chunkWords.length; i++){
        if (pageWords[start + i]=== chunkWords[i]){
          score++;
        }
      }
      if (score > bestScore){
        bestScore = score;
        bestIndex = start;
      }

    }

    const startSpan = wordToSpan[bestIndex];
    const endSpan = wordToSpan[
      bestIndex + chunkWords.length - 1
    ];


    spans.forEach((span) => {
    span.style.background = "";
    span.style.color = "";
    });
    for(let i = startSpan; i<= endSpan; i++){
      spans[i].style.background = "yellow";
      spans[i].style.color = "black";
    }

  }  
  
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
                onRenderTextLayerSuccess={() => {
                  const container = pageRefs.current.get(page);

                  if (!container) return;

                  const textLayer =
                      container.querySelector(".react-pdf__Page__textContent");

                  if (!(textLayer instanceof HTMLDivElement)) return;

                  handlePageLoaded(textLayer);
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
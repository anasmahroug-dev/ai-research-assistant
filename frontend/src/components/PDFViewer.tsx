"use client";

import { Document, Page, pdfjs } from "react-pdf";
import "react-pdf/dist/Page/TextLayer.css";
import "react-pdf/dist/Page/AnnotationLayer.css";

pdfjs.GlobalWorkerOptions.workerSrc =
  new URL(
    "pdfjs-dist/build/pdf.worker.min.mjs",
    import.meta.url
  ).toString();

type Props = {
    fileUrl: string;
    pageNumber: number;
};

export default function PDFViewer({fileUrl, pageNumber}: Props) {
    return (

        <div className="
        w-full 
        h-full 
        overflow-auto 
        bg-zinc-900
        flex
        justify-center
        items-start
        p-6
        ">

            <Document file={fileUrl}>
               <div className="shadow-2xl  drop-shadow-2xl rounded-lg overflow-hidden">
                <Page pageNumber={pageNumber} 
                width={750} />
                </div>
            </Document>

        </div>

    );

}
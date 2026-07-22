export type PdfStatus =
  | "processing"
  | "ready"
  | "failed";

export interface PDF {
    id: number;
    filename: string;
    cloudinary_url: string;
    status: PdfStatus;
}
from enum import Enum

class PdfStatus(str, Enum):
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"
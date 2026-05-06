from pathlib import Path
import fitz  # pymupdf
from docx import Document

SUPPORTED_EXTENSIONS = {".sol", ".txt", ".pdf", ".docx"}

def load_contract_from_string(text: str) -> str:
    cleaned = text.strip()
    if not cleaned:
        raise ValueError("Contract text is empty.")
    return cleaned

def load_contract_from_file(file_path: str) -> str:
    path = Path(file_path)
    ext = path.suffix.lower()
    if ext == ".pdf":
        return _read_pdf(path)
    elif ext == ".docx":
        return _read_docx(path)
    else:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

def _read_pdf(path: Path) -> str:
    doc = fitz.open(str(path))
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    if not text.strip():
        raise ValueError("PDF appears to be empty or scanned.")
    return text.strip()

def _read_docx(path: Path) -> str:
    doc = Document(str(path))
    text = "\n".join([para.text for para in doc.paragraphs])
    if not text.strip():
        raise ValueError("Word document appears to be empty.")
    return text.strip()
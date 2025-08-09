import os
from typing import Literal

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

try:
    import docx
except ImportError:
    docx = None


def _extract_from_pdf(file_path: str) -> str:
    if not PyPDF2:
        raise ImportError("PyPDF2 is required for PDF extraction. Install with `pip install PyPDF2`.")
    text = []
    with open(file_path, "rb") as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        for page in reader.pages:
            text.append(page.extract_text() or "")
    return "\n".join(text).strip()


def _extract_from_docx(file_path: str) -> str:
    if not docx:
        raise ImportError("python-docx is required for DOCX extraction. Install with `pip install python-docx`.")
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs]).strip()


def _extract_from_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as txt_file:
        return txt_file.read().strip()


def extract_text(
    input_source: str,
    source_type: Literal["text", "pdf", "docx", "txt"]
) -> str:
    """
    Extracts plain text from a given input source.

    Args:
        input_source (str): Either a raw text string or a file path depending on `source_type`.
        source_type (Literal): One of "text", "pdf", "docx", or "txt".

    Returns:
        str: Extracted text content.
    """
    if source_type == "text":
        return input_source.strip()

    if not os.path.isfile(input_source):
        raise FileNotFoundError(f"File not found: {input_source}")

    if source_type == "pdf":
        return _extract_from_pdf(input_source)

    elif source_type == "docx":
        return _extract_from_docx(input_source)

    elif source_type == "txt":
        return _extract_from_txt(input_source)

    else:
        raise ValueError(f"Unsupported source_type: {source_type}")

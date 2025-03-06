import fitz
import re
import io



def extract_text_from_pdf(pdf_file):
    """Extracts and processes text from a PDF file object."""
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""

    for page in doc:
        text += page.get_text("text") + " "  # Extract text with spaces

    # Fix encoding issues
    text = text.replace("\xa0", " ")  # Replace non-breaking spaces

    # Remove hyphenation at line breaks (e.g., "interfere-\nnce" → "interference")
    text = re.sub(r"(\w+)-\n(\w+)", r"\1\2", text)

    # Fix words split by newlines (e.g., "interfere\nnce" → "interference")
    text = re.sub(r"(\w+)\n(\w+)", r"\1\2", text)

    # Properly split sentences
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())


    return [s.strip() for s in sentences if s.strip()]


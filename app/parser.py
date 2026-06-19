import PyPDF2

def extract_text_from_pdf(file_path):
    """Extract raw text from a PDF file."""
    text = ""
    try:
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        raise ValueError(f"Could not read PDF: {str(e)}")

    if not text.strip():
        raise ValueError("No readable text found in PDF. It may be a scanned image.")

    return text.strip()
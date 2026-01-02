import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF using PyMuPDF.
    Returns clean text as a string.
    """

    text = ""

    try:
        doc = fitz.open(pdf_path)

        for page in doc:
            page_text = page.get_text()
            text += page_text + "\n"

        doc.close()

    except Exception as e:
        print("Error extracting text:", e)
        return ""

    # Clean text (remove too many spaces/newlines)
    text = text.replace("\t", " ")
    text = " ".join(text.split())

    return text.lower()  # Return lowercase for easy matching

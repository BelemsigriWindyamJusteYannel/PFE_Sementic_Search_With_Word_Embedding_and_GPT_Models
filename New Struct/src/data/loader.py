import fitz  # PyMuPDF

def text_extract_from(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()  # Extract text from each page
    doc.close()
    text = text.encode('utf-8').decode('utf-8')
    return text


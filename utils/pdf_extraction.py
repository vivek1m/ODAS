from pypdf import PdfReader


def extract_from_pdf(file):
    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        text += page.extract_text()
    return text
def extract_from_pdfs(files):
    text = ""

    for i in range(len(files)):
        text += f"Document {i}"
        for page in PdfReader(files[i]).pages:
            text += page.extract_text()
    return text
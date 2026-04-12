from PyPDF2 import PdfReader


def parse_resume(file):
    text = ""

    reader = PdfReader(file)

    for page in reader.pages:
        text += page.extract_text()

    return text
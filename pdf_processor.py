from pypdf import PdfReader


def read_pdf(pdf_path):
    """
    Read PDF and return page number + text
    """

    reader = PdfReader(pdf_path)

    pages = []

    for page_num, page in enumerate(reader.pages):

        text = page.extract_text()

        if text:
            pages.append(
                {
                    "page": page_num + 1,
                    "text": text
                }
            )

    return pages


def chunk_text(text, chunk_size=500):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunks.append(text[start:end])

        start += chunk_size

    return chunks
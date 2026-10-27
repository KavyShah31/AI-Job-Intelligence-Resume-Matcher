from pathlib import Path

import fitz 

def extract_text_from_pdf(pdf_file):
    """
    Extract selectable text from a PDF path or uploaded PDF.
    """
    document = None

    try:
        if isinstance(pdf_file,(str,Path)):
            document = fitz.open(str(pdf_file))
        else:
            document = fitz.open(
                stream=pdf_file.getvalue(),
                filetype="pdf",
            )

        pages = [
            page.get_text("text")
            for page in document
        ]

        text =  "\n".join(pages).strip()

        if not text:
            raise ValueError(
                "No readable text found. This ma be a scanned PDF."
            )

        return text

    except Exception as error:
        raise ValueError(
            f"Unable to read PDF: {error}"
        ) from error

    finally:
        if document is not None:
            document.close()
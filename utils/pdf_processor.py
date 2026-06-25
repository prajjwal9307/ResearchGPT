import fitz
import os


def save_uploaded_file(uploaded_file):

    os.makedirs("data", exist_ok=True)

    file_path = os.path.join(
        "data",
        uploaded_file.name
    )

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path


def extract_text_from_pdf(
        pdf_path,
        file_name
):

    pages = []

    doc = fitz.open(pdf_path)

    for page_num, page in enumerate(doc):

        text = page.get_text()

        if text.strip():

            pages.append(
                {
                    "text": text,
                    "page_number": page_num + 1,
                    "file_name": file_name
                }
            )

    doc.close()

    return pages
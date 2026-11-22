
from pathlib import Path
from email import policy
from email.parser import BytesParser
from docx import Document
import re
import json


# Get the main project directory
BASE_DIR = Path(__file__).resolve().parent.parent

DOCUMENTS_DIR = BASE_DIR / "documents"
PROCESSED_DIR = BASE_DIR / "processed_documents"


def clean_text(text):
    """
    Remove unnecessary spaces and blank lines
    while preserving paragraph separation.
    """

    text = text.replace("\r\n", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def convert_email_to_text(email_path):
    """
    Read an EML file and convert its contents
    into a normal text document.
    """

    with open(email_path, "rb") as file:
        message = BytesParser(
            policy=policy.default
        ).parse(file)

    subject = message.get("subject", "")
    sender = message.get("from", "")
    date = message.get("date", "")

    # Prefer the plain-text email body
    email_body = message.get_body(
        preferencelist=("plain",)
    )

    if email_body:
        body = email_body.get_content()

    else:
        # Fallback for HTML-only emails
        html_body = message.get_body(
            preferencelist=("html",)
        )

        body = html_body.get_content() if html_body else ""

        body = re.sub(
            r"<[^>]+>",
            " ",
            body
        )

    # Combine email details and body
    complete_text = f"""
Subject: {subject}

From: {sender}

Date: {date}

{body}
"""

    return clean_text(complete_text)


def extract_docx_text(docx_path):
    """
    Extract text from Word document paragraphs
    and tables.
    """

    document = Document(docx_path)

    extracted_content = []

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            extracted_content.append(
                paragraph.text
            )

    # Extract table content
    for table in document.tables:

        for row in table.rows:

            row_content = [
                cell.text.strip()
                for cell in row.cells
            ]

            extracted_content.append(
                " | ".join(row_content)
            )

    return clean_text(
        "\n".join(extracted_content)
    )


def process_documents():
    """
    Process all four knowledge-base documents.
    """

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    all_documents = []

    # 1. Process Word documents
    docx_files = list(
        DOCUMENTS_DIR.glob("*.docx")
    )

    for file_path in docx_files:

        text = extract_docx_text(file_path)

        all_documents.append({
            "source": file_path.name,
            "file_type": "DOCX",
            "content": text
        })

        print(f"Processed: {file_path.name}")

    # 2. Process email documents
    email_files = list(
        DOCUMENTS_DIR.glob("*.eml")
    )

    for file_path in email_files:

        text = convert_email_to_text(
            file_path
        )

        # Save the converted email as TXT
        output_path = (
            PROCESSED_DIR /
            "five_day_work_week.txt"
        )

        output_path.write_text(
            text,
            encoding="utf-8"
        )

        all_documents.append({
            "source": file_path.name,
            "file_type": "EML",
            "content": text
        })

        print(f"Converted: {file_path.name}")

    # Verify that all four sources were found
    if len(all_documents) != 4:

        raise ValueError(
            f"Expected 4 documents, "
            f"but found {len(all_documents)}. "
            f"Check your documents folder."
        )

    # Save extracted text and source metadata
    output_json = (
        PROCESSED_DIR /
        "extracted_documents.json"
    )

    with open(
        output_json,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            all_documents,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\nAll four documents processed successfully!")

    return all_documents


if __name__ == "__main__":

    documents = process_documents()

    print("\nDOCUMENT EXTRACTION SUMMARY")

    for document in documents:

        print(
            f"\nSource: {document['source']}"
        )

        print(
            f"Type: {document['file_type']}"
        )

        print(
            f"Characters extracted: "
            f"{len(document['content'])}"
        )

        print(
            f"Preview: "
            f"{document['content'][:200]}"
        )

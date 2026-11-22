
import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "processed_documents" / "extracted_documents.json"
OUTPUT_FILE = BASE_DIR / "processed_documents" / "chunks.json"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150


def split_long_paragraph(paragraph):
    """
    Split a long paragraph into smaller pieces.
    Try to preserve complete sentences.
    """

    sentences = re.split(r'(?<=[.!?])\s+', paragraph.strip())

    pieces = []
    current = ""

    for sentence in sentences:

        if len(sentence) > CHUNK_SIZE:

            if current:
                pieces.append(current)
                current = ""

            words = sentence.split()
            word_chunk = ""

            for word in words:

                if len(word_chunk) + len(word) + 1 <= CHUNK_SIZE:
                    word_chunk = (word_chunk + " " + word).strip()

                else:
                    if word_chunk:
                        pieces.append(word_chunk)

                    word_chunk = word

            if word_chunk:
                pieces.append(word_chunk)

        elif len(current) + len(sentence) + 1 <= CHUNK_SIZE:

            current = (current + " " + sentence).strip()

        else:

            if current:
                pieces.append(current)

            current = sentence

    if current:
        pieces.append(current)

    return pieces


def split_text(text):
    """
    Split text using paragraph boundaries instead of
    cutting the document at arbitrary character positions.
    """

    chunks = []

    # Identify paragraphs using blank lines
    paragraphs = re.split(r'\n\s*\n', text.strip())

    units = []

    for paragraph in paragraphs:

        paragraph = paragraph.strip()

        if not paragraph:
            continue

        # Keep normal paragraphs together
        if len(paragraph) <= CHUNK_SIZE:
            units.append(paragraph)

        else:
            # Split only paragraphs that are too large
            units.extend(split_long_paragraph(paragraph))

    current_chunk = []

    for unit in units:

        candidate = "\n\n".join(current_chunk + [unit])

        if len(candidate) <= CHUNK_SIZE:
            current_chunk.append(unit)

        else:

            # Save the current chunk
            if current_chunk:
                chunks.append("\n\n".join(current_chunk))

            # Preserve a small overlap from the previous chunk
            overlap_units = []
            overlap_length = 0

            for previous_unit in reversed(current_chunk):

                if overlap_length + len(previous_unit) > CHUNK_OVERLAP:
                    break

                overlap_units.insert(0, previous_unit)
                overlap_length += len(previous_unit)

            current_chunk = overlap_units

            # Add the new paragraph
            if len("\n\n".join(current_chunk + [unit])) <= CHUNK_SIZE:
                current_chunk.append(unit)
            else:
                current_chunk = [unit]

    # Save the final chunk
    if current_chunk:
        chunks.append("\n\n".join(current_chunk))

    return chunks


def create_chunks():

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        documents = json.load(file)

    all_chunks = []

    for document in documents:

        text_chunks = split_text(document["content"])

        for index, chunk in enumerate(text_chunks):

            all_chunks.append({
                "chunk_id": f"{document['source']}_{index}",
                "source": document["source"],
                "content": chunk
            })

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(
            all_chunks,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("Paragraph-aware text splitting completed!")
    print("Total documents:", len(documents))
    print("Total chunks:", len(all_chunks))

    for document in documents:
        document_chunks = [
            chunk for chunk in all_chunks
            if chunk["source"] == document["source"]
        ]

        print(
            f"{document['source']}: "
            f"{len(document_chunks)} chunks"
        )

    return all_chunks


if __name__ == "__main__":
    create_chunks()


import os
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai

from src.logger import log_interaction
from src.retriever import retrieve_documents


# Step 1: Get project directory
BASE_DIR = Path(__file__).resolve().parent.parent


# Step 2: Load environment variables
load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("GEMINI_API_KEY")
model_name = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from .env")


# Step 3: Create Gemini client
client = genai.Client(
    api_key=api_key,
    http_options={"timeout": 60000}
)


def generate_answer(question):

    # Step 4: Retrieve relevant HR information
    print("1. Starting document retrieval...")

    retrieved_chunks = retrieve_documents(question, top_k=5)

    print("2. Document retrieval completed!")
    print("Retrieved chunks:", len(retrieved_chunks))

    # Step 5: Check whether documents were found
    if not retrieved_chunks:
        answer = (
            "I couldn't find relevant information in the "
            "available HR documents. Please contact HR or "
            "your BU HR team for clarification."
        )

        log_interaction(question, retrieved_chunks, answer)
        return answer

    # Step 6: Combine retrieved document chunks
    context = "\n\n".join(
        f"Source: {chunk['source']}\n"
        f"Information: {chunk['content']}"
        for chunk in retrieved_chunks
    )

    # Step 7: Create prompt
    prompt = f"""
You are an HR Policy Assistant.

Your responsibility is to answer employee questions
accurately using the supplied HR documents.

IMPORTANT RULES:

1. Use ONLY the information provided in the HR document context.
2. Never invent, assume, or guess company policies.
3. Read all the retrieved information before answering.
4. Combine relevant information from multiple chunks
   when necessary to provide a complete answer.
5. For procedural questions, provide clear numbered steps
   in the correct sequence.
6. Include important eligibility requirements, conditions,
   limitations, and deadlines when they are relevant.
7. Mention the original source document at the end.
8. If the requested information is not available in the
   supplied context, clearly say that it is not covered
   in the available HR documents.
9. When information is unavailable, politely direct the
   employee to HR or BU HR.
10. Do not claim that a procedure or policy is unavailable
    if the supplied context actually contains that information.

HR DOCUMENT CONTEXT:

{context}

EMPLOYEE QUESTION:

{question}

Provide a clear, accurate and employee-friendly answer.
"""

    # Step 8: Send request to Gemini
    print("3. Sending request to Gemini...")

    for attempt in range(2):

        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )

            print("4. Gemini response received!")

            answer = response.text

            # Check for empty response
            if not answer:
                answer = (
                    "Sorry, I couldn't generate an answer. "
                    "Please try asking your question again."
                )

            # Step 9: Log successful interaction
            log_interaction(question, retrieved_chunks, answer)

            return answer

        except Exception as e:

            error_message = str(e).upper()

            print("Gemini API Error:", str(e))

            temporary_errors = [
                "503",
                "504",
                "429",
                "UNAVAILABLE",
                "DEADLINE_EXCEEDED",
                "RESOURCE_EXHAUSTED",
                "INTERNAL"
            ]

            is_temporary = any(
                error in error_message
                for error in temporary_errors
            )

            # Retry only temporary errors
            if is_temporary and attempt == 0:

                print(
                    "Gemini is temporarily unavailable. "
                    "Retrying once after 2 seconds..."
                )

                time.sleep(2)
                continue

            # Friendly error message
            answer = (
                "Sorry, the HR assistant is temporarily unable "
                "to generate a response. Please try again shortly."
            )

            # Log failed interaction too
            log_interaction(question, retrieved_chunks, answer)

            print("Gemini request failed.")

            return answer


# Step 10: Run directly from terminal
if __name__ == "__main__":

    question = input("Enter your HR question: ")

    answer = generate_answer(question)

    print("\nHR CHATBOT ANSWER\n")
    print(answer)

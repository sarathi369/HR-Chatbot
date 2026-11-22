
import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("GEMINI_API_KEY")
model_name = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

client = genai.Client(
    api_key=api_key,
    http_options={"timeout": 120000}
)

print("Testing Gemini connection...")

try:
    response = client.models.generate_content(
        model=model_name,
        contents="Reply with only: Gemini connection successful."
    )

    print("\nSUCCESS!")
    print(response.text)

except Exception as e:
    print("\nGEMINI API ERROR:")
    print(e)

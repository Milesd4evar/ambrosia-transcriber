import os
from gemini_pipeline import transcribe_file_with_gemini

path = input("Enter path to PDF or PNG/JPG: ").strip()
api_key = os.environ.get("GEMINI_API_KEY")

results = transcribe_file_with_gemini(path, api_key)

for page_num, text in results:
    print(f"\n===== PAGE {page_num} =====\n")
    print(text)
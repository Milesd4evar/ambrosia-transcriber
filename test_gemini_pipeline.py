from gemini_pipeline import run_gemini_transcribe

api_key = input("Enter GEMINI_API_KEY: ").strip()
image_path = input("Enter path to PNG/JPG image: ").strip()

output = run_gemini_transcribe(image_path, api_key)

print("\n===== GEMINI OUTPUT =====\n")
print(output)
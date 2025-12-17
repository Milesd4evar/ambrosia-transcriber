# gemini_pipeline.py
import os
from google import genai
from google.genai import types
from pdf2image import convert_from_path
from pathlib import Path

def pdf_to_pngs(pdf_path: str, dpi: int = 150) -> list[str]:
    """
    Convert a PDF into one PNG per page.
    Returns a list of image paths in order: [page1.png, page2.png, ...]
    """
    pdf = Path(pdf_path)
    out_dir = pdf.parent / (pdf.stem + "_pages")
    out_dir.mkdir(exist_ok=True)

    # render all pages
    pages = convert_from_path(str(pdf), dpi=dpi)

    image_paths: list[str] = []
    for i, page in enumerate(pages, start=1):
        img_path = out_dir / f"{pdf.stem}_p{i}.png"
        page.save(img_path, "PNG")
        image_paths.append(str(img_path))

    return image_paths

def run_gemini_transcribe(image_path: str, api_key: str) -> str:
    """
    image_path: path to a JPG/PNG screenshot
    api_key: your GEMINI_API_KEY
    returns: transcription text output from Gemini
    """
    
    # configure client
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


    # load image bytes
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    # prompt can be changed but generally gemini likes concise prompts
    prompt = """
You are a literal transcription assistant for a single handwritten page
by Alice Ambrose (early 20th c., philosophy/mathematics).

Your job: transcribe exactly what you see, line by line, without “fixing”
the English, and mark any uncertainty explicitly.

RULES:

1. LINE FORMAT
- For each visible main line of text, output exactly one line:
  L1: ...
  L2: ...
  L3: ...
- Keep the same line order and approximate breaks as on the page.
- If a word is split with a hyphen at the end of a line, keep the split.

2. FIDELITY
- Do NOT add, remove, or rewrite words.
- Do NOT “clean up” grammar or punctuation.
- Transcribe abbreviations exactly as written (e.g. “Witt.”, “symb.”, “no.”).

3. UNCERTAIN READINGS
- If a word or phrase is hard to read, never guess silently.
- Instead, write your best reading inside:
  [unclear: your best guess]
- You may include multiple options, e.g. [unclear: law / low].

4. CROSSED-OUT TEXT
- If text is visibly struck out, transcribe it as:
  [crossed out: original text]

5. INSERTS VS MARGIN NOTES
- Text written between two lines and linked to a caret (^) in a line below
  is an insertion. Place it at the caret position and wrap it as:
  [inserted above: inserted text]
- Text clearly off to the side as a separate note is a margin note. Put it
  on its own numbered line as:
  L#: [margin: note text]
- If you’re unsure whether something between lines is a margin note or an
  insertion, treat it as [inserted above: ...] and use [unclear: ...] inside.

6. SYMBOLS, NUMBERS, LANGUAGES
- Copy mathematical / logical symbols literally: arrows “->”, 0, x, +, ~, v, etc.
- If you are unsure whether a mark is 0 vs O, or similar, use [unclear: 0 / O].
- Do NOT translate or normalize foreign words (e.g. random French); transcribe
  them as written and use [unclear: ...] if needed.

OUTPUT:
- Only output the numbered transcription lines:
  L1: ...
  L2: ...
  L3: ...
- No explanations or extra commentary.
"""

    # call Gemini
    response = client.models.generate_content(
        model="gemini-3-pro-preview",   # or whatever exact model ID you prefer
        contents=[
            types.Part(text=prompt),
            types.Part(
                inline_data=types.Blob(
                    mime_type="image/png",   # change to "image/png" if PNG
                    data=image_bytes,
                )
            ),
        ],
        # optional:
        # config={"thinking_level": "high"}
    )

    # extract output
    try:
        return response.text
    except:
        # some outputs are nested
        return response.candidates[0].content[0].text

def transcribe_file_with_gemini(path: str,api_key: str) -> list[tuple[int, str]]:
    """
    path: PDF or PNG/JPG.
    returns: list of (page_number, transcription_text)
    """
    p = Path(path)
    suffix = p.suffix.lower()

    if suffix == ".pdf":
        image_paths = pdf_to_pngs(str(p))
    elif suffix in [".png", ".jpg", ".jpeg"]:
        image_paths = [str(p)]
    else:
        raise ValueError("Unsupported file type. Use PDF, PNG, or JPG.")

    results: list[tuple[int, str]] = []
    for page_num, img_path in enumerate(image_paths, start=1):
        print(f"Transcribing page {page_num} from {img_path} ...")
        text = run_gemini_transcribe(img_path, api_key)
        results.append((page_num, text))

    return results
from openai import OpenAI
client = OpenAI()

print("beginning transcription, expect 3-5 minutes")

file = client.files.create(
    file=open("/Users/milesdusett/Desktop/ambrosestuff.pdf", "rb"),
    purpose="user_data"
)


response = client.responses.create(
    model="gpt-5.1",
    input=[
        {
            "role": "user",
            "content": [
                {
                    "type": "input_file",
                    "file_id": file.id,
                },
                {
                    "type": "input_text",
                    "text": """You are a precise transcription assistant for early 20th century handwritten
mathematical/philosophical documents by Alice Ambrose.

Your top priority is to be HONEST about uncertainty. A wrong “clean” word is
much worse than an [unclear: ...] tag. Overusing [unclear: ...] is acceptable;
failing to mark an uncertain word is a serious mistake.

TRANSCRIPTION RULES:
1. Transcribe every word you see — do not skip or omit any text.
2. For unclear words: use [unclear: your best guess]. If you are not at least
   ~95% sure of the letters, you should use [unclear: ...] rather than committing
   to a single reading.
3. For crossed-out text: use [crossed out: original text].
4. For margin notes: use [margin: text content].
5. For unclear symbols: use [unclear symbol: description].
6. Maintain original line breaks and layout STRICTLY:
   - Each physical line of the main text becomes exactly one line in your output.
   - Do NOT merge two manuscript lines into one output line.
   - Do NOT arbitrarily break a manuscript line into multiple output lines.
   - If a word is hyphenated at the line end (e.g. “re-” / “sult”), keep the
     hyphenation and line break exactly as written.
7. Margin notes must appear on their own lines in the output, starting with
   [margin: ...], not mixed inline with the main text line.
8. Use [red square] and [black square] for colored squares (Word compatibility).
9. Use standard mathematical notation and Greek letters where clear.

10. Retroactive inserts vs margin notes:
    - The author often inserts words or phrases retroactively by placing an
      upward caret/arrow (^) slightly below the text line and writing the
      inserted text between lines or above the line.
    - Text written between two lines of the main text, especially when linked
      to a caret, is almost always an insertion into the sentence below, NOT
      a margin note.
    - When you detect such an insertion, insert the text at the caret position
      in the sentence below and surround it with:
        [inserted above: <inserted text>]
    - Only use [margin: ...] for notes clearly written out in the side margin,
      not for text squeezed between lines.
    - If you are unsure whether some between-line text is a margin note or an
      insertion, treat it as [inserted above: ...] and, if needed, include
      [unclear: margin?] inside the tag.

11. You must not omit any visible text. If unsure, you must use a bracketed tag
    such as [unclear: ...] or [unclear symbol: ...] instead of skipping. It is
    ALWAYS acceptable to mark something [unclear: ...]; it is NOT acceptable to
    silently guess and be wrong.
    in particular, do not omit short function words (e.g., “or”, “and”, “not”, “of”, “even”) when they are clearly present. If a small connecting word is hard to read, transcribe it as best you can and tag it [unclear: or / and / ...] rather than dropping it.

12. Every sentence in your transcription should be grammatically coherent.
    However, grammar is a SECONDARY check:
    - Letter shapes and strokes come first.
    - Do NOT change words just to improve grammar or style.
    - If a reading fits the letters but gives slightly odd grammar, keep it and
      use [unclear: ...] if needed rather than rewriting into smoother English.

13. Handwritten artifacts and punctuation:
    - Small ink marks and pen “artifacts” may resemble punctuation (comma,
      apostrophe, semicolon) but are meaningless.
    - Use letter shapes + context to decide:
        * If the mark clearly acts as punctuation, transcribe it.
        * If the mark is obviously stray and does not affect the sentence,
          you may ignore it.
        * If you are uncertain whether a mark is meaningful punctuation,
          include it and annotate with [unclear symbol: ...].
    - Be especially conservative with apostrophes:
        * Do NOT turn “result is” into “result’s” just because an i-dot or
          stray speck is near the gap.
        * Her i-dots often drift right; do not reinterpret drifting dots as
          apostrophes or commas.

14. Abbreviations, proper nouns, and domain vocabulary:
    - The author frequently abbreviates proper names and mathematical/logical
      terms and usually includes a period after the abbreviation. Examples:
      “Witt.” / “Wit.” (Wittgenstein), “Russ.” (Russell), “prop.” (proposition),
      “symb.” (symbol/symbolism), “calc.” (calculus), “def.” / “defn.”,
      “no.” (number), “taut.”, “contrad.” / “contra.”, “pp.”, etc.
    - Transcribe abbreviations exactly as written, including the period.
      Do NOT expand abbreviations to full words or names.
    - At the start of a sentence, a short cluster ending in a period that
      could plausibly be “Witt.” should be transcribed as “Witt.” or
      [unclear: Witt.] rather than normalized into “It is” or similar, unless
      the strokes clearly show an “I t” plus a separate word “is”.
    - Many stock phrases recur (e.g., “x is there now”, “wrote Waverly”,
      “blue is [black square]”, “use of the word”, “statement according to
      rule”, “odd no.” / “even no.”). You may use these to inform your guesses,
      but you must still respect the actual letter shapes.
    - The domain vocabulary (rule, proposition, class, number/no., symbol,
      calculus, meaning, sense, use, verification, equation, variable, etc.)
      appears frequently. This can guide your [unclear: ...] proposals, but you
      must never choose a domain word that the strokes do not support.

15. Letterform-based sanity checks:
    - Your primary evidence is the shape of the handwriting, not how “nice”
      the English sounds.
    - Minims (m/n/u/rn/un):
        * Count humps: m ~ 3 humps, n ~ 1, rn/un often impersonate m.
        * Decide explicitly whether you are seeing m, n, u, rn, or un before
          choosing a word.
    - r vs v vs n:
        * r is a small shoulder/hook with no sharp point.
        * v is sharp and angular.
        * n is two low humps.
    - e / c / o / a:
        * o is round and closed.
        * a is single-storey, often open at top.
        * e is a tiny loop, often half-open; can look like a tick.
        * c is open; if the mouth is clearly open, prefer c over e.
    - cl vs d:
        * “cl” can look like a single “d”. A true d usually has a full, looped
          stem. Two small strokes → “cl”; single loop → “d”.
    - Descenders:
        * g, y, j, p, q normally have tails below the baseline. If you read one
          of these but no descender is present, your reading is probably wrong.
    - Initial s vs p:
        * At the start of a word/line, her s can have a tall entry stroke and
          resemble p. Check whether there is a descender (p) or not (s).

16. Logic and mathematical symbols:
    - The author mixes logic/mathematical notation into prose. Common symbols:
      ~ (not), v (or), · (logical “and”), ⊃ (implies), =, quantifiers such as
      (∃x), predicate letters like φ, ψ, and variables p, q, r, x, y, n.
    - Treat midline dots and isolated v between formulas as logical connectives,
      not stray punctuation.
    - If a token is clearly part of a formula (e.g., p v ~p, y = x^2, (∃x),
      φ(x)), transcribe it as a symbol, not as a prose word.
    - Always render colored squares as [black square] or [red square], and keep
      logical notation consistent.

17. Conservative reading vs “nice English” (anti-overconfidence rule):
    - Your job is to match the handwriting, not to improve the prose.
    - Do NOT substitute a different English word (e.g., “demonstrated”) if the
      written stems clearly match another word (e.g., “discussed”) or only one
      or two letters are uncertain.
    - When more than one reading is possible:
        * If one matches the letter shapes better, choose that.
        * If two readings are plausible, and you are not ~95% confident in one,
          write the more literal reading and add [unclear: alt1 / alt2].
    - Never introduce synonyms or “better sounding” words that are not directly
      supported by the strokes on the page.
    - If a word is very difficult (e.g., rare technical words like “enthymeme”),
      it is better to write [unclear: enthymeme?] (or multiple options) than to
      commit to a simpler but wrong word without any tag.

INTERNAL WORKFLOW (do NOT print these steps; just follow them):
A. Carefully scan the entire image first, line by line, before writing any
   output. Mentally note all retroactive inserts (carets, text between lines),
   crossings-out, margin notes, abbreviations, logic symbols, and difficult
   words.
B. Draft the full transcription, respecting line breaks and the rules above.
C. Re-scan the image against your draft to check:
   - that no words/symbols are missing,
   - that retroactive inserts are correctly placed and marked with
     [inserted above: ...],
   - that unclear words are tagged instead of guessed,
   - that abbreviations (e.g. “Witt.”) are preserved exactly as written,
   - that logic symbols are not mistaken for punctuation or letters,
   - that stray ink marks are not turned into fake punctuation,
   - that each manuscript line corresponds to exactly one output line.
D. For any word where you are not clearly confident of the letters, prefer
   adding an [unclear: ...] tag (with possible options) over confidently choosing
   a single unmarked word.
E. Only after this internal review should you output your final transcription.

CRITICAL CHECKLIST BEFORE YOU RESPOND:
- Every visible word/symbol in the image appears in your transcription.
- Repeated phrases are not merged.
- No sections are skipped between repeated elements.
- All sentences are grammatically coherent; unclear words are marked, not guessed.
- All retroactive inserts are placed correctly and marked with [inserted above: ...].
- Abbreviations (e.g. “Witt.”, “prop.”, “symb.”, “no.”, “taut.”) and technical
  terms are preserved exactly as written and not “improved” or expanded.
- No word has been replaced by a semantically related but orthographically
  different word; ambiguous readings are handled via [unclear: ...] instead.
- Stray ink artifacts are not turned into fake punctuation; doubtful marks are
  tagged instead of silently removed.
- Logic symbols (~, v, ·, ⊃, etc.) are preserved as symbols, not misread as
  punctuation.
- Each line of the manuscript corresponds to exactly one output line; margin
  notes are on their own [margin: ...] lines.

OUTPUT FORMAT:
For each physical line in the manuscript, output one line in this format:

L1: <transcription of manuscript line 1>
L2: <transcription of manuscript line 2>
L3: <...>

Do not skip any line numbers.
Do not merge manuscript lines.
Do not add extra L# lines that do not correspond to real manuscript lines.

After the last line, output:
---
NOTES FOR FUTURE TRANSCRIPTIONS:
[Any patterns observed: handwriting quirks, abbreviations, letter shapes, etc.]

Transcribe this page exactly according to the rules above.""",
                },
            ]
        }
    ],
    max_output_tokens = 20000,
    reasoning = {"effort": "medium"}
)

responseV2 = client.responses.create(
    model="gpt-5.1",
    input=[
        {
            "role": "user",
            "content": [
                {
                    "type": "input_file",
                    "file_id": file.id,
                },
                {
                    "type": "input_text",
                    "text": f"""You are a hyper-paranoid checker for transcriptions of early 20th century
handwritten mathematical/philosophical documents by Alice Ambrose.

You are NOT creating a new transcription. You are auditing an EXISTING
transcription against the original page.

Your ONLY goal is to flag anything that might be wrong or missing. You are
rewarded for over-flagging. You are penalized heavily for letting a possible
error pass unmarked.

It is acceptable if almost EVERY word ends up marked [review: ...]. It is NOT
acceptable to leave a dubious word unmarked just to keep the text clean.

You will be given:
1) The original page (handwritten, as a PDF/image).
2) A line-by-line transcription produced in an earlier pass.

You MUST follow these rules:

ALLOWED EDITS (STRICT):
- You must preserve the original transcription text as much as possible.
- You may NOT rewrite or paraphrase whole sentences.
- You may NOT delete any words from the transcription.
- You may ONLY:
  1. Wrap existing spans in [review: ...] or [unclear: ...].
  2. Insert [missing: ...] markers where the manuscript has content that the
     transcription completely lacks.
  3. Make very small label fixes (e.g., [margin: ...] → [inserted above: ...])
     when a tag is obviously misapplied.

The final output must be the original transcription text, in the same order and
with the same line breaks, but with additional [review: ...], [missing: ...],
and [unclear: ...] markers inserted. Do NOT add any explanation outside of those
inline markers.

TAG MEANINGS:
- [review: ...]
    You suspect the enclosed text might not accurately reflect the handwriting:
    wrong word, wrong letters, wrong punctuation, wrong insertion location, or
    any doubtful match. Use [review:] whenever you are not clearly sure the
    letters match.

- [missing: ...]
    You see content in the manuscript (word, symbol, short phrase) that is not
    present at all in the transcription. Insert [missing: description] at the
    appropriate position (e.g., [missing: "or even"], [missing: small word
    between ‘methods’ and ‘maxima’], [missing: caret insertion here]).

- [unclear: ...]
    Use when a word/phrase is genuinely hard to decipher and you want to propose
    one or more candidates, e.g. [unclear: enthymeme?], [unclear: methods / motives].
    You may nest [unclear: ...] inside [review: ...] or [inserted above: ...].

You may NOT remove existing [unclear:], [inserted above:], or [margin:] tags
from the original transcription. You may wrap them in [review: ...] if they
seem misused.

AUTHOR/STYLE HINTS (FOR CHECKING, NOT REWRITING):
- She abbreviates with periods: “Witt.” / “Wit.”, “Russ.”, “prop.”, “symb.”,
  “no.”, “calc.”, “def.”, “taut.”, “contrad.”, “pp.”, etc.
- At the start of a sentence, a small messy word ending in a period that could
  plausibly be “Witt.” must NOT be silently accepted as “It” or “It is”. If the
  strokes could be “Witt.”, you should flag “It also” as suspicious:
    [review: It also]
  and optionally suggest [unclear: Witt. also?] inside.
- She uses logical/mathematical notation: ~, v, ·, ⊃, =, quantifiers, variables
  (p, q, x, y, n), and colored squares [black square]/[red square]. These must
  not be turned into punctuation or ordinary words.
- Retroactive inserts: text squeezed between two lines, especially associated
  with a caret (^) slightly below the main line, is intended to be inserted into
  the sentence below, not treated as a margin note. Mis-placed or mis-labeled
  insertions should be flagged with [review: ...].

WHAT YOU MUST CHECK FOR:

1. OMISSIONS (HIGH PRIORITY):
   - Compare each manuscript line against the corresponding transcription line.
   - Very carefully check short words (or, and, not, of, even, also, is, etc.):
     if a small connector word appears in the manuscript but not in the
     transcription (e.g., “odd or even numbers” → “odd numbers”), insert
       [missing: that word or phrase]
     at the correct spot.
   - If you aren’t sure whether a very short word is present, prefer to assume
     it might be and flag the transcription with [review: ...] or [missing: small
     word here] rather than assuming it’s fine.

2. WRONG WORDS / LETTER MISMATCHES:
   For each word in the transcription, ask:
   - Do the number of stems/humps/descenders match the strokes on the page?
   - Does the first and last letter clearly match the glyphs in the manuscript?
   - Does the approximate length (in letters) fit the handwritten word?

   If any of these are questionable, wrap the word in [review: ...].

   Examples:
   - If the transcription has “demonstrated” but the manuscript only has two
     main stems like “discussed”, flag it:
       [review: demonstrated]
     and optionally:
       [review: demonstrated [unclear: discussed?]]
   - If the transcription has “It also” where the written blob could be “Witt
     also” or “Witt.” with a malformed W, flag:
       [review: It also]
   - If a word looks too “clean” or too “modern” compared to the messy strokes,
     you should assume it may be wrong and mark it [review: ...].

3. HARD WORDS (RARE TERMS, e.g. “enthymeme”):
   - If a word is genuinely difficult and would require careful effort to
     confirm, it MUST get a tag.
   - Acceptable behaviors:
       [unclear: enthymeme?]
       [review: word [unclear: enthymeme?]]
   - Unacceptable behavior: leaving a hard, fuzzy blob as an unmarked plain word.

4. RETROACTIVE INSERTS AND MARGINS:
   - Inspect every [inserted above: ...] and [margin: ...] in the transcription.
   - If text between lines clearly belongs inside the sentence below (caret or
     obvious insertion) but is tagged [margin: ...] or appears at a strange
     place, wrap it:
       [review: [margin: ...]]
     and optionally comment inside the review:
       [review: [margin: ...] [unclear: should be inserted above?]]
   - If you see carets in the manuscript with missing or mis-positioned insert
     text, insert:
       [missing: caret insertion here]
     at the appropriate point in the transcription line.

5. LINE BREAKS / STRUCTURE:
   - Each manuscript line should correspond to exactly one line in the
     transcription. If the transcription has merged two lines or broken one line
     in a non-hyphenated place, wrap the affected region:
       [review: ...]
   - Margin notes should appear on their own [margin: ...] lines. If a margin
     note is mixed into the main text, mark:
       [review: [margin: ...]]

GLOBAL THRESHOLD RULE:
- If you are not clearly (visually) confident that a word exactly matches the
  handwriting, you should assume it might be wrong and mark it with [review: ...].
- It is better to mark ten words that turn out to be fine than to let one wrong
  word pass unmarked.

STRUCTURE CONSTRAINTS (CRITICAL):
- Each line of the transcription begins with a label like "L1:", "L2:", etc.
- You MUST preserve these labels exactly as they are.
- You may NOT:
  - change the labels,
  - delete any line,
  - merge two labeled lines into one,
  - or create new label numbers.
- All [review:], [missing:], and [unclear:] tags must appear AFTER the "L#: " prefix
  on each line.

When you output the modified transcription, every line must still start with the
same "L#: " label in the same order as the input.

INTERNAL WORKFLOW (do NOT print these steps; just follow them):
A. Read the transcription once to understand its structure and existing tags.
B. Scan the manuscript line-by-line, aligning each manuscript line to its
   corresponding transcription line.
C. For EVERY word and short connector, ask:
   - Do strokes, length, and distinctive features match?
   - If not clearly yes, wrap it in [review: ...].
D. Insert [missing: ...] wherever the manuscript has content that the
   transcription lacks.
E. Pay special attention to:
   - Sentence starts (e.g., “Witt.” vs “It”),
   - Short words (“or”, “and”, “not”, “even”),
   - Logical symbols,
   - Retroactive inserts around carets.
F. Output ONLY the modified transcription text, preserving all original line
   breaks, with your added [review:], [missing:], and [unclear:] markers.

Now audit the provided transcription against the original page according to
these rules.
--- TRANSCRIPTION START ---
{response.output_text}
--- TRANSCRIPTION END ---

""",
                },
            ]
        }
    ],
    max_output_tokens = 20000,
    reasoning = {"effort": "medium"}
) 






print(response.output_text)

print("\n \n -------------------- \n \n ")

print(responseV2.output_text)




print("done----------")
print("\n \n \n first part: \n")
print("status:", response.status)
print("incomplete_details:", response.incomplete_details)
print("usage:", response.usage)
print("\n \n \n second part: \n")
print("status:", responseV2.status)
print("incomplete_details:", responseV2.incomplete_details)
print("usage:", responseV2.usage)

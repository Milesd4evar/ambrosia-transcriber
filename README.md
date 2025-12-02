# ambrosia

two-pass transcription + checking pipeline for early 20th c. handwritten math/philosophy manuscripts (alice ambrose).

- pass 1: transcription using openai gpt-5.1 with a detailed system prompt
- pass 2: hyper-paranoid checker that tags [review:], [unclear:], and [missing:] to guide a human transcriber

currently: single-script prototype in `ambrosia.py`.

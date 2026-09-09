# Exact-copy landing pages from Word documents

Use this workflow when the user says the supplied Word copy must be used exactly, without shortening or rewriting.

## Source extraction

1. Read the `.docx` with a document-aware reader or `python-docx`.
2. Keep the Word document as the single source of truth. Build shared page data directly from its paragraphs instead of manually retyping long descriptions.
3. Preserve every non-empty paragraph verbatim, including product titles, descriptions, offer wording and prices.
4. UI-only labels required for interaction, such as form field labels and previous/next controls, may be added, but they must not introduce new marketing claims.

## Multi-version generation

- Use one checked-in generator script that reads the Word file and outputs every requested variant.
- Make the generator idempotent. Replace a stable generated root/marker block on every run; do not only replace the initial placeholder, because later reruns would update CSS while silently leaving stale HTML.
- Keep factual content shared and direction CSS/markup separate.
- If the user asks for several revisions of an existing direction, place them in non-destructive folders such as `v1-a/`, `v1-b/`, and `v2-new/` unless explicit overwrite instructions are given.
- Distinguish variants through information architecture, not only color. Examples:
  - Horizontal expandable reading river.
  - Long-form manuscript with sticky table of contents and full chapters.
  - Filmstrip/carousel with one full book description in focus and accessible thumbnail tabs.

## Deterministic copy verification

After generating each page:

1. Extract all non-empty source paragraphs from the Word document.
2. Parse visible HTML text with an HTML parser.
3. Normalize whitespace only for comparison. Do not normalize wording, punctuation or numbers.
4. Assert that every source paragraph occurs in the rendered HTML text.
5. Report `source paragraphs`, `missing paragraphs`, and a sample of any missing content.

Example check:

```python
from docx import Document
from html.parser import HTMLParser
from html import unescape
import re

source = [p.text for p in Document(docx_path).paragraphs if p.text != ""]

def norm(value):
    return re.sub(r"\s+", " ", unescape(value)).strip()

class TextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
    def handle_data(self, data):
        self.parts.append(data)

parser = TextParser()
parser.feed(html_path.read_text(encoding="utf-8"))
visible = norm(" ".join(parser.parts))
missing = [(i + 1, text) for i, text in enumerate(source) if norm(text) not in visible]
assert not missing, missing
```

## Order-section pattern

When requested, use a desktop split layout:

- Left: every supplied product-price line verbatim, including the complete-set line.
- Right: order form with name, phone, province/city when relevant, detailed delivery address, quantity and note.
- For Vietnam province selection, use a required `select` with `autocomplete="address-level1"`, verify the current administrative-unit count against an authoritative source, and count rendered options deterministically. Keep the detailed address field separate.
- On mobile, stack price list before the form.
- CTA links should scroll directly to the order section.
- If no endpoint exists, do not imply the order was submitted. Keep submission blocked or show an explicit operational notice that the form is not connected.

## Verification

In addition to copy matching:

- Check every local asset path.
- Count expected books, price rows and form fields.
- Check duplicate IDs, responsive rules, focus states and reduced-motion support.
- Render desktop and mobile screenshots.
- For long pages, use a same-origin iframe QA harness to scroll to a deep section before headless screenshot capture when direct fragment screenshots race with smooth scrolling.

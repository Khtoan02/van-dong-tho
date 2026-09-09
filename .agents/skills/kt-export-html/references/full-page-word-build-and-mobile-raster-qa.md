# Full-page Word build and mobile raster QA

Use this recipe when extending an existing hero into a long landing page from exact Word copy.

## Deterministic Word extraction without extra dependencies

When `python-docx` is unavailable, parse `word/document.xml` from the DOCX zip with stdlib `zipfile` + `xml.etree.ElementTree`.

- Iterate every `w:p`.
- Preserve ordered `w:t` text.
- Convert `w:br` / `w:cr` to line breaks and `w:tab` to tabs before splitting. A Word document can visually contain more copy lines than its `w:p` count because line breaks live inside one paragraph.
- Assert the expected source count before generation.
- If the source includes an explicit editorial note such as “chia thành 3 ô”, classify it as an instruction, implement it structurally, exclude only that line from public-copy verification, and report the exclusion explicitly.

## Exact-copy generation

- Keep a checked-in generator that maps source paragraph indexes into section markup; do not manually retype long paragraphs into HTML.
- Keep a checked-in verifier that normalizes whitespace only and reports source count, intentionally excluded editorial instructions, public paragraphs checked, missing paragraphs, duplicate IDs, missing local assets, and form-field count.
- UI labels required by forms may be added. If no form endpoint exists, prevent submission and show an explicit “not connected” operational notice rather than simulating success.

## Long-page screenshot QA

A single `Page.captureScreenshot(captureBeyondViewport=true)` on a very tall mobile page may show blank offscreen images even when images are not lazy-loaded. Treat this as a rasterization artifact until verified.

Validated distinction procedure:

1. Capture the full page for macro rhythm and overflow.
2. For each suspicious deep section, set exact mobile metrics, reload, call `element.scrollIntoView({block: 'start', behavior: 'instant'})`, wait for paint, then capture the current viewport with `captureBeyondViewport=false`.
3. Judge image/layout correctness from the scrolled viewport capture, not the blank full-page artifact.
4. Verify both standard mobile (390x844) and short mobile (390x700) when above-the-fold composition matters.

## Optical spacing around transparent mockups

Transparent product assets inside a fixed-height wrapper can create a large apparent gap because `object-fit: contain` vertically centers the visible pixels. Moving `top` alone may not solve it.

- Reduce the wrapper height until it closely matches the rendered asset aspect ratio.
- Then adjust `top` and width.
- Re-render at 390x844 and 390x700.
- Confirm the logo position separately when the user asks it to remain fixed.

## Antigravity IDE preview delivery

For frontend tasks in Antigravity IDE, do not rely only on a markdown `localhost` link. After confirming HTTP 200, call the desktop `open_preview` tool with `http://127.0.0.1:<port>/...` and a useful tab label. Keep the direct path and URL in the report as fallbacks.

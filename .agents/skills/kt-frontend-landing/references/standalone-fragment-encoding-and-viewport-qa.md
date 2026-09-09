# Standalone fragment encoding and viewport QA

Use this when a builder-ready HTML fragment is also opened directly through localhost for review.

## Symptom split

- Mojibake such as `THá»¬ THÃCH`, `ÄÄ‚NG KÃ`, or `VÃ€` is an encoding failure, not a missing Roboto glyph.
- A requested 390px mobile emulation reporting `innerWidth` around 980px is missing viewport context, not proof that the responsive CSS failed.

## Fast diagnosis

1. Inspect response headers:

```bash
curl -sI http://127.0.0.1:PORT/artifact.html
```

If the response is only `Content-Type: text/html`, the browser still needs an early charset declaration.

2. Inspect the first 1.024 bytes and verify UTF-8 decoding:

```python
from pathlib import Path
raw = Path("artifact.html").read_bytes()
assert raw.decode("utf-8")
assert b'<meta charset="UTF-8">'.lower() in raw[:1024].lower()
```

3. In the real browser record:

```js
({
  characterSet: document.characterSet,
  innerWidth,
  clientWidth: document.documentElement.clientWidth,
  scrollWidth: document.documentElement.scrollWidth
})
```

## Safe QA contexts

Choose one deliberately:

- If the target builder accepts top-level meta elements, begin the fragment with:

```html
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
```

- Otherwise, keep the deployment fragment wrapper-free and place it inside a temporary QA document whose `<head>` contains both meta elements.
- Alternatively, configure the preview server to return `Content-Type: text/html; charset=UTF-8`; still provide viewport context in the QA document.

Do not add `<html>`, `<head>`, or `<body>` to a Custom HTML/JS deployment fragment solely to fix local preview.

## Regression gates

At desktop and exact 390x844 mobile:

- `document.characterSet === "UTF-8"`
- `innerWidth === 390` for the mobile run
- `scrollWidth <= clientWidth`
- Supplied Vietnamese strings render literally in DOM text
- Screenshot inspection confirms correct diacritics and wrapping

If a CDP full-section crop starts in the preceding section, reset `window.scrollTo(0, 0)` before using a document-coordinate `Page.captureScreenshot` clip.

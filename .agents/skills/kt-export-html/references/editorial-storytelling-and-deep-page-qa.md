# Editorial storytelling sections and deep-page QA

Use when a landing page is built from long-form book, author, case-study, founder-story, or narrative copy and the user expects the design to follow the content rather than force every section into a generic grid.

## Analyze narrative function before layout

Classify each section before choosing components:

- **Story opening**: a question, scene, tension, or premise. Treat it like the first page of a chapter, not a feature grid.
- **Story continuation**: evidence, backstory, or escalation. Maintain the reading line and use imagery as a pause between passages.
- **Concept explanation**: cards, tabs, or structured lists can help here.
- **Reflection / quotation**: reduce density and increase visual silence.
- **Offer / order**: switch to clear product facts and functional form UI.

Do not use the same image-left/copy-right composition for consecutive story sections. It interrupts narrative rhythm and makes supplied long-form copy feel like advertising blocks.

## Typography that follows the source art

Roboto remains the user's default for body copy and UI, but it is not automatically the right display face. When the hero contains expressive literary or hand-drawn typography:

1. Inspect the hero title's contrast, width, stroke shape, and emotional register.
2. Choose a Vietnamese-capable display font that harmonizes with it.
3. Keep body and form labels in Roboto for readability.
4. Render actual Vietnamese headings before committing; verify diacritics and wrapping on mobile.

A validated pairing for literary/spiritual book pages is **Cormorant Garamond 600/700 for headings + Roboto 400/500/700 for body/UI**.

## Storytelling layout patterns

### Chapter opening

- Large editorial heading with a soft display serif.
- Narrow reading column, generous line-height, and a visible chapter/beat marker.
- Optional drop cap on the first passage.
- Preserve the exact paragraph; styling may change, wording may not.

### Two-beat passage

- Put each supplied paragraph in its own narrative beat.
- Connect beats with a fine vertical thread or chapter markers.
- Place a small product/bookplate between beats as a pause, not as a competing sales visual.
- On mobile: heading -> passage 1 -> bookplate -> passage 2.

### Documentary continuation

- Keep passages in one reading stream.
- Use an author/photo strip between paragraphs rather than a giant portrait beside the copy.
- A horizontal crop can function as a documentary pause; test its object-position on desktop and mobile.

## Video embeds

For a supplied YouTube URL:

1. Verify metadata with YouTube oEmbed.
2. Embed with `https://www.youtube-nocookie.com/embed/<VIDEO_ID>?rel=0`.
3. Use a 16:9 wrapper and a descriptive iframe `title` from verified metadata.
4. Verify a real scrolled viewport, not only a full-page screenshot.

## Vietnam province selector

When an order form needs province/city selection:

- Add a required `select` with `autocomplete="address-level1"` plus the detailed street-address textarea.
- Use the current 34 province-level administrative units and record the authoritative source used.
- Keep the options embedded when reliability matters more than live API dependency.
- Verify option count deterministically.
- Do not imply the form submits unless a real endpoint exists; block submit and show an operational notice until connected.

## Idempotent Word-driven generators

A generator that only replaces the initial placeholder will silently stop updating markup after the first run. Make reruns idempotent:

1. Add stable start/end markers around generated CSS and body content, or replace the entire generated root such as `.content-page` through the closing `</main>`.
2. Rebuild from the Word source on every run.
3. Run exact-copy verification after every regeneration.
4. Include new controls such as `select` in form-field counts.
5. Verify external embed IDs and expected option counts.

## Deep-page CDP verification

Very tall mobile screenshots can show blank offscreen images or iframes even when eager-loaded because Chromium may not raster content that never entered the viewport. Do not treat the blank full-page capture as proof of a production defect.

Validated procedure:

1. Capture the full page for macro rhythm and overflow.
2. For every deep image, iframe, form, or sticky section, use CDP to call `scrollIntoView({block: 'start', behavior: 'instant'})`.
3. Wait for paint, then capture the real viewport with `captureBeyondViewport: false`.
4. Compare the full-page artifact with the scrolled viewport before changing code.
5. For exact mobile widths on Windows headless Chrome, use `Emulation.setDeviceMetricsOverride`; `--window-size=390,...` may still produce a wider inner viewport.

## Preview delivery in Antigravity IDE

A markdown localhost link may be handled by the chat surface instead of the desktop preview pane. When the user is in Antigravity IDE, call `open_preview` with `http://127.0.0.1:<port>/index.html` and a clear tab label. Confirm HTTP 200 separately, but open the pane yourself rather than assuming the user can click the chat link.
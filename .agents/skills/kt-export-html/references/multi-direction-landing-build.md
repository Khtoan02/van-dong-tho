# Multi-direction Landing Page Build

Use this checklist when one brief produces several committed visual directions.

## 1. Normalize source content

Create one source-of-truth structure before writing page markup:

- product/title and exact asset filename
- supplied description or approved shortened copy
- list price, sale price, discount
- shared CTA copy
- author/brand copy
- forbidden inventions: testimonials, metrics, urgency, unsupported claims

When filenames include Unicode and spaces, preserve them exactly and verify the resolved local path from each version directory.

## 2. Direction contract

For every `vN`, specify all of the following before implementation:

- hero anchor and image placement
- page ground and accent palette
- display/body type behavior
- section rhythm and separators
- collection/product explorer behavior
- author treatment
- final-offer composition
- desktop and mobile hero strategy

Do not call a palette swap a new direction.

## 3. Recommended architecture

For a static multi-version concept build:

- Keep `v1/index.html` ... `vN/index.html` directly runnable.
- A generator script may hold shared factual data and emit self-contained HTML.
- Keep shared CSS primitives small; direction CSS should own composition.
- Put direction-specific mobile overrides after direction desktop rules.
- Use semantic sections and an accessible product explorer.

Tabbed explorer minimum:

- `role="tablist"`, `role="tab"`, `role="tabpanel"`
- `aria-selected` and `aria-controls`
- one active panel, others hidden
- Left/Right or Up/Down arrow support
- visible `:focus-visible`

## 4. Deterministic audit per version

Verify and record:

- page returns HTTP 200
- expected number of product tabs/items
- hero CTA and closing CTA both present
- no duplicate IDs
- every local `<img src>` resolves
- responsive media query exists
- `prefers-reduced-motion` exists
- visible focus styling exists

A small Python `HTMLParser` audit is sufficient for these structural checks.

## 5. Screenshot QA

Render at minimum:

- desktop: approximately 1440 x 1000
- mobile: 390 x 844

Then compare contact sheets across directions.

First-viewport checks:

- headline fully visible and sensibly wrapped
- primary CTA visible or intentionally positioned just below a clear continuation
- hero subject not cropped through face, cover title, or critical artwork
- sufficient text/background contrast
- no horizontal clipping
- each direction remains recognizable without reading its label

If mobile text clips:

1. Add `min-width: 0` to the grid/flex child.
2. Set an explicit copy width/max-width relative to the viewport.
3. Add mobile-specific display sizes after direction desktop CSS.
4. Reposition background imagery independently from desktop.
5. Re-render the screenshot; do not infer success from CSS alone.

## 6. Delivery notes

Report:

- all version paths and preview URLs
- real verification results
- which assets and content sources were used
- any missing checkout/CTA destination
- font/network dependencies and fallbacks
- assumptions that still need client confirmation

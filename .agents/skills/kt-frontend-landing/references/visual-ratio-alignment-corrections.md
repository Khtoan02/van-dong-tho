# Visual ratio and alignment correction patterns

Use this reference when iterative landing-page review surfaces complaints such as “headline is too large,” “the product is too small,” or “the title is misaligned with the content.”

## Diagnose ratio before changing decoration

1. Capture the exact desktop and mobile CSS viewports.
2. Measure the headline font size, line count, line-height, copy-column width, media-column width, and rendered subject size.
3. Distinguish the media frame from the subject inside the source asset. A square mockup may contain large internal white margins, so widening the frame alone may not make the product feel larger.
4. Repair the ratio jointly:
   - reduce headline size and relax line-height,
   - rebalance grid columns toward the media,
   - enlarge the subject inside a clipped media wrapper only when the source has safe internal margins,
   - re-render before making a second adjustment.
5. Check the actual new screenshot. Do not critique a stale render left from a previous QA run.

## Internal whitespace in supplied imagery

For an image whose subject occupies only part of its canvas:

- Prefer a wrapper with `overflow: hidden` and a modest image transform such as `scale(1.08–1.15)`.
- Inspect the native image first so logos, heads, hands, and shadows are not cropped.
- `getBoundingClientRect()` on a transformed image may extend outside the wrapper even when the wrapper clips it and the document has no horizontal overflow. Treat `scrollWidth > clientWidth` as the real overflow test.
- If the source already contains a label or name card, avoid duplicating the same visual copy beside it. Keep a semantic heading visually hidden if necessary.

## Alignment invariant

Within one section, the heading, divider, body list, and closing statement should share a deliberate alignment system.

A common defect is:

- heading uses the full 1140px container,
- body uses a centered 820px helper,
- closing statement uses another auto-aligned max-width.

That creates an obvious horizontal “step.” Either place all elements on the full container axis or make the narrower body axis explicit in the heading too. After repair, compare actual left-edge coordinates, not only CSS declarations.

## Decorative-block discipline

Color blocks behind product imagery are optional composition, not a default. If the supplied product image already has enough contrast, omit the extra block. When the user asks to remove it, delete both the base pseudo-element and breakpoint-specific overrides so dead decoration rules do not remain.

## Portrait assets in authority sections

- Download user-supplied remote portraits into the client project when portability matters.
- Record native dimensions and alpha before layout.
- Use `object-fit: contain` for cutout portraits unless intentional crop is approved.
- If a below-fold portrait is essential to the section and headless/full-page QA does not trigger lazy loading, remove `loading="lazy"` or explicitly scroll during QA; verify the final rendered image has non-zero `naturalWidth`.
- Desktop pattern: portrait column + biography column, with proof metrics spanning the row below.
- Mobile pattern: portrait, biography, then stacked proof metrics.

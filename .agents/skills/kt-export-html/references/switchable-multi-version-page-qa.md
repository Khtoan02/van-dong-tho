# Switchable multi-version landing pages - responsive QA

Use when one HTML document keeps shared copy/markup but exposes several visual directions through `body[data-version]` and a visible version switcher.

## Durable implementation pattern

- Keep factual copy in one shared DOM so wording cannot drift between directions.
- Switch only a root attribute such as `body[data-version="2"]`; update `aria-pressed` on every switch button and persist the choice only as a convenience.
- Give every direction clearly different composition, section rhythm, surface treatment, and typography behavior - not just different colors.
- Keep controls keyboard accessible and provide an `aria-live` status message.

## CSS specificity trap

Source order alone does not guarantee that a shared mobile rule wins. A direction rule such as:

```css
body[data-version="3"] .ebook-panel { grid-template-columns:1.2fr .8fr; }
```

beats a later but less-specific rule:

```css
@media (max-width:900px) { .ebook-panel { grid-template-columns:1fr; } }
```

Put matching-specificity overrides inside the media query:

```css
@media (max-width:900px) {
  body[data-version="3"] .ebook-panel { grid-template-columns:1fr; }
}
```

Audit every direction at the mobile breakpoint; do not infer responsiveness from the shared rule.

## Version-switcher placement

A wide fixed bottom dock can hide CTAs and long-form copy on mobile. A validated compact alternative is a narrow vertical numeric dock at the lower-right edge:

```css
@media (max-width:900px) {
  .version-switcher {
    right:10px;
    bottom:10px;
    max-width:56px;
    flex-direction:column;
  }
  .version-btn { width:42px; height:42px; padding:0; font-size:0; }
  .version-btn::after { content:attr(data-version); font-size:.8rem; }
}
```

Retain full descriptive labels in accessible names/DOM. Capture deep-section screenshots where CTA buttons sit near the viewport bottom to prove the dock does not cover them.

### Reserve a mobile content lane when the compact dock still overlaps copy

A 42-56px right-edge dock can still cover wide headings, service descriptions, or ebook copy even though it no longer covers the CTA. When screenshot QA shows this, reserve a matching content lane instead of making the control illegibly small:

```css
@media (max-width:520px) {
  .story-section,
  .beliefs-section,
  .services-section,
  .ebook-section,
  .site-footer {
    padding-right:56px; /* dock width + offset + breathing room */
  }
}
```

If a direction has a full-bleed or rotated inner block, update that block's width and right padding by the same delta so the background remains full while readable content avoids the dock. Re-render the longest heading, service CTA, and lead-magnet section at the exact mobile viewport after the change. A clean overflow assertion alone is insufficient because a fixed overlay does not increase `scrollWidth`.

## Overflow checks with animated hero ornaments

Animated concentric rings and marquee tracks may temporarily extend document width even when their local container looks clipped. If the visual contract permits it, set overflow clipping at the root (`html { overflow-x:hidden; }`), not only on `body`, then measure:

- `innerWidth`
- `document.documentElement.scrollWidth`
- offending element rectangles after animations have started

Run this assertion after selecting every direction at desktop and mobile widths. Allow for the vertical scrollbar reducing layout width on desktop, but never allow `scrollWidth > innerWidth` on the exact mobile viewport.

## Evidence set

For each direction:

1. Click the real switch button and assert `body.dataset.version` changed.
2. Capture one desktop deep-section viewport.
3. Capture one exact mobile deep-section viewport.
4. Build desktop and mobile contact sheets to catch directions converging visually.
5. Separately capture the longest or most structurally different mobile sections, especially founder copy and ebook/offer sections.
6. Inspect visible pixels for clipping, unreadable contrast, and control overlap - HTTP and DOM assertions are insufficient.

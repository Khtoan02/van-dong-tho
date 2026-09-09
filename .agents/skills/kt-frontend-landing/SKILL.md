---
name: kt-frontend-landing
description: Use when cloning or coding responsive landing-page UI.
version: 1.0.0
author: Coder
license: MIT
platforms: [macos, windows, linux]
metadata:
  antigravity:
    tags: [frontend, landing-page, html, css, responsive, visual-qa]
    related_skills: [kt-design-loop, hero-derived-long-form-landing-pages]
---

# Landing Page Frontend

Build or clone landing-page sections as production-ready HTML/CSS, preserve conversion hierarchy, and verify the rendered result at real desktop and mobile viewports before reporting completion.

## When to use

Use for:

- Hero sections, sales pages, opt-in pages, webinar pages, thank-you pages, and campaign microsites.
- Reference-image-to-HTML/CSS cloning.
- Responsive repairs involving crop, overflow, spacing, hierarchy, CTA consistency, or embedded media shells.
- Extending an approved hero into a larger page together with `hero-derived-long-form-landing-pages`.

When the user invokes `/kt-design-loop`, load `kt-design-loop` as well. This skill governs implementation and responsive QA; `kt-design-loop` governs teardown and independent critics.

## Inputs and placement

1. Identify the client or internal project and its deliverable folder.
2. Read the project README, `_agent` context, brand rules, copy, and assets when available.
3. Keep client/project deliverables in their project folder, never in Antigravity system directories.
4. Inspect every reference at its native dimensions before estimating proportions.
5. If an asset or claim is absent, use a clearly neutral placeholder rather than inventing content.

## Implementation standard

- Use semantic HTML and maintainable CSS.
- Define design tokens in `:root`: colors, typography, radii, shadows, spacing, and content width.
- Prefer mobile-first or responsive-first sizing with `clamp()`, grid/flex constraints, and explicit breakpoints.
- Keep `box-sizing: border-box` global and set `min-width: 0` on grid/flex children that contain long copy.
- Never horizontally scale typography to imitate a reference. Use the approved family/weight, then tune size, tracking, line-height, column width, and deliberate line breaks.
- Keep one primary CTA treatment unless the brief explicitly defines multiple CTA levels.
- Use inline SVG for simple icons when that avoids unnecessary dependencies.
- Use CDN fonts/libraries only when needed and disclose them.
- Preserve exact supplied identifiers, dates, prices, CTA copy, and claims. Do not silently update stale-looking reference content.

## Reference cloning workflow

1. Extract exact visible text and observable geometry from the reference.
2. Record 5-7 checkable visual mechanisms when quality is judged against a reference.
3. Build the layout skeleton before decorative detail.
4. Match hierarchy in this order:
   - major grid and column balance,
   - headline wrapping and dominant media dimensions,
   - conversion cards and CTA alignment,
   - spacing rhythm,
   - typography and color,
   - subtle decoration.
5. Render at the reference's native viewport when known.
6. Compare renders, fix the single largest visible gap, and repeat.
7. Re-capture after every material edit and confirm the screenshot timestamp/output changed; never judge the new CSS from a stale render.

## Ratio, alignment, and supplied-image corrections

User review often identifies composition problems more accurately than isolated token checks. Treat these as layout corrections, not cosmetic requests:

- **Headline too large:** tune font size, line-height, copy-column width, and line count together. A smaller font in a simultaneously narrower column may look unchanged.
- **Product image too small:** distinguish the outer frame from the subject inside the image canvas. If the source contains safe internal whitespace, enlarge the subject inside an overflow-clipped wrapper and inspect logo/head/hand/shadow edges after rendering.
- **Section heading feels offset:** compare the actual left edges of heading, divider, list, and closing statement. Do not mix a full-width section heading with a centered narrow body helper unless that offset is intentional.
- **Unwanted decorative block:** decoration behind a product image is optional. Remove the pseudo-element and every breakpoint override rather than leaving dead CSS.
- **Authority portrait:** inspect alpha and native dimensions, keep supplied copy/claims intact, and avoid visually duplicating a name card already baked into the image.
  - When replacing a placeholder with a transparent portrait, remove the placeholder wrapper's background, fixed height, radius, overflow, padding, and breakpoint overrides unless they remain intentionally visible. A transparent source still appears on the wrapper's CSS background.
  - Interpret a relative resize against the current rendered image, not the source pixels or column: for example, 30% larger than `width: 50%` means `width: 65%`. Keep `height: auto`, then re-render desktop and true-width mobile.

See `references/visual-ratio-alignment-corrections.md` for worked diagnosis patterns, safe internal-image scaling, alignment invariants, and portrait-section guidance. See `references/transparent-portrait-sizing.md` for alpha-background diagnosis, placeholder cleanup, relative resizing, and verification.

## Long-headline rule

Reference heroes often combine large type with long Vietnamese copy. A line that crosses the grid gutter is a blocking defect.

- Measure the rendered line, not just the intended CSS column.
- For deliberate desktop line breaks, `white-space: nowrap` is acceptable only when every line is proven to fit.
- If a line does not fit, first tune the true font size/tracking and grid proportions. Do not hide the overflow or let adjacent media cover it.
- At mobile breakpoints, restore natural wrapping with `white-space: normal` and `overflow-wrap: break-word` where needed.

## Blank video and media placeholders

When the user asks to leave video content blank:

- Recreate only the observable shell: aspect ratio, frame, radius, inset, and shadow.
- Use a neutral dark or brand-neutral interior.
- Do not copy a speaker thumbnail, poster, player controls, fake duration, or play button unless specifically requested.
- Label the region accessibly as a video placeholder.

## Responsive verification

A screenshot is valid evidence only when its CSS viewport is known.

1. Verify desktop at the reference size or the project's desktop target.
2. Verify at least one actual mobile viewport, typically 390 × 844, and add smaller/wider breakpoints when the design warrants it.
3. Record `document.characterSet`, `innerWidth`, `document.documentElement.clientWidth`, `scrollWidth`, and `scrollHeight`.
   - When Vietnamese appears as `THá»¬ THÃCH`, diagnose response/meta encoding before changing fonts: require UTF-8 via the HTTP charset or a `<meta charset="UTF-8">` in the first 1.024 bytes.
   - For standalone HTML fragments, verify a viewport declaration is present in the artifact or its QA wrapper. If an intended 390px CDP run reports `innerWidth` near 980px, fix the missing viewport context before judging responsive CSS.
   - On overlay-scrollbar/mobile viewports, `scrollWidth == innerWidth` is expected.
   - On desktop Chrome with a classic vertical scrollbar, `innerWidth` may exceed `clientWidth` by the scrollbar width. The robust defect test is `scrollWidth > clientWidth` or a measured child extending beyond the unclipped root.
   - A transformed image may report a bounding box outside its clipped wrapper without causing document overflow; inspect the wrapper and root metrics before calling it a defect.
4. Inspect actual renders for:
   - clipped words or cards,
   - horizontal overflow,
   - image ratio/crop,
   - CTA tap size and wrapping,
   - full media-frame width,
   - above-fold hierarchy,
   - tiny benefit/legal text.
5. Do not treat `overflow-x: hidden` as a repair for an oversized child.
6. On Windows, a command-line Chrome screenshot may be cropped from a browser viewport wider than the requested narrow window. Use CDP device metrics for authoritative mobile evidence. See `references/windows-chrome-cdp-responsive-rendering.md` and `scripts/render_viewports_cdp.py`.

For the complete fragment-specific diagnosis, safe preview contexts, and regression probes, see `references/standalone-fragment-encoding-and-viewport-qa.md`.

## Verification gates

Before delivery:

- [ ] Output files exist in the correct project folder.
- [ ] HTML parses and referenced CSS/assets resolve.
- [ ] CSS braces/syntax checks pass.
- [ ] Local preview returns HTTP 200 when a server is used.
- [ ] Desktop render exists at the intended viewport.
- [ ] Mobile render uses a verified CSS viewport, not only screenshot dimensions.
- [ ] No true horizontal overflow: require `scrollWidth <= clientWidth`; when `innerWidth` differs, account for the vertical scrollbar instead of reporting a false defect.
- [ ] User-requested blank/placeholder regions contain no copied media.
- [ ] The page has been opened in Preview Pane when local preview is useful.

## Delivery report

Report:

- Client/project
- Objective
- Inputs read
- Output path
- Files created/updated
- Verification, including viewport and overflow evidence
- Preview instruction
- Assumptions / items needing confirmation
- Next action

Never claim completion from source inspection alone. A landing page is complete only after real rendering and responsive verification.

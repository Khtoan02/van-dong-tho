# Independent rebuild from a hosted page builder

Use this when a user wants to clone a page for long-term A/B testing but does not want the original builder runtime, branding, CDN, analytics, or form backend.

## First classify the deliverable

Do not conflate these two outputs:

- **Source mirror** - saves the published HTML and still runs the builder's runtime/CDN. It may be pixel-identical but is not independent.
- **Independent rebuild** - preserves rendered layout and copy while replacing runtime behavior, localizing visual assets/fonts, and removing builder dependencies.

When the user says "rebuild", "independent", or wants durable element-level A/B testing, deliver the independent form. State plainly if an intermediate artifact is only a mirror.

## Proven workflow

1. Save the published page as a reference archive, e.g. `builder-mirror.html`. Never overwrite the only reference.
2. Capture the original at desktop and mobile before edits.
3. Audit scripts, network hosts, images, fonts, lazy-load behavior, viewport code, form handlers, tracking, and runtime-injected UI.
4. Generate a static `index.html` from the archive:
   - Remove external and inline builder/analytics scripts.
   - Remove builder runtime preloads, API preconnects, and tracking noscript blocks.
   - Remove builder-controlled lazy-load body classes when they suppress backgrounds.
   - Keep static markup/CSS needed for pixel parity, even if legacy class names remain.
5. Localize page-owned images, icons, and fonts under `assets/`; maintain an `asset-manifest.json` mapping original URLs to local paths.
6. Recreate only required behavior with project-owned JavaScript:
   - Responsive viewport behavior.
   - Intersection-based reveal states.
   - Accessible form button keyboard behavior.
   - Native validity and a documented custom submit event or real CRM endpoint.
7. Inspect animation bootstrap CSS. Builder exports may contain selectors such as `opacity: 0 !important` until runtime adds a class. Reimplement the reveal class with equal/higher specificity and `!important` where required; verify computed opacity, not just class presence.
8. Serve locally and verify in a fresh browser context.

## Branding and dependency regression

Builder branding can be runtime-injected with a random class and exist only during a short time window. A screenshot taken after it disappears is a false pass.

Test at multiple times after navigation, especially around 0 s, 3-5 s, 10 s, and after scrolling. Assert all of the following:

- No DOM node whose computed `background-image` points to a builder branding asset.
- No visible "Powered by" text.
- Builder runtime globals are undefined.
- `performance.getEntriesByType('resource')` contains no unexpected external hosts.
- No external `<script src>` remains in the delivered HTML.

For LadiPage specifically, the runtime has been observed to inject a random-class fixed badge after roughly 3 seconds and remove it around 10 seconds. Search the computed background image for `by/ladipage.svg`; do not rely on a fixed selector.

## Visual verification

- Compare the first viewport at the exact original desktop and mobile canvas.
- Then scroll through every section in both reference and rebuild so lazy assets and reveal animations settle, return to the top, and capture full-page renders.
- Compare section crops for prominent images, timeline boxes, form/button, and footer.
- Treat tiny pixel differences from looping animation phase separately from structural differences.
- Run a mobile normal-height and short-height pass.

## Form safety

Do not silently preserve a production builder form endpoint in an independent rebuild. Either connect the approved CRM endpoint or prevent production submission and expose a documented integration hook, such as a custom `lead-submit` event. Never send a QA lead to production merely to prove the UI works.

## Delivery disclosure

Report separately:

- Whether legacy static class names remain.
- Whether any runtime/CDN/API dependency remains.
- Number and total size of localized assets.
- External resource hosts observed in a fresh load.
- Form backend status.
- Branding regression times tested.

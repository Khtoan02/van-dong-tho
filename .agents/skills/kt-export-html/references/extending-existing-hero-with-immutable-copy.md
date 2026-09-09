# Extending an Existing Hero with Immutable Copy

Use this when a project already contains an approved Hero and the user supplies exact long-form copy for all sections below it.

## Source-scope discipline

- Treat explicit exclusions such as `version/`, `archive/`, `old/`, or `backup/` as hard boundaries: do not open or reuse files inside them.
- File discovery may reveal excluded paths. Filter them out before selecting inputs and do not cite them as design references.
- Do not assume standalone `sections.css`, `sections.js`, QA images, or test scripts are active. Confirm that the current `index.html` actually links or imports them before trusting their content or screenshots.
- Preserve the approved Hero unless the user asks to change it. Add external section CSS/JS links and insert the new markup after the Hero rather than rewriting a large Hero file containing inline/base64 assets.

## Exact-copy structure

- Map every supplied paragraph to markup before styling.
- If the user requires a long founder narrative to remain one section, use exactly one `<section>` and create internal visual moments with `<div>` or `<article>` containers. Assert that no nested `<section>` occurs before the founder section closes.
- Styling may split a sentence across inline elements such as `<strong>`, but punctuation and spaces must remain visually exact. Example: `</strong>, chúng tôi`, not `</strong> , chúng tôi`.
- Avoid duplicating phrases as decorative chips unless the brief explicitly permits those phrases as diagram labels. Pure geometry should use `aria-hidden="true"`.
- CTA text that the brief explicitly permits may be reused; CTA destinations stay `#` until a real URL is supplied and must be reported as unresolved.

## Deterministic copy QA

A naive HTMLParser that joins every text node with spaces can create false failures around inline punctuation. For copy-presence checks:

1. Remove `<style>` and `<script>` blocks.
2. Strip remaining tags without inserting spaces at every tag boundary.
3. HTML-unescape the result.
4. Collapse actual whitespace only.
5. Check every required source string against that normalized visible text.

Also assert:

- one founder-story section;
- no nested section inside it;
- exact count/order of sections below Hero;
- no duplicate IDs;
- no missing local assets;
- balanced CSS braces and JavaScript syntax.

## Responsive visual QA

- Render representative deep sections at desktop, tablet, and mobile - not only the top of the page.
- Use CDP `scrollIntoView({behavior:'instant', block:'start'})`, then wait for paint before capture.
- Assert exact `innerWidth`; allow normal scrollbar width differences when comparing `documentElement.scrollWidth` to `innerWidth`, but fail when content width exceeds the viewport.
- Capture at minimum: founder opening, narrative contrast moment, principles, services, and lead magnet.
- Inspect component screenshots at readable scale. A full-page thumbnail hides wrapping, CTA placement, and oversized mobile visuals.

## Progressive motion

- Content is visible in base CSS.
- Add a root motion class only when IntersectionObserver is available and reduced motion is not requested.
- `prefers-reduced-motion` disables decorative orbit rotation and reveal transitions without hiding content.

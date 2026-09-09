# OpenRouter image generation and full-page QA

Use this recipe when a landing page needs a generated cinematic background and OpenRouter credentials are already configured for Antigravity.

## Provider-first image workflow

When a connected image MCP is unavailable, blocked, or out of credit, do not immediately replace the requested photorealistic asset with CSS illustration. Check whether the active Antigravity/OpenRouter setup exposes an image-output model.

1. Discover current models from `https://openrouter.ai/api/v1/models?output_modalities=image` or `https://openrouter.ai/api/v1/images/models`.
2. Use the current model slug returned by discovery rather than assuming an old marketing name. A verified example in August 2026 was `openai/gpt-5.4-image-2`.
3. Send `POST https://openrouter.ai/api/v1/images` with:
   - `model`
   - a detailed composition prompt
   - `n: 1`
   - `quality: "high"`
   - `aspect_ratio: "16:9"`
   - `output_format: "png"`
   - `background: "opaque"`
4. Authenticate with `Authorization: Bearer <OPENROUTER_API_KEY>`; resolve the key from the environment first, then the active profile/Antigravity `.env` without printing the secret.
5. Decode `data[0].b64_json` and save it under the project `assets/` directory. Save a separate non-secret metadata JSON containing model, dimensions/ratio, media type, usage/cost, output path, and byte size.
6. Inspect the generated image before integration. Check focal placement, negative space for copy, edge darkness, leading lines, realism, and mobile crop tolerance.
7. Link the image as a real CSS background and keep atmospheric overlays separate so they can be tuned without regenerating the asset.

### Prompt structure for cinematic hero backgrounds

Specify observable composition rather than only mood:

- Exact focal object and its viewport zone, e.g. desk/chair/laptop in the lower-center occupying about 20% width.
- Calm, low-detail negative space for headline placement.
- Side framing and darker lower corners.
- A bright central leading line or valley path.
- Explicit exclusions: people, text, logos, extra furniture, buildings, UI.
- Aspect ratio and photographic treatment.

## Reliable screenshot QA

For exact responsive screenshots, prefer Playwright CLI over raw Chrome `--window-size`, which may include browser chrome or produce a viewport different from the requested dimensions.

```bash
npx -y playwright screenshot \
  --channel chrome \
  --viewport-size "1440,1000" \
  --full-page \
  --wait-for-timeout 500 \
  "http://localhost:PORT/index.html?v=qa" \
  "qa/full-desktop.png"

npx -y playwright screenshot \
  --channel chrome \
  --viewport-size "390,844" \
  --full-page \
  --wait-for-timeout 500 \
  "http://localhost:PORT/index.html?v=qa" \
  "qa/full-mobile.png"
```

Use a cache-busting query after CSS revisions. Inspect both actual renders, not only HTTP status.

## Scroll-reveal progressive enhancement

Full-page screenshot tools capture the entire document without necessarily scrolling every section through the viewport. If `.reveal` starts at `opacity: 0`, offscreen sections can appear blank even though they would reveal during manual scrolling. This is also a content-access risk when JavaScript or IntersectionObserver fails.

Use visible-by-default content:

```css
.reveal { opacity: 1; transform: none; }
.reveal.animate-in { animation: sectionRise .75s ease both; }
@keyframes sectionRise {
  from { opacity: 0; transform: translateY(24px); }
}
```

IntersectionObserver should only add the enhancement class and never be required to make content readable:

```js
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('animate-in');
      observer.unobserve(entry.target);
    }
  });
});
```

## Mobile tab QA

A horizontally scrolling tab row can look clipped in static screenshots and obscure later options. For four short capability tabs on narrow mobile layouts, a 2-column grid is often more robust:

```css
@media (max-width: 480px) {
  .feature-tabs {
    display: grid;
    grid-template-columns: 1fr 1fr;
    overflow: visible;
  }
  .feature-tab { min-width: 0; width: 100%; }
}
```

Still retain `tablist`, `tab`, `tabpanel`, `aria-selected`, click handling, and arrow-key navigation.

## Motion runtime QA with Chrome CDP

Screenshots verify layout but not whether motion hooks execute. For a motion-heavy landing page, launch temporary headless Chrome with a remote-debugging port and assert computed runtime state through CDP.

Verify at least:

1. Scroll progress transform changes after `scrollTo(...)`.
2. A pointer move changes the hero parallax CSS variable on fine-pointer desktop state.
3. Orbit and chart computed `animationName` values match their intended keyframes.
4. Emulate `prefers-reduced-motion: reduce`, reload, then confirm perpetual animation is `none`, cursor glow is hidden, and content remains visible.

Useful launch flags:

```text
--headless=new
--remote-debugging-port=PORT
--remote-allow-origins=*
--user-data-dir=TEMP_PROFILE
```

Do not rely on headless Chrome's default media state. Explicitly call `Emulation.setEmulatedMedia` with `no-preference` before positive motion assertions and `reduce` before accessibility assertions. Run pointer assertions while the hero is still in view; scrolling first can create a false negative.

Keep motion compositional and cheap: `requestAnimationFrame`-throttled scroll progress, transform/opacity animation, pointer parallax only for `(pointer: fine)`, slow atmosphere/orbit movement, and visible-by-default content.

## Final verification

- HTTP 200 from the local server.
- Generated asset exists, has expected dimensions, and is referenced by HTML/CSS.
- Desktop and mobile full-page screenshots contain every section.
- No horizontal clipping at 390px.
- No duplicate IDs, missing in-page anchors, or missing local assets.
- Form UI does not imply a successful submission without a backend.
- Fictional/demo copy is clearly labeled when real brand/product facts are unavailable.
- `prefers-reduced-motion` is present.

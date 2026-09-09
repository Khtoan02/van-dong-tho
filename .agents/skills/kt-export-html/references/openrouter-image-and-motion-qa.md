# OpenRouter Image Generation and Motion QA

Use this reference when a landing page needs generated hero artwork or when CSS/JS animation must be verified beyond static screenshots.

## Generate image assets through OpenRouter

OpenRouter exposes a dedicated image endpoint even when Antigravity has no first-class OpenRouter image tool.

1. Discover current image models instead of assuming a model slug:
   - `GET https://openrouter.ai/api/v1/images/models`
   - or `GET https://openrouter.ai/api/v1/models?output_modalities=image`
2. Send `POST https://openrouter.ai/api/v1/images` with:
   - `model`
   - `prompt`
   - `n: 1`
   - `quality`
   - `aspect_ratio`
   - `output_format`
3. Decode `data[0].b64_json` and save it under the project `assets/` directory.
4. Save non-secret metadata beside it: model, dimensions/aspect ratio, media type, byte size, and returned usage/cost.
5. Load `OPENROUTER_API_KEY` from the active Antigravity environment or profile `.env`; never print or copy the key into project files.
6. Inspect the generated image before integrating it. Check focal-object placement, negative space for copy, edge darkness, leading lines, realism, and mobile crop.

A high-quality 16:9 hero prompt should explicitly reserve a calm upper-center copy area, put the focal tableau in the lower center, request darker edges, and prohibit text/logos/unwanted objects.

## Progressive animation rule

Content must remain visible without JavaScript or IntersectionObserver. Use animation as progressive enhancement:

```css
.reveal { opacity: 1; transform: none; }
.reveal.animate-in { animation: sectionRise .8s ease both; }
```

Do not make `.reveal` invisible by default. Full-page screenshots, print, slow scripts, or observer failures would otherwise produce blank sections.

## Motion design checklist

Prefer restrained, compositional motion:

- `requestAnimationFrame`-throttled scroll progress.
- Pointer parallax only under `(pointer: fine)`.
- Slow atmospheric drift, mist breathing, or background scale.
- SVG path draw animation for charts.
- Staggered section children, orbit motion, floating chips, and subtle CTA sheen.
- Avoid bounce easing and rapid perpetual movement.
- Use transforms and opacity where possible.

Always include `prefers-reduced-motion`. Stop perpetual animations, disable parallax/cursor glow, and restore stable transforms so centered elements do not jump.

## Runtime verification with Chrome CDP

Static screenshots prove layout but not motion. Use a temporary headless Chrome instance with remote debugging and evaluate computed styles at runtime.

Verify at least:

1. Scroll progress transform changes after `scrollTo(...)`.
2. Pointer movement changes the hero parallax CSS variable.
3. Orbit/chart computed `animationName` matches the intended keyframe.
4. After `Emulation.setEmulatedMedia` with `prefers-reduced-motion: reduce` and reload:
   - perpetual animation name is `none`;
   - cursor glow is `display: none`;
   - content remains visible.

Chrome may require `--remote-allow-origins=*` for a local CDP WebSocket client. Treat headless media defaults as test state: explicitly emulate `no-preference` before positive animation assertions and `reduce` before accessibility assertions.

## Verification order

1. HTTP 200 and asset existence.
2. Desktop and mobile screenshots.
3. Full-page screenshot to catch blank reveal sections.
4. Runtime CDP motion assertions.
5. Reduced-motion assertions.
6. Duplicate IDs, anchors, tab/panel counts, and local asset paths.

# Third-party embed performance patterns

Use this reference when Loom, YouTube, HighLevel/KT Funnel Builder forms, chat widgets, payment widgets, or other third-party iframes dominate initial page load.

## Diagnose before changing

Run Lighthouse mobile and desktop and retain before/after JSON. Record:

- Performance score, FCP, LCP, TBT, CLS.
- Initial transfer bytes and request count.
- Requests aggregated by domain.
- Whether the iframe loads video/HLS, large JS bundles, trackers, CAPTCHA, or form UI before the user reaches it.

A lightweight HTML/CSS page can still be slow when above-fold video and below-fold forms initialize eagerly.

## Click-to-load video

For a heavy video embed above the fold:

1. Save a local, compressed poster in WebP/AVIF.
2. Render an accessible `<button>` with the poster and play affordance.
3. Do not include the iframe in initial Light DOM.
4. On the first click, replace the button with the real iframe and enable autoplay/fullscreen.
5. Verify two states programmatically:
   - Initial: launch button exists, iframe does not.
   - After click: launch button is gone, iframe exists.
6. Preserve a fixed aspect ratio and explicit poster dimensions to avoid CLS.

Do not rely on `loading="lazy"` for an above-fold iframe: it may still load immediately.

## Lazy-load a native HighLevel/KT Funnel Builder form

For a form far below the fold:

1. Keep the official iframe markup in an inert `<template>` so it does not request anything initially.
2. Keep a normal Light DOM mount element near the intended form location.
3. Observe the mount with `IntersectionObserver` and a generous root margin (for example 800-1200px).
4. When near the viewport, clone the iframe from the template into the Light DOM mount.
5. Only then inject the official `form_embed.js`, exactly once.
6. Never place the live iframe in Shadow DOM and never replace the official resize/attribution bridge with a custom resizer.
7. Give the mount a neutral loading placeholder and a minimum height; after initialization, let the native iframe height expand the wrapper.

Verified runtime states:

- Initial page load: no form iframe and no official embed script.
- Near viewport: one iframe in Light DOM, one official embed script, `data-iframe-resizer-initialized` present, iframe width/height > 0.
- Parent URL retains path and query/UTM sentinel.

Local runtime verification does not prove production Form Submission, Contact, workflow, or attribution. Those still require deployment and an authorized test submission.

## Responsive image and font cleanup

- Convert active content images to WebP/AVIF and keep width/height attributes.
- Use `srcset`/`sizes` for an above-fold poster so mobile does not download a desktop-sized image.
- Keep below-fold images lazy and asynchronously decoded.
- Self-host the approved font when a remote font stylesheet creates a render-blocking request chain. For Vietnamese Roboto, include both Latin and Vietnamese WOFF2 subsets and preserve all required weights.
- Do not delete user-provided source images merely because optimized derivatives exist; exclude unused originals from deployment instead.

## Acceptance checks

- Lighthouse before/after reports use the same server, viewport preset, throttling, and page URL.
- Initial network does not contain the video/form third-party domains.
- Video loads after click.
- Form loads when scrolled near it and resizes without overlap.
- `scrollWidth === innerWidth` on mobile.
- CLS remains near zero.
- Full visual regression passes after font/image format changes.

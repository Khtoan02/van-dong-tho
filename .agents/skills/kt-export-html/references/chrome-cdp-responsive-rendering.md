# Chrome CDP Responsive Rendering

Use this when command-line `--window-size=390,844` produces a screenshot that looks cropped or wider than the requested mobile viewport.

## Why

On some Windows Chrome builds, headless `--window-size` controls the outer window but the CSS viewport can retain a larger minimum width. A 390 px screenshot may therefore be a crop of a roughly 500 px layout, creating false overflow and clipping findings.

## Reliable method

1. Start headless Chrome with a remote debugging port and a temporary user-data directory.
2. Pass `--remote-allow-origins=*` (or the specific origin) to avoid `403 Forbidden` on the WebSocket handshake.
3. Connect to the page target over CDP/WebSocket. On current Node versions with a global `WebSocket`, a dependency-free QA script can:
   - create a page with `PUT http://127.0.0.1:<port>/json/new?<encoded-url>`;
   - read `webSocketDebuggerUrl` from the response;
   - send numbered CDP messages and resolve them by matching response `id`;
   - wait for `Page.loadEventFired` before measuring or capturing.
4. Before reloading, call:

```json
{
  "method": "Emulation.setDeviceMetricsOverride",
  "params": {
    "width": 390,
    "height": 844,
    "deviceScaleFactor": 1,
    "mobile": true
  }
}
```

4. Reload, wait for fonts/images/entry animation, then use `Page.captureScreenshot`.
5. Evaluate and record real layout metrics:

```js
JSON.stringify({
  innerWidth,
  innerHeight,
  scrollWidth: document.documentElement.scrollWidth,
  scrollHeight: document.documentElement.scrollHeight
})
```

Pass mobile overflow QA only when `innerWidth === requested width` and `scrollWidth <= innerWidth`.

## Animation-safe screenshots and progressive enhancement

A screenshot taken immediately after navigation can capture elements during entry animations, often at `opacity: 0`. Either:

- wait long enough through CDP before `Page.captureScreenshot`, or
- use Chrome `--virtual-time-budget=3000` for a simple command-line desktop render.

Never diagnose missing copy from a render until the animation has settled.

More importantly, scroll-reveal content must be visible by default. Do not ship `.reveal { opacity: 0 }` as the base state and depend on JavaScript to restore visibility. Prefer one of these patterns:

- base CSS visible, then add a JavaScript-only pending class to elements that will actually animate; or
- keep the content visible and use transform-only enhancement if animation is not an acceptance criterion.

This prevents blank deep links, blank anchor screenshots, and unreadable pages when JavaScript is delayed or unavailable. Runtime QA should record the number of reveal elements whose computed opacity is `1` and compare it with the total reveal count.

## Deep-section mobile capture

Do not stop at the top viewport. For each long page, capture representative deep sections at the same exact mobile metrics:

1. Navigate to the page and set `Emulation.setDeviceMetricsOverride`.
2. Evaluate `document.querySelector(selector).scrollIntoView({block:'start', behavior:'instant'})`.
3. Wait for layout, fonts, images, and observers to settle.
4. Capture with `captureBeyondViewport:false`.
5. Inspect narrative copy, cards, prominent images/mockups, and CTA visibility independently.

Hash navigation alone is not a deterministic deep-section QA method: it can race layout, fonts, or reveal observers. Explicit `scrollIntoView` after load is more reliable.

## Deep-section desktop capture

The same `scrollIntoView` requirement applies to desktop deep-section QA. Do not rely on hash navigation (`#section-id`) in shell commands or browser URLs; the hash can be treated as a comment in unquoted shell strings, and even when quoted the scroll may race layout and reveal observers. Always use CDP `Runtime.evaluate` with `scrollIntoView({behavior:'instant',block:'start'})` and wait for paint before `Page.captureScreenshot`.

## Opaque generated product assets

When an image model does not return transparency, request a uniform pure-black background, place the asset over a black hero, and blend with `mix-blend-mode: screen`. If the source rectangle remains visible, add a soft `mask-image: radial-gradient(...)` around the subject. Verify the result from a render, because black levels may still differ.
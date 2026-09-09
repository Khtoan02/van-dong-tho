# LadiPage source mirror vs independent rebuild

Use this note when a client asks to "clone y nguyên" a live LadiPage landing page, especially for A/B testing.

## Two different deliverables

### Source mirror
- Save the published HTML and keep its generated DOM/CSS, LadiPage runtime, CDN assets, forms, analytics, and platform behavior.
- Fastest route to visual parity, but it is not independent frontend code.
- Runtime behavior can change by hostname, account status, verified domain, cookies, time, or platform API responses.
- Do not describe this as a rebuild. Report it explicitly as a LadiPage source mirror.

### Independent rebuild
- Recreate the rendered result in owned HTML/CSS/JS, download approved assets locally, and replace LadiPage form/tracking dependencies deliberately.
- Better default for long-term A/B testing because sections and elements can be edited without generated runtime coupling.
- Visual parity must be verified by screenshot comparison at the same viewports, scroll positions, loading states, and time checkpoints.

## Decision rule

When the request combines "clone y nguyên" with "A/B test từng phần tử", do not silently choose a source mirror. If the user has not specified architecture, state the two approaches and ask one short architecture question before building. Recommend independent rebuild for editable, deployable A/B variants. A source mirror is acceptable only when the user explicitly wants the fastest control snapshot or continued LadiPage dependency.

## LadiPage powered-by badge behavior

Published LadiPage runtime can inject a temporary `Powered by Ladipage` badge on unverified hosts such as localhost:

- Runtime constant points to `https://w.ladicdn.com/source/v3/by/ladipage.svg?v=1.0`.
- A random class is generated, so fixed class selectors are unreliable.
- The badge is typically inserted after about 3 seconds, fixed at bottom-left, animated for about 10 seconds, then removed.
- A screenshot captured after the badge disappears can falsely pass pixel parity while an interactive preview still exposes it.

Do not treat waiting for disappearance or hiding the badge as proof of an independent clone. The root dependency remains `ladipagev3.min.js`.

## Verification matrix

For a source mirror, verify at minimum:

1. Immediately after load.
2. Around 5 seconds after load, when delayed branding/config UI may appear.
3. After 15 seconds.
4. At top and at a mid-page scroll position.
5. In the actual Antigravity Preview Pane or intended browser, not only headless full-page capture.
6. Network/runtime dependency list, including LadiPage JS, CDN assets, form APIs, and analytics.

A useful deterministic DOM probe during the badge window is:

```js
[...document.querySelectorAll('body *')].filter((el) =>
  getComputedStyle(el).backgroundImage.includes('by/ladipage.svg')
)
```

## Delivery wording

Always report:

- Architecture: source mirror or independent rebuild.
- External runtime/CDN dependencies.
- Whether assets are local or remote.
- Whether the form and tracking remain tied to the original platform.
- What was actually tested, including timing checkpoints.

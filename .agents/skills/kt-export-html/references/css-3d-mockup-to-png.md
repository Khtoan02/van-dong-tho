# CSS 3D scene -> transparent PNG mockup (Windows recipe)

Render a standalone HTML scene (e.g. `templates/book-mockup-scene.html`) into a PNG with headless Chrome, then use the PNG in heroes / ads creatives. Verified on sếp's Windows host, Aug 2026.

## Render command (works)

```bash
CHROME="/c/Program Files/Google/Chrome/Application/chrome.exe"   # Edge also present: /c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe
OUT="C:\\Users\\Admin\\AppData\\Local\\Temp\\shots"
"$CHROME" --headless=new --disable-gpu --hide-scrollbars \
  --user-data-dir="C:\\Users\\Admin\\AppData\\Local\\Temp\\prof_$RANDOM" \
  --window-size=1000,1200 \
  --default-background-color=00000000 \
  --screenshot="$OUT\\mockup.png" \
  "http://localhost:PORT/scene.html?v=1"
```

- `--default-background-color=00000000` => transparent PNG (alpha kept, including a blurred floor-shadow div - great for compositing onto any background). Omit it (and add `?bg=dark` handled by the scene) for a baked background.
- Serve the scene over `python -m http.server`; do not use `file://` (fonts + cache behave worse).

## Pitfalls hit in practice

1. **`Failed to write file ... Access is denied (0x5)`**: happens with a relative `--screenshot` path and/or no `--user-data-dir`. Fix = absolute WINDOWS path with backslashes for the output AND a `--user-data-dir` under Temp. Do NOT `rm -rf` an old profile to reuse it (blocked as destructive) - just mint a new dir name per run.
2. **Stale screenshots (identical bytes after CSS edits)**: headless Chrome caches. Bump a `?v=N` query string AND use a fresh `--user-data-dir` every iteration.
3. **Off-center object in the PNG**: a rotated 3D object shifts inside its canvas. Fix in the SCENE (e.g. `margin-left: 40px` on the object, re-render) - never patch it in the target page with negative margins.
4. Spine legibility: with `rotateY(-32deg)` the spine is only a sliver; that is normal and looks like real book ads. Increase `--T` (thickness) before increasing the angle - too much `rotateY` distorts the cover.

## Mobile overflow debug probe (headless, no devtools)

When a screenshot shows clipping but you cannot tell which element overflows, wrap the page in an iframe probe and dump the DOM:

```html
<iframe id="f" src="/index.html" style="width:390px;height:900px;border:0"></iframe>
<pre id="out"></pre>
<script>
f.onload = () => {
  const d = f.contentDocument, w = f.contentWindow, out = [];
  out.push('body.scrollWidth=' + d.body.scrollWidth, 'innerWidth=' + w.innerWidth);
  d.querySelectorAll('*').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width > w.innerWidth + 1) out.push('WIDE: ' + el.tagName + ' w=' + Math.round(r.width));
  });
  document.getElementById('out').textContent = out.join('\n');
};
</script>
```

Run with `--dump-dom --virtual-time-budget=4000` and grep the `<pre id="out">` block. In the Free PR session this proved nothing overflowed (`scrollWidth 375 < innerWidth 390`) - the "clipped" H1 was just long uppercase words at too large a `clamp()`, fixed by smaller mobile type + an explicit `<br>` shown only under 900px.

## Using the PNG in the hero

- Plain `<img src="...transparent.png">`, `width: min(500px, 100%)`, no extra drop-shadow filter (the PNG already carries its floor shadow).
- Gentle float: `@keyframes bookFloat { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-14px)} }`, 7s ease-in-out infinite, `animation-play-state: paused` on hover.
- Mobile: `animation: none`, `margin: 0 auto`, width ~`min(340px, 88vw)`.
- `prefers-reduced-motion`: disable the float entirely.

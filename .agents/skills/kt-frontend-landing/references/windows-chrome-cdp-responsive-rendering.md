# Authoritative mobile rendering with Chrome CDP on Windows

## Why this exists

Screenshot pixel dimensions alone do not prove the browser used the same CSS viewport. Narrow command-line Chrome captures on Windows can be produced from a wider minimum browser viewport and then cropped. The image may look like a responsive failure even when the requested `--window-size` appears correct.

The durable rule is not to distrust Chrome CLI categorically. It is to verify the effective viewport instead of inferring it from the PNG dimensions.

## Reliable evidence

Use Chrome DevTools Protocol (CDP):

1. Launch an isolated headless Chrome with `--remote-debugging-port=<port>` and a temporary `--user-data-dir`.
2. Open a target through `/json/new?about:blank`.
3. Call `Emulation.setDeviceMetricsOverride` with exact width, height, scale factor, and mobile mode.
4. Navigate to the local page.
5. Wait until `document.readyState === 'complete'`.
6. Capture the screenshot with `Page.captureScreenshot`.
7. Read and record:
   - `window.innerWidth`
   - `window.innerHeight`
   - `document.documentElement.scrollWidth`
   - `document.documentElement.scrollHeight`
8. For a normal responsive page, require `scrollWidth == innerWidth`.

Use the reusable script at `scripts/render_viewports_cdp.py` after starting Chrome with remote debugging.

## Example Chrome launch

```bash
'C:/Program Files/Google/Chrome/Application/chrome.exe' \
  --headless=new \
  --disable-gpu \
  --remote-debugging-port=9333 \
  --remote-allow-origins=* \
  --user-data-dir='C:/Users/Admin/AppData/Local/Temp/landing-page-cdp' \
  about:blank
```

Run long-lived Chrome through the background-process tool rather than appending `&`.

## Example render

```bash
python scripts/render_viewports_cdp.py \
  --url http://127.0.0.1:4173 \
  --cdp http://127.0.0.1:9333 \
  --out-dir renders \
  --viewport desktop:1717x916 \
  --viewport mobile:390x844
```

Expected stdout is JSON containing viewport and scroll metrics for every render. Treat a mismatched mobile `scrollWidth` as a real layout defect and inspect the widest child; do not merely hide overflow.

## Proven repair sequence for long hero copy

When media covers a long heading line:

1. Confirm the heading itself crosses the grid track.
2. Keep the approved font family and weight.
3. Tune font size, letter spacing, and column ratio until deliberate desktop lines fit.
4. Preserve `min-width: 0` on the grid child.
5. Restore natural wrapping at mobile breakpoints.
6. Rerender desktop and true CDP mobile viewports.

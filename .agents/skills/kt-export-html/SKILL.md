---
name: kt-export-html
description: Use when exporting coded landing pages as copy-paste HTML for app.gohighlevel.com / Funnel Builder/GHL Builder. Enforces production-safe assets, native form attribution, runtime and mobile QA.
---

# Landing Page Frontend (Coder Agent)

Use when coding, redesigning, or fixing landing pages / sales pages / opt-in / webinar / thank-you pages / websites for agency clients or KT Funnel Builder internal marketing.

## Workflow

1. **Read context first.** For client work: `./clients/{client}/README.md` and `_agent/` files. For KT Funnel Builder internal: `./agency/_agent/working-rules.md` + brand KB at `00_Agency/00_Knowledge-Base/02_Brand/brand-positioning.md` (authoritative for brand claims - do not duplicate brand facts into skills).
2. **Pick output folder.** Client deliverables → `01_Clients/{client}/...`. KT Funnel Builder internal projects → `00_Agency/02_Projects/{project-name}/` (website redesigns live in their own project folder, e.g. `website-redesign/`).
3. **Build** a single self-contained `index.html` (embedded CSS/JS, design tokens in `:root`, semantic HTML, responsive) unless the task calls for a repo stack.
4. **Verify** (see Verification section - browser_navigate cannot preview local files).
5. **Report** in the Coder Delivery format from the system prompt. In Antigravity IDE, open the localhost page in Preview Pane and include the direct file path/restart command as fallbacks; do not assume a chat hyperlink to localhost will open correctly.

## Xuất file HTML sẵn sàng cho app.gohighlevel.com / Funnel Builder/GHL Builder

Dùng quy trình này khi chuyển landing page đang chạy độc lập thành một file để copy toàn bộ vào **một Custom HTML/JS element** trên app.gohighlevel.com / Funnel Builder hoặc GHL Builder.

### 1. Tạo deployment artifact riêng

- Không ghi đè `index.html` hoặc source đã duyệt nếu sếp không yêu cầu.
- Xuất một file riêng có tên rõ ràng như `gohighlevel-ready.html` hoặc `gohighlevel-ready-tracking-safe.html`.
- Nếu có generator, sửa/tạo generator làm source of truth và build lại artifact; không vá riêng file generated.
- Fragment để dán vào builder không chứa `<!doctype>`, `<html>`, `<head>` hoặc `<body>` trừ khi builder đích yêu cầu rõ ràng.
- Không còn đường dẫn local như `assets/`, `D:/`, `C:/Users/...`; dùng public CDN URL, data URI hợp lý hoặc asset đã upload lên app.
- Xóa annotation/transcript artifact như `@url:`, `Context Warnings`, markdown fence và lời giải thích ngoài code.

### 2. Chọn đúng kiến trúc form trước khi xuất

- Nếu cần native Form Submission, workflow `Form Submitted` và attribution của HighLevel / Page Builders, dùng native iframe embed lấy nguyên từ Form Builder.
- Nếu cần kiểm soát trực tiếp từng field/payload bằng HTML, dùng workflow External Tracking hoặc server-side bridge tương ứng; không giả vờ form frontend-only đã kết nối CRM.
- Không để custom submit handler, fake success state hoặc External Tracking script chạy song song với native iframe nếu business không chủ ý tạo hai luồng capture.

### 3. Native form attribution - quy tắc bắt buộc

`form_embed.js` không chỉ resize iframe. Script tìm iframe bằng `document.querySelectorAll('iframe')`, đọc `document.location.href`, query/UTM và `document.referrer`, rồi truyền context trang cha cho form. Vì vậy:

1. Native iframe phải tồn tại trong **Light DOM** và có thể tìm thấy bằng:

```js
document.querySelector('iframe[data-form-id="FORM_ID"]')
```

2. Không đặt iframe trực tiếp trong Shadow Root.
3. Nạp script chính thức đúng một lần:

```html
<script src="https://link.leandigi.vn/js/form_embed.js"></script>
```

4. Không tự gọi `window.iFrameResize(...)`. Resize thủ công không thay thế attribution message handler và có thể khởi tạo iframe sai thứ tự.
5. Giữ nguyên các thuộc tính embed quan trọng: `src`, `id`, `data-layout`, `data-form-id`, `data-layout-iframe-id`, `data-form-name`, `data-height` và `title`.
6. Iframe nên tồn tại ngay khi trang tải; chỉ ẩn/hiện modal. Không tạo iframe bằng `innerHTML` sau khi `form_embed.js` đã chạy.

### 4. Khi UI cần Shadow DOM - dùng Light DOM + named slot

Đặt iframe làm child Light DOM của host:

```html
<div id="landing-app">
  <iframe
    slot="ghl-form"
    src="https://link.leandigi.vn/widget/form/FORM_ID"
    id="inline-FORM_ID"
    data-form-id="FORM_ID"
    data-layout-iframe-id="inline-FORM_ID"
    title="FORM_NAME">
  </iframe>
</div>
```

Trong Shadow template:

```html
<div class="crm-form">
  <slot name="ghl-form"></slot>
</div>
```

HighLevel hiện tự bọc iframe inline theo cấu trúc gần giống:

```text
host
└── .ep-iFrameContainer
    └── .ep-wrapper
        └── iframe
```

Wrapper được tạo sau khi `form_embed.js` chạy và làm iframe không còn là direct child của host. Vì vậy cần chuyển `slot="ghl-form"` sang **Light DOM child ngoài cùng mà HighLevel tạo**, không chỉ `.ep-wrapper`:

```js
const assignGhlFormSlot = () => {
  const iframe = host.querySelector('iframe[data-form-id="FORM_ID"]');
  if (!iframe) return;

  let directChild = iframe;
  while (
    directChild.parentElement &&
    directChild.parentElement !== host
  ) {
    directChild = directChild.parentElement;
  }

  if (directChild.parentElement === host) {
    directChild.setAttribute('slot', 'ghl-form');
  }
};

const formSlotObserver = new MutationObserver(assignGhlFormSlot);
formSlotObserver.observe(host, {
  childList: true,
  subtree: false
});
assignGhlFormSlot();
```

CSS trong Shadow Root phải chấp nhận cả iframe trước khi khởi tạo và wrapper sau khi HighLevel khởi tạo:

```css
.crm-form slot[name="ghl-form"]::slotted(iframe),
.crm-form slot[name="ghl-form"]::slotted(.ep-wrapper),
.crm-form slot[name="ghl-form"]::slotted(.ep-iFrameContainer) {
  display: block;
  width: 100%;
  border: 0;
}
```

Đặt fallback style trực tiếp trên iframe hoặc bằng Light DOM CSS vì `::slotted()` không xuyên qua `.ep-iFrameContainer` để style iframe cháu. Sau runtime, để `form_embed.js` sở hữu chiều cao chính thức.

Nếu không cần style isolation, ưu tiên **Light DOM + CSS namespace** thay cho Shadow DOM. Đây là kiến trúc đơn giản và ít rủi ro nhất.

### 5. Static QA bắt buộc cho artifact

- Chính xác một native iframe cho mỗi form cần hiển thị.
- `src`, `id`, `data-form-id`, `data-layout-iframe-id` khớp cùng Form ID.
- `form_embed.js` đúng một lần.
- Không có `window.iFrameResize(` thủ công.
- Không còn local asset path hoặc annotation rác.
- Không có duplicate HTML `id` thật.
- CTA mở đúng modal; modal đóng bằng nút, backdrop và Escape nếu design yêu cầu.
- Build hai lần cho cùng output phải idempotent, không nhân iframe/script.

### 6. Runtime QA bắt buộc

Serve bằng localhost và kiểm tra trong browser thật:

1. `document.querySelectorAll('iframe[data-form-id="FORM_ID"]').length === 1`.
2. Iframe có `data-iframe-resizer-initialized` sau khi script chính thức chạy.
3. Nếu dùng Shadow slot, `slot.assignedElements()[0]` phải là Light DOM container có chứa iframe.
4. Click CTA thật để mở modal; iframe phải có `getBoundingClientRect().width > 0` và `height > 0`.
5. Form hiển thị đủ field và CTA, không bị cắt đáy hoặc tràn ngang.
6. Kiểm tra desktop và mobile thật tối thiểu 390x844; assert `innerWidth === 390` và `documentElement.scrollWidth === 390`.
7. Chụp screenshot popup/form ở desktop và mobile, không chỉ kiểm tra HTTP 200.
8. Không submit lead production chỉ để kiểm tra giao diện.

### 7. Attribution QA sau publish

Dùng cửa sổ ẩn danh, contact mới và URL production có path + query sentinel:

```text
/landing-path?utm_source=lp_qa&utm_medium=test&utm_campaign=attribution_qa
```

Submit đúng một lần khi sếp cho phép, sau đó xác minh trong native Form Submission và Contact:

- Page URL giữ đúng domain + path.
- Query/UTM sentinel được nhận đúng.
- Source không fallback sang `direct` khi URL có `utm_source`.
- Workflow chạy đúng một lần.

Không dùng contact hoặc browser session cũ để kết luận vì first/latest attribution, sticky contact và cookie cũ có thể làm sai kết quả. Không tuyên bố attribution production PASS nếu mới chỉ preview local; local QA chỉ chứng minh kiến trúc và runtime sẵn sàng.

### 8. Delivery report bắt buộc

Báo cáo phải ghi rõ:

- File nào để copy vào builder.
- File nguồn nào không bị chỉnh sửa.
- Form ID và domain embed đã dùng.
- Static/runtime/mobile QA thực tế.
- Có hay chưa có production submission QA.
- Hướng dẫn: copy **toàn bộ file** vào một Custom HTML/JS element duy nhất.

### When extending an existing hero into a full landing page

When sếp supplies a hero section and asks for the remaining sections, treat the hero as the design contract and content source:

1. **Honor source exclusions before reading.** If sếp says not to access `version/`, `archive/`, `old/`, `backup/`, or another legacy folder, treat it as a hard boundary. Discovery may reveal those paths, but do not open, reuse, or cite their contents. Filter them out before selecting inputs.
2. **Confirm which artifacts are active.** Do not assume nearby `sections.css`, `sections.js`, QA images, or scripts belong to the current page. Verify that the active `index.html` actually links/imports them before trusting or reusing them.
   - Re-read the relevant `<head>`, post-hero markup, and script imports immediately before the first write. A file can change between discovery and implementation because another process or prior workflow is still updating it. If the active page has gained a section bundle, reassess and replace one coherent block - never append a second homepage beneath it.
   - When changing from an old section bundle to a new one, update the HTML imports, validation script, and render script together. Then prove the old bundle is no longer referenced and the new CSS/JS each load exactly once.
3. **Read the active hero file completely** - extract its `:root` tokens, font stack, CTA geometry, grid padding (`--pad-x`), and motion patterns. Do not invent a new design system.
4. **Use the exact same horizontal padding token** (`--pad-x`) for every subsequent section shell. Do not add an arbitrary `max-width` wrapper that visibly narrows later sections on wide screens.
5. **Reuse the hero CTA system** for all later buttons: same pill radius, same padding, same arrow chip, same hover lift/shadow. Invert colors only for contrast (e.g. gold card → black button), never change geometry.
6. **Keep the founder/story letter simple** when the reference is plain portrait-left / letter-right. Do not add manifesto cards, numbered pain lists, badges, decorative timelines, or extra CTAs. Use a clearly labeled placeholder if no real portrait is available.
7. **Section order follows the supplied copy exactly.** Do not shorten, summarize, or reorder paragraphs when sếp says "đừng chỉnh sửa hay rút gọn nội dung".
8. **Verify the full page** with desktop, tablet, and mobile screenshots at the exact viewport, including deep-section captures via CDP `scrollIntoView` (not hash navigation).

For immutable long-form copy, one-section founder narratives, active-artifact checks, deterministic visible-text QA, and desktop/tablet/mobile deep-section verification, see `references/extending-existing-hero-with-immutable-copy.md`.

## Design standards for sếp (learned from his feedback)

Sếp rejected a conventional hero + 3-card layout as not creative enough. Default to **distinctive, creative compositions**:

- Asymmetric hero layouts (text block with brand-colored left border + large 3D/floating visual card on the other side), not centered-stack heroes.
- Marquee strips, sticky-sidebar section layouts, horizontal-scroll card rows.
- 3D transforms (ebook covers with spine, tilted cards that straighten on hover), floating badge elements with slow float animation, cursor glow, scroll-reveal via IntersectionObserver, per-line slide-up headline animations.
- Respect `prefers-reduced-motion`.

**Font:** sếp asked for **Roboto** in frontend deliverables ("dùng font Roboto cho anh thôi") - use Roboto (300-900) as the default **body and UI** family unless he says otherwise. Do not force Roboto onto every display heading when supplied hero artwork uses a literary, hand-drawn, or expressive face. Inspect the hero first and choose a Vietnamese-capable display font that harmonizes with it; render real Vietnamese diacritics and wrapping on desktop/mobile before committing. A validated literary pairing is Cormorant Garamond 600/700 for headings + Roboto for body/UI.

**Narrative-first layouts:** analyze each section's role before selecting a component. Story openings and continuations should read like chapters with deliberate beats, narrow reading widths, and imagery used as a pause - not consecutive generic image-left/copy-right grids. Reserve cards for concept grouping, lists for benefits, visual silence for reflection, and split facts/form layouts for ordering. See `references/editorial-storytelling-and-deep-page-qa.md`.

**Reference simplicity is a constraint:** when sếp supplies a plain portrait-left / letter-right reference and asks for a simple text letter, match that restraint. Do not add manifesto panels, numbered pain lists, badges, decorative timelines, or extra CTAs. Use a real portrait when available; otherwise use a clearly labeled placeholder rather than another person's image. For this pattern, plus responsive animated hero/logo overlap and exact-aspect-ratio QA, see `references/hero-overlap-and-simple-founder-sections.md`.

**KT Funnel Builder brand palette:** black `#0a0a0a` family + yellow `#FFD700` (hover `#E6C200`). Keep brand colors when redesigning - he explicitly asks for this.

### Hero-derived page contract

After the hero is approved, treat it as the design contract for the rest of the landing page:

- **One CTA system per page.** Reuse the hero button's geometry, radius, arrow chip, typography, padding, and hover behavior in later sections. Invert colors for contrast when needed, but do not invent section-specific button shapes unless sếp explicitly requests a second system.
- **One full-width content grid.** Ordinary sections, service cards, offer sections, and footer should share the hero's left/right content edges. Use the same horizontal padding token and `width:100%`; avoid an arbitrary later-section `max-width` that visibly collapses the page on wide screens.
- **Intentional narrow exceptions only.** A storytelling/founder-letter section may use a centered measure around 70% of the hero content grid. Return to the full hero grid for grouped concepts, services, offers, and footer.
- Verify the contract numerically with `getBoundingClientRect()` at the user's actual viewport, then inspect pixels. Compare each shell's `left`, `right`, and `width` to the hero's inner content grid.

For the validated grid ratios, CTA reuse, simple founder layout, responsive hero-marquee overlap, and exact-viewport checks, see `references/hero-overlap-and-simple-founder-sections.md`.

**Copy rules:** Vietnamese, hyphen-minus `-` instead of em dash. Never invent metrics, testimonials, client logos, or claims - use clearly-labeled placeholders (e.g. "Client 1") and flag them in the report as needing real assets.

### Clone architecture must be explicit

"Clone y nguyên" can mean either a **source mirror** (reuse generated platform HTML/runtime) or an **independent rebuild** (owned HTML/CSS/JS that matches the rendered result). These are not interchangeable.

- When the goal includes long-term A/B testing of individual elements, recommend an independent rebuild and do not silently ship a source mirror.
- If architecture is not explicit, ask one short question choosing between source mirror and independent rebuild before building; this ambiguity materially changes dependencies, editability, deployment, and QA.
- If using published page source, report it as a source mirror, list every retained runtime/CDN/form/tracking dependency, and never describe it as rebuilt code.
- For an independent rebuild, approved source assets may be downloaded locally, but platform-generated runtime, branding, forms, and analytics must be replaced deliberately rather than hidden.
- Visual parity still overrides redesign and generic usability improvements unless the user separately requests fixes. Preserve original spacing and responsive quirks, then prove parity with same-environment desktop/mobile screenshot diffs.
- Do not let a final delayed screenshot hide transient runtime UI. Verify interactive pages immediately, near 5 seconds, after 15 seconds, and at top plus mid-page scroll in the actual Preview Pane or target browser.
- LadiPage may inject a random-class `Powered by Ladipage` badge on unverified hosts after a delay. A fixed selector, waiting for disappearance, or a screenshot taken after it disappears is not sufficient verification.

See `references/ladipage-mirror-vs-independent-rebuild.md` for architecture decisions, dependency reporting, the deterministic badge probe, and timing matrix. See `references/independent-rebuild-from-hosted-builder.md` for the broader builder-independent extraction workflow, local asset manifest, animation bootstrap recovery, fresh-load network assertions, and safe form integration hook. See `references/exact-landing-clone-parity.md` for screenshot capture and critic-evidence details.

### Exact-copy override

When the user says supplied Word copy must be used exactly, that instruction overrides any general permission to shorten content for layout:

1. Treat the `.docx` as the single source of truth and extract content programmatically rather than retyping long passages.
2. Preserve every non-empty source paragraph verbatim. Do not summarize, rewrite or add marketing copy.
3. Put long content behind accessible details, tabs, chapters or carousel panels when needed, but keep the complete text in the HTML.
4. Use one generator for multiple variants so factual copy and prices cannot drift between versions.
5. Before delivery, compare parsed visible HTML text against every non-empty Word paragraph and report the exact missing count. A page is not complete unless the missing count is zero.
6. UI labels required for forms or navigation may be added, but they must not introduce claims. If an order form has no backend, do not imply successful submission.

See `references/exact-word-copy-and-order-forms.md` for the extraction, deterministic comparison, multi-version layout and order-section recipe. For stdlib DOCX parsing with embedded line breaks, explicit editorial-instruction exclusions, long-page mobile raster artifacts, deep-section CDP captures, and transparent-mockup spacing, see `references/full-page-word-build-and-mobile-raster-qa.md`.

## Verification (local files)

`browser_navigate` refuses `file://` and `localhost`/private URLs **by design** - do not retry or treat as a bug. Instead:

1. Serve the folder: `terminal(background=true, notify_on_complete=true)` with `cd "<project-folder>" && python -m http.server 8080`.
2. Confirm in a follow-up foreground call: `curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/index.html` → expect `200`.
3. In Antigravity IDE, open the verified localhost URL directly in the Preview Pane with `open_preview`; do not rely on a clickable localhost link in chat, because that link handler has repeatedly failed for sếp even when curl returns HTTP 200. Also report the direct file path and restart command as fallbacks.
- For exact responsive screenshots on Windows Chrome headless, do not trust `--window-size=390,...`: Chrome can clamp the inner width to about 504px and a later crop produces fake mobile clipping. Launch Chrome with a remote-debugging port, use CDP `Emulation.setDeviceMetricsOverride` for the exact viewport, assert `innerWidth` and `documentElement.scrollWidth`, then call `Page.captureScreenshot`. See `references/chrome-cdp-responsive-rendering.md`.
- When connecting to Chrome CDP via WebSocket, pass `--remote-allow-origins=*` (or the specific origin) to avoid `403 Forbidden` handshake errors on the `webSocketDebuggerUrl`.

## Design QA with Impeccable detector

The `impeccable` npm package (v3.5+) ships a deterministic design detector that runs with no AI/API key - useful as an automated QA pass before delivery. Verified working on this machine.

- Run on any HTML/CSS file: `npx -y impeccable detect <file-or-dir>` (exit code 2 = findings; `--json` for machine-readable output).
- Useful flags: `--scope type,layout`, `--viewport 390x844` (mobile pass), `--no-advisory`.
- It catches: low contrast (WCAG AA), overused fonts, AI-tell palettes (purple/cyan gradients), nested cards, bounce easing, etc.
- **Tension with sếp's prefs:** its `overused-font` rule flags Roboto (his chosen default). Treat font findings as advisory - brief/client wins over detector. Contrast and layout findings are real defects, fix those.
- Full skill (24 commands like `/audit`, `/critique`, `/polish`, `/bolder`) is built for Cursor/Claude Code harnesses, not Antigravity - but `detect` works standalone from any terminal. See `references/impeccable-detector.md` for install modes and command list.

## Multi-direction concept builds

When a brief asks for several visual directions (`v1/`...`vN/`), treat them as independently committed concepts rather than color themes over one generic page.

1. Extract shared factual data first: titles, prices, descriptions, CTA copy, asset filenames, and forbidden claims. Keep this source of truth separate from direction-specific presentation.
2. Give every direction a distinct hero composition, palette, type treatment, section rhythm, product explorer, author treatment, and closing offer. Shared narrative order is acceptable; identical visual structure is not.
3. For content-heavy collections, prefer an accessible tabbed explorer over a giant uniform card grid. Include `tablist` / `tab` / `tabpanel` roles, `aria-selected`, keyboard arrow navigation, and visible focus.
4. If multiple self-contained pages share factual content, use a checked-in generator script with shared data plus direction-specific CSS/hero markup. Keep every delivered `vN/index.html` directly runnable.
5. Never invent a CTA destination. If the checkout/order URL is missing, use an in-page placeholder and flag the missing destination in the delivery report.

### Visual verification for multiple versions

- Audit each version for HTTP 200, expected product/tab count, CTA count, duplicate IDs, missing local assets, responsive rules, focus styling, and reduced-motion support.
- For a device mockup with real slides, verify alpha inside the display opening rather than trusting RGBA metadata, cut a true transparent screen when needed, and derive the CSS screen bounds from the exact same pixel coordinates used for the alpha cutout. Test settled slides and mid-transition states separately through CDP. See `references/transparent-device-mockup-carousel.md`.
- Render actual desktop and mobile screenshots for every version. A headless Chromium-family browser can render localhost directly; discover the executable instead of assuming one fixed installation path.
- For a cinematic hero without final product photography, use a licensed/local environment photo plus a restrained CSS foreground product tableau; see `references/cinematic-css-product-hero.md` for the composition, responsive, accessibility, copy-safety, and verification recipe.
- Build desktop and mobile contact sheets to compare directions side by side. Inspect the first viewport for clipped headlines, hidden CTA, broken crops, weak contrast, and concepts that have drifted into the same visual system.
- For several directions switched inside one shared document, click the real switch controls during QA rather than setting classes only. Assert the root version state, inspect every direction at each breakpoint, and verify the switcher itself does not cover deep-section CTAs. On mobile, prefer a compact right-edge numeric dock over a wide bottom bar when the control must remain fixed.
- Mobile hero QA must be screenshot-based at both a normal viewport (for example 390x844) and a short viewport (for example 390x700). Wide editorial heroes often clip because grid children retain max-content width or direction CSS overrides shared mobile rules. Useful safeguards include `min-width: 0`, an explicit mobile copy width such as `calc(100vw - 40px)`, restrained mobile display sizes, and direction-specific image positioning. Do not judge only whether everything technically fits: inspect the vertical rhythm from logo → title/support copy → CTA → product/device visual. Sếp prefers the full visual above the fold with a tight, balanced gap; when a mockup feels disconnected, scale it down and reduce its wrapper height/vertical centering space before merely changing `top`. Re-render both viewport heights after each fix.
- See `references/multi-direction-landing-build.md` for separate-page direction builds. See `references/switchable-multi-version-page-qa.md` for shared-DOM version switching, CSS-specificity traps, mobile control placement, animated overflow probes, and the evidence set.

## Generated hero assets and motion QA

When a landing page needs original cinematic artwork, check the configured OpenRouter image-output models before falling back from requested photorealistic art to CSS illustration. Keep scroll-reveal content visible by default, and for motion-heavy pages verify real animation plus `prefers-reduced-motion` behavior with runtime Chrome CDP assertions rather than screenshots alone. See `references/openrouter-image-generation-and-full-page-qa.md` for the validated generation, full-page screenshot, mobile-tab, and motion QA recipe.

## Pitfalls

- **Direction CSS specificity:** a direction selector such as `body[data-version="3"] .ebook-panel` can beat a later shared mobile `.ebook-panel` rule because specificity outranks source order. Put direction-specific mobile overrides inside the breakpoint with matching or higher specificity, then click every real version control and inspect the generated/runtime page - not only the source or default direction. See `references/switchable-multi-version-page-qa.md`.
- **Fixed comparison controls can hide conversion UI:** a wide bottom version dock may cover mobile CTA buttons and long copy. Capture the deepest offer/service states with the control visible; if it overlaps, use a compact right-edge numeric dock or a non-fixed control rather than adding arbitrary section padding.
- **Animated ornaments can create root overflow:** expanding hero waves or marquee children may increase `documentElement.scrollWidth` after animation starts even when `body` is clipped. Probe element rectangles after paint for every direction and viewport; if visually appropriate, clip overflow at `html` as well as the component boundary.
- **HTTP checks are not visual QA:** HTTP 200 and valid asset paths cannot reveal clipped headlines, off-screen CTA, or poor hero crops. Render screenshots whenever layout is part of the deliverable.
- **QA scripts are part of the page architecture:** after replacing section IDs, counts, CSS/JS bundle names, CTA protocols, or screenshot targets, update deterministic validators and CDP render scripts in the same change. Local-reference audits must exempt legitimate schemes such as `tel:`, `mailto:`, `data:`, fragment links, and `http(s):`; otherwise a valid CTA is misreported as a missing file. Never weaken QA merely to make stale assertions pass - rewrite expectations to describe the delivered page, then run both structural validation and exact-viewport rendering.
- **Match the user's actual viewport before claiming a layout fix.** When feedback includes a screenshot, inspect its pixel dimensions and render that exact width/height plus one contrasting aspect ratio. A fix tuned only at `1440x1000` can fail on a wide-short viewport such as `1875x945`. Verify the semantic vertical order in pixels - CTA, checklist/proof, then marquee - and do not report success from a different viewport.
- **For hero ornament + marquee overlaps, move the ornament, not the content rail.** Keep the marquee near the bottom in normal flow with only a small overlap offset; use stacking, visible overflow, wave scale, and negative animation delays so the rings cross over it. Large fixed negative margins can pull the rail into CTA/checklist content. See `references/hero-marquee-overlap-responsive-qa.md`.
- **Scroll-reveal must be progressive enhancement.** Keep long-form content visible in base CSS; never rely on JavaScript to change every `.reveal` element from `opacity:0` to readable. For deep-page QA, record visible reveal count versus total, then explicitly `scrollIntoView` representative narrative, service, mockup, and CTA sections before viewport screenshots. Hash-only captures can race layout and observers. See `references/chrome-cdp-responsive-rendering.md`.
- **Deep-section QA requires explicit scroll, not hash navigation.** When capturing mobile or desktop screenshots of specific sections below the fold, use CDP `Runtime.evaluate` with `document.querySelector(selector).scrollIntoView({behavior:'instant',block:'start'})` and wait for paint before `Page.captureScreenshot`. Hash-only navigation (`#section-id`) can race layout, fonts, and reveal observers, producing screenshots of the wrong viewport region.
- **A downscaled full-page screenshot is not sufficient image QA.** It can hide severe aspect-ratio distortion and an oversized mobile crop. For every prominent mockup/portrait, capture the component or section at the exact target viewport and inspect it at readable scale. Measure `getBoundingClientRect()`, `naturalWidth/naturalHeight`, computed `width/height`, `aspect-ratio`, `object-fit`, and `object-position`; compare rendered and natural ratios numerically. HTML `width`/`height` attributes or legacy CSS can leave a fixed height while responsive CSS shrinks only the width - explicitly set `height:auto` for contained transparent mockups. For mobile portraits, avoid inheriting source-image height; use an intentional compact frame and verified `object-position`. Patch the generator/source of truth, rebuild, then re-check both desktop and mobile so the fix survives regeneration.

- **`npx impeccable install` is interactive** - it hangs and times out in a non-TTY terminal. Pass `--scope=project --providers=cursor` (or another provider) to skip the prompts.
- **No `&` backgrounding in foreground terminal calls** - it is rejected. Use `terminal(background=true)` for the http server, then run curl in a separate foreground call.
- **First draft too generic = rework.** Spend the layout budget on composition (asymmetry, scroll behavior, 3D/motion details) before polishing colors - sếp judges creativity by layout first.
- Keep server processes noted so they can be killed/restarted when sếp asks for the next iteration. After a rewrite in Antigravity IDE, refresh or reopen the same localhost URL in Preview Pane rather than sending another chat hyperlink.
- When packaging for GoHighLevel or another builder, create a separate deployment artifact if the user says not to touch the current source. Remove document wrappers, eliminate local asset paths, isolate styles/behavior, and test the generated fragment itself inside a neutral builder-like wrapper. See `references/gohighlevel-html-deployment.md` for Shadow DOM packaging, processed-asset handling, CRM form limitations, and deterministic QA.
- Heavy inline validation one-liners may hit consent prompts on this Windows setup; the curl 200 check + sếp's own eyes is the accepted verification bar here.

## Animation and motion verification

When the user asks for animation, treat every named effect as a separate acceptance criterion. Do not infer success from CSS keyframes, `animationName`, or a static screenshot. Measure time-separated computed styles in a real browser for each promised effect - for example SVG `strokeDashoffset` changing, orbit transform matrices changing, and chip Y translation changing.

Keep content visible without JavaScript. Calculate pointer-parallax pixel values in JavaScript rather than relying on browser-sensitive custom-property multiplication inside `calc()`. Trigger section-specific animations when the section enters the viewport and restart them after tab changes where relevant.

Respect `prefers-reduced-motion` by default. If the user explicitly wants motion enabled and their OS setting silently disables it, expose a visible Motion On/Off control instead of claiming the effects work. See `references/cinematic-motion-runtime-verification.md` for the implementation and Chrome CDP verification recipe.

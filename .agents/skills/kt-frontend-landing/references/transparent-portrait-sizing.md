# Transparent Portrait Replacement and Relative Sizing

Use this note when replacing a temporary portrait block with a supplied PNG/WebP that contains alpha, or when the user asks to resize the portrait relative to its current appearance.

## Diagnose the visible background correctly

A source reported as `RGBA` can still show two different backgrounds:

1. Transparent pixels outside the portrait artwork reveal the CSS background of the wrapper.
2. Opaque or semi-opaque pixels inside the artwork remain part of the image itself.

If a transparent portrait appears inside a gray rectangle, inspect both layers before editing the asset:

- Source: native width/height, image mode/alpha, and visible artwork bounds.
- Wrapper: computed `background`, padding, border radius, fixed/min height, overflow, and pseudo-elements.
- Image: computed width/height, `object-fit`, and `object-position`.

Do not blame the source alpha until the wrapper background is proven transparent.

## Replace a placeholder cleanly

When the placeholder wrapper has no remaining visual purpose, remove all of its presentation rather than changing only one property:

```css
.authority-portrait {
  margin: 0;
  display: grid;
  place-items: center;
  background: transparent;
}

.authority-portrait img {
  display: block;
  width: var(--portrait-width, 65%);
  height: auto;
  object-fit: contain;
  object-position: center;
}
```

Also remove stale placeholder SVG/text, fixed image heights, wrapper `min-height`, padding, radius, overflow clipping, and breakpoint-specific height overrides unless the approved design still needs them. Dead placeholder rules often cause the "transparent image has a gray background" illusion or leave large blank vertical space.

Use meaningful `alt` text, retain public production-safe URLs, and preserve the source aspect ratio with `height: auto`.

## Relative resize requests

Treat "increase the image by about X%" as a multiplication of the current rendered size:

```text
new percentage = current percentage × (1 + requested increase)
```

Example:

```text
current width = 50%
requested increase = 30%
new width = 50% × 1.30 = 65%
```

Do not add 30 percentage points (`50% -> 80%`) unless the user explicitly says "add 30 percentage points" or gives the target width.

Change the image width, not the whole grid column, when the request concerns only the portrait. Otherwise typography and section geometry may shift while the portrait appears only slightly different.

## Verification

After each material portrait change:

1. Render desktop and an exact mobile CSS viewport such as `390 × 844`.
2. Assert `innerWidth`, `clientWidth`, and `scrollWidth`; reject a supposed 390px run that reports about 980px.
3. Inspect pixels for the full head, shoulders, outline/ring, and alpha edges.
4. Confirm no rectangular wrapper background remains when transparency is requested.
5. Confirm `naturalWidth/naturalHeight`, rendered dimensions, `height:auto`, `object-fit`, and `object-position`.
6. Check the vertical gap between portrait, copy, and the following section after removing fixed wrapper height.
7. Capture a fresh screenshot after every edit; do not reuse evidence from the previous size.

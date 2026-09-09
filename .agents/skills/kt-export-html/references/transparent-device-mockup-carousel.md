# Transparent Device Mockups with an Image Carousel

Use when a hero has a laptop/phone/tablet PNG frame and real slide images must appear inside the screen.

## Asset preflight

1. Download remote assets locally rather than hotlinking production UI.
2. Inspect every image for dimensions, format, and alpha channel.
3. Do not assume an RGBA mockup has a transparent display opening. Sample or inspect the screen-center alpha separately from corner alpha.
4. Verify all slide images have a consistent aspect ratio before implementation.

A mockup may be RGBA while its LCD area remains opaque black. In that case, cut only the inner display opening to alpha zero and preserve the bezel/frame:

```python
from PIL import Image, ImageDraw

image = Image.open("mockup-original.png").convert("RGBA")
mask = Image.new("L", image.size, 0)
ImageDraw.Draw(mask).rounded_rectangle((x1, y1, x2, y2), radius=5, fill=255)
alpha = image.getchannel("A")
alpha.paste(0, mask=mask)
image.putalpha(alpha)
image.save("mockup.png", optimize=True)
```

Measure `(x1, y1, x2, y2)` from the actual supplied asset. Verify the screen-center alpha is `0` and that bezel pixels remain nonzero. Do not use `mix-blend-mode`, black-background masking, or feathered CSS masks when a true alpha cutout can be produced.

## Layering recipe

- Device wrapper uses the mockup's native aspect ratio.
- Carousel screen is absolutely positioned using percentages derived from the display opening:
  - `left = x1 / image_width * 100%`
  - `top = y1 / image_height * 100%`
  - `width = (x2 - x1) / image_width * 100%`
  - `height = (y2 - y1) / image_height * 100%`
- Slide layer sits below the frame.
- Transparent mockup frame sits above the slide layer with `pointer-events:none`.
- Put navigation controls above both layers if they need to remain clickable.
- If supplied slides already contain complete designed compositions, use `object-fit: fill` only when their ratio exactly matches the screen opening; otherwise prefer `contain` and an intentional backing color to avoid destructive crop.

## Carousel behavior

Implement without a dependency unless the project already has a carousel library:

- Previous/Next controls.
- One dot per slide and `aria-current` on the active dot.
- Keyboard: Left, Right, Home, End.
- Touch swipe with a modest threshold (about 35 px).
- Optional autoplay around 5 seconds.
- Pause autoplay on pointer hover and keyboard focus.
- Disable autoplay for `prefers-reduced-motion`.
- Maintain an `aria-live="polite"` status such as `Case study 2 trên 10`.
- Expose a tiny test handle during development, for example `window.caseStudyCarousel.activeIndex`, then verify real state changes through CDP.

## Verification

Do not stop at visual inspection.

1. Confirm the expected slide and dot counts in the DOM.
2. Record active index and active image source.
3. Trigger Next and confirm both values change.
4. Jump to the final slide and verify wrapping/index logic.
5. Capture screenshots of at least two different active slides to prove the carousel changed visibly.
6. Render desktop and a true emulated mobile viewport. Confirm `scrollWidth === innerWidth`.
7. Inspect that the slide stays entirely inside the bezel and that no rectangular background remains around the device.
8. After swapping a mockup with a different canvas/aspect ratio, rebalance device width and negative margins; old composition values rarely transfer safely.

## Pitfalls

- `has_alpha: true` only proves the file has an alpha channel, not that the display opening is transparent.
- A square mockup canvas may contain large transparent padding. CSS sizing is based on the full canvas, so apparent laptop size and vertical rhythm can differ sharply from a tightly cropped mockup.
- Using a background image may make old CSS glow/grid layers redundant and visually overbuilt. Remove duplicate atmospheric layers.
- Headless screenshots taken before entry animations settle can falsely show missing copy. Use CDP or sufficient virtual-time budget before judging the render.

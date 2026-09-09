# Embedded media and generated assets

Use this reference when a landing page includes a third-party iframe or assets generated through Antigravity.

## Responsive third-party video embeds

1. Preserve the supplied embed URL exactly, but remove chat-only wrappers such as `@url:` before writing HTML.
2. Use a semantic iframe with a concise `title`, fullscreen support, and an explicit responsive wrapper. If the source supplies `padding-bottom: 62.5%`, preserve that ratio unless the user asks to change it.
3. Keep visual chrome on the outer shell and clipping on the inner ratio wrapper:
   - outer shell: padding, border radius, background, shadow;
   - inner wrapper: `position: relative`, ratio, `overflow: hidden`, inner radius;
   - iframe: absolute inset, full width/height, no border.
4. Verify the embed endpoint returns a successful response and does not redirect to an unexpected URL.
5. Third-party players often initialize after the parent document reaches `complete`. For screenshot QA, wait several seconds after page load; an immediate black frame is not proof that the embed failed.
6. Confirm player UI or thumbnail in a real render at desktop and mobile. Also measure iframe dimensions and compare width/height to the intended ratio.
7. Verify DOM geometry for nearby components. For a countdown intended below the video, assert `countdownTop > videoBottom` and record the gap rather than relying only on a partial screenshot.
8. If the normal preview port is occupied, inspect the served page title before QA. Do not kill an unrelated server. Start the project on a dedicated free port and make the render URL configurable.

## Logos with internal whitespace

Raster logo files can contain large transparent or white margins. The CSS image box and visible artwork bounds are not the same.

- Inspect native dimensions and visible-pixel bounds before sizing.
- Judge top spacing and component spacing from the visible logo artwork, while also preserving a real layout margin between the image box and the next component.
- When asked to reduce a logo to 80%, multiply each breakpoint's existing width by 0.8; do not choose a visually approximate replacement.
- Re-render both desktop and mobile after vertical offset changes because centering rules can make a margin change move the visible artwork by less than the raw CSS delta.

## Antigravity-generated landing-page assets

Antigravity credentials may live in a credential pool and may not appear in a child shell's `os.environ`.

- Do not conclude an image API key is absent from an environment-variable probe alone.
- Check Antigravity auth status and whether the `image_gen` toolset/backend is enabled.
- Generate through the Antigravity `image_generate` runtime so it can load pooled credentials without exposing secrets to shell output.
- Save accepted images into the project asset directory; do not leave production HTML dependent on Antigravity cache paths.
- Verify each copied asset's real dimensions and browser `naturalWidth`/`naturalHeight`.
- Run visual QA at the actual card ratio. Prefer `object-fit: contain` when preserving the complete generated composition matters more than edge-to-edge fill.

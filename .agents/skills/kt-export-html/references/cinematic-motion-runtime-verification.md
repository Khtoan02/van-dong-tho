# Cinematic Motion - Runtime Verification

Use this when adding visible animation to a landing page. Static screenshots and the presence of `@keyframes` are insufficient evidence.

## Implementation principles

- Keep content visible without animation or JavaScript; motion is progressive enhancement.
- Use transform/opacity for continuous motion and `requestAnimationFrame` for scroll-linked updates.
- For pointer parallax, calculate complete pixel values in JavaScript and assign CSS variables such as `--scene-x: -4px`. Avoid fragile CSS arithmetic such as `calc(var(--x) * -.4)` because support differs across browser versions.
- Trigger one-shot animations when the relevant section enters the viewport. For SVG line drawing, add a section state class through `IntersectionObserver`, then animate `stroke-dashoffset`.
- Restart panel-specific animation when an interactive tab changes by removing and re-adding the section state class across animation frames.
- Continuous decorative motion should be visible enough to verify: orbit transforms must change over time; floating chips must show a measurable Y translation.

## User intent versus reduced motion

Normally respect `prefers-reduced-motion`. If the user explicitly requests that motion remain enabled in their environment and the OS preference is suppressing it, provide an explicit in-page Motion On/Off control. Do not leave animation silently disabled. Motion state should be visible to the user, and Motion Off must deterministically stop animations.

## Tight runtime checks

Verify the exact effects the user asked for in a real browser over time:

1. **Chart draw** - after scrolling Platform into view, sample the line path's computed `strokeDashoffset`, wait, sample again; values must differ and finish near zero.
2. **Orbit rotation** - sample an orbit element's computed `transform`, wait roughly one second, sample again; matrices must differ.
3. **Floating chips** - sample a chip's computed `transform`, wait roughly one second, sample again; Y translation must differ.
4. **Motion control** - with OS reduced motion emulated, confirm the requested default state is actually active; activate Motion Off and confirm computed `animationName` becomes `none`.
5. **Visual regression** - render desktop and full mobile pages to ensure transforms do not introduce clipping or blank sections.

Chrome DevTools Protocol is a reliable fallback when a Playwright test runner is not installed: start headless Chrome with `--remote-debugging-port`, connect to the page WebSocket, use `Runtime.evaluate`, `Emulation.setEmulatedMedia`, `Input.dispatchMouseEvent`, and timed samples of computed styles.

## Failure patterns

- `animationName` alone proves only that CSS selected a keyframe, not that pixels visibly change.
- A full-page screenshot may capture only one instant and cannot prove motion.
- Entrance animations that run on initial page load may finish before the user scrolls to the section.
- Global `@media (prefers-reduced-motion: reduce) { * { animation:none!important } }` can explain why all requested effects vanish. Inspect the live media state before changing animation code.
- Do not report animation complete until each specifically promised effect has a time-separated runtime assertion.
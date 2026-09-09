# Hero ornament + marquee overlap without responsive collisions

Use when a hero has a large animated ornament (rings, glow, waves) that should visually pass over a moving logo rail near the bottom.

## Stable composition

- Keep the hero content and ornament above the marquee with explicit stacking (`hero z-index > marquee z-index`).
- Keep the marquee in normal document flow near the hero bottom. Do not pull it upward with a large fixed negative margin merely to create overlap.
- Let the ornament expand into the marquee's area using visible overflow and animation scale. This preserves the semantic vertical order: CTA -> proof/checklist -> logo rail -> next section.
- If an expanding wave starts invisible, use staggered negative animation delays so at least one wave is already mid-cycle on initial paint. Verify that the wave, not the logo rail, creates the overlap.
- Remove hard dividers only when the design calls for a continuous canvas; do not use border removal as a substitute for correct spacing.

## Required viewport QA

A tall desktop screenshot can hide collisions that occur on a wide, short laptop/desktop viewport. Before reporting success:

1. Inspect the user's screenshot dimensions when feedback includes an image.
2. Render that exact width and height.
3. Also render one contrasting desktop aspect ratio, such as `1440x1000` after a `1875x945` report.
4. Check pixel order and spacing: CTA bottom < checklist top/bottom < marquee top. The marquee must not pass between CTA and checklist.
5. Capture after enough virtual/runtime time for the animated wave to be visible.
6. Confirm the ornament crosses the rail on the intended side while the rail stays behind it.
7. Reopen/refresh the Preview Pane only after both renders pass.

## Failure pattern

A fixed negative margin tuned at one viewport (for example `margin-top:-150px`) can appear correct at `1440x1000` but move the logo rail into the CTA/checklist at a wider, shorter viewport. Prefer a small overlap offset and make the animation reach the rail instead.
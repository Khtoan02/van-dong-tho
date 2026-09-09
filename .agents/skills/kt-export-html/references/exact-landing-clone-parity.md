# Exact landing-page source-mirror verification

Use this only after the user explicitly chooses a source mirror as the control page. For an editable, platform-independent A/B control, use an independent rebuild instead and apply the visual-comparison parts of this workflow without retaining the builder runtime.

## Validated workflow

1. Confirm and record the architecture as `source mirror`; do not call it a rebuild.
2. Fetch the deployed HTML exactly as served, preserving bytes after HTTP decompression.
3. Save the mirror as `index.html` without reformatting, minifying, normalizing, or editing markup. Retain remote CDN assets and runtime scripts only because this architecture was explicitly chosen.
4. Verify source and mirror byte length, SHA-256, and byte equality before visual QA.
4. Render the reference URL and local clone through the same Chrome/CDP process, viewport, device metrics, load delay, and screenshot method.
5. Assert document title, viewport width, scroll width, scroll height, section/form counts, duplicate IDs, and horizontal overflow.
6. Compare screenshots deterministically with Pillow `ImageChops.difference`:
   - image dimensions must match;
   - `diff.getbbox()` should be `None` for exact parity;
   - RGB mean absolute error should be zero.
7. Keep reference, clone, and diff images as evidence. Build neutral A/B comparison boards for a craft critic so labels do not reveal which side is the reference.
8. Do not submit a live production form during QA. Inspect its fields and runtime DOM, then state that submission was intentionally not tested.

## Dynamic overlays and lazy state

Hosted builders can inject origin-dependent or transient branding into localhost renders. A screenshot taken too early can show a temporary badge that is absent on the production domain even when the HTML is byte-identical.

- First prove byte equality.
- Capture at a stable post-load state. A validated case required 15 seconds instead of 5 seconds before the temporary builder badge disappeared.
- Re-capture both breakpoints and recompute the pixel diff. Do not hide a badge with CSS until timing and origin behavior have been ruled out.
- For lazy media, compare both the initial full-page state and scrolled section-level captures when media visibility matters.

## Design-loop critic evidence

- Exact-clone briefs must explicitly say that original spacing, empty regions, and known visual flaws are intentional control behavior. A Brief critic must not redesign the source under the guise of usability.
- If a System critic cannot resolve a small visual detail from a downscaled full-page board, add an enlarged detail crop while retaining the full-page render.
- Clarify ambiguous nouns in the critic brief. For example, “typewriter illustration” means a static image of a typewriter, not a typewriter text animation.
- If the same evidence gap survives a round, escalate the critic model tier and provide better evidence rather than changing a pixel-identical artifact.

## Deployment caveats

A byte-identical local control may still depend on the original CDN, analytics, form endpoint, domain checks, and Internet access. Report these dependencies and ask for the final A/B deployment platform/domain before changing tracking or submission behavior.

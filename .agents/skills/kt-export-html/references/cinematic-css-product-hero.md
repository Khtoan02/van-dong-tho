# Cinematic editorial hero with a CSS product tableau

Use when a landing-page hero needs a premium photographic mood but final product imagery is unavailable. This is a validated fallback for books and other rigid rectangular products - not a substitute for supplied brand assets.

## Composition recipe

1. Use one licensed/local photographic background for environmental realism.
2. Darken the copy side with a directional overlay, then add a restrained radial warm light behind the product side.
3. Build only the foreground product tableau in CSS:
   - absolutely positioned covers with fixed aspect ratios;
   - subtle `rotateY()` / `rotate()` and `perspective` for front, spine, and rear volumes;
   - ivory-to-beige surface gradients, thin inset borders, neutral deep shadows;
   - one simple environmental silhouette such as a mirror frame or vase.
4. Keep foreground elements decorative with `aria-hidden="true"`; expose one concise accessible label on their wrapper.
5. Use supplied copy exactly. Do not add dates, founding claims, collection labels, provenance, edition status, or other credibility language merely to make the layout look authentic.
6. If CTA destination is unknown, use a clearly disclosed in-page target and flag it for replacement.

## Responsive strategy

Desktop can use a 45/55 copy-to-product split. On mobile, switch to a vertical flow and treat the visual as a bounded second block rather than preserving desktop scale.

Useful mobile controls:

- reduce the visual block height before shrinking the headline;
- pull all product positions inward (`left`/`right`) instead of allowing negative overflow;
- reduce object height to roughly 70-78% of the visual block;
- scale secondary decor from `transform-origin: bottom right`;
- render a real 390x844 screenshot and check that headline, body, CTA, and enough of each product are visible.

A product may continue below the first viewport when the hero is taller than one screen, but the visual must read as intentional - not as a giant cropped rectangle.

## Verification loop

1. Serve over `python -m http.server`.
2. Verify HTML and every local asset return HTTP 200.
3. Render desktop and mobile screenshots with headless Chrome.
4. Inspect visually for copy clipping, CTA visibility, weak contrast, product collisions, and excessive cropping.
5. Remove any decorative microcopy that implies unsupported facts.
6. Re-render after the fix; HTTP checks alone are not visual QA.

## Anti-slop note

For an editorial sales hero, a large left headline plus right product tableau is appropriate to the Decide/Learn surface. Avoid adding kicker copy solely as decoration, icon grids, glass panels, fake metrics, or multiple competing CTAs. A small nonverbal rule/diamond ornament can provide rhythm without inventing claims.

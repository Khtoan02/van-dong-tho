# Responsive hero overlap and simple founder-section QA

Use when a hero combines an animated radial visual, a moving logo rail, and a following content section, or when a founder letter is modeled on a simple portrait-plus-text reference.

## Animated hero + logo rail

Do not position the logo rail with a large fixed negative margin based on one screenshot. A value that works at `1440x1000` can place the rail through CTA/checklist content at a wider, shorter viewport such as `1875x945`.

Preferred composition:

1. Keep the logo rail after the hero in normal document flow with only a small overlap.
2. Put the hero/radial visual above the rail with `z-index`; keep the rail behind it.
3. Use negative animation delays for staggered waves so at least one expanded ring is visible immediately without moving the rail into the content.
4. Give the logo rail enough top/bottom padding that:
   - it sits below CTA/checklist content;
   - it is near the lower reach of the largest ring;
   - the following section begins only after the ring's maximum visible boundary.
5. Remove hard divider borders when they visually clip the wave transition.

## Required viewport matrix

Render the exact viewport shown in user feedback, not a convenient substitute. For wide desktop heroes, test at least:

- a conventional desktop viewport such as `1440x1000`;
- a wide, short viewport matching the user's screenshot when applicable, e.g. `1875x945`;
- the established exact mobile CDP viewport.

Inspect CTA, checklist, marquee, maximum ring boundary, and start of the next section in the same screenshot. A pass at one aspect ratio is not proof at another.

For motion overlap, capture at more than one animation phase, including a late expansion phase. Static CSS or an early-frame screenshot cannot prove the maximum wave does not cross into the next section.

## Simple founder-letter references

When the reference is a plain portrait-left / letter-right composition, do not turn the copy into manifesto cards, numbered pain lists, badges, quote panels, decorative timelines, or extra CTAs.

Use:

- left: real founder portrait, approximately 4:5 to 3:4, modest radius, optional name/role caption;
- right: date, one clear heading, paragraphs, restrained bold emphasis, optional sign-off;
- desktop: approximately 35/65 columns with aligned tops;
- mobile: portrait, caption, date, heading, then letter text.

If the real founder portrait is not available, never substitute another person's photo. Use a clearly labeled placeholder and flag the missing asset.

## Hero-derived grid width

The approved hero establishes the page's full content grid. Later full-width sections should not become visibly narrower just because a generic shell has a hard-coded `max-width`.

Validated pattern:

```css
:root { --pad-x: clamp(24px, 5vw, 80px); }
.hero,
.page-section { padding-inline: var(--pad-x); }
.section-shell,
.footer-main,
.footer-bottom { width: 100%; margin-inline: auto; }
.founder-letter .section-shell { width: 70%; }
@media (max-width: 900px) {
  .founder-letter .section-shell { width: 100%; }
}
```

At a `1875px` viewport with `80px` side padding, the hero inner grid is `1715px`. A 70% founder-story shell is approximately `1201px`, while beliefs, services, ebook/offer, and footer remain `1715px` and share `x=80` / `right=1795`.

Do not compare the hero element's outer bounding box when it includes padding. Compare the hero's inner content edges or derive them from the shared padding token.

## One CTA language per landing page

Do not create a novel button geometry for each section. Once the hero CTA is approved, later CTA buttons should reuse:

- pill or corner geometry;
- type size/weight;
- horizontal and vertical padding;
- arrow-chip shape;
- hover lift/shadow behavior.

Color inversion is allowed for contrast. For example, on a gold service card use the hero pill in black/white; on a dark card use the same pill in gold/black. The geometry and interaction remain identical.

A runtime check can assert the shared system:

```js
[...document.querySelectorAll('.service-btn')].map(el => ({
  display: getComputedStyle(el).display,
  radius: getComputedStyle(el).borderRadius,
  width: el.offsetWidth,
  height: el.offsetHeight,
  arrowRadius: getComputedStyle(el.querySelector('.service-arrow')).borderRadius
}));
```

Follow the runtime check with a screenshot of the actual section. Computed `border-radius:999px` does not by itself prove the button is visually aligned or unclipped.

## Deep-section screenshot verification

A shell command containing an unquoted URL with `#section-id` can treat the hash as a comment and silently capture the wrong part of the page. Quote the full URL. If Chrome still captures before hash scrolling settles, use CDP:

1. navigate to the page;
2. wait for load/layout;
3. call `document.querySelector(selector).scrollIntoView({block:'start',behavior:'instant'})`;
4. wait for paint;
5. assert the section's `getBoundingClientRect().top` is approximately zero;
6. capture the viewport.

Reject screenshots that show the previous section even if the command exited successfully.
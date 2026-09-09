# Exact copy and content-QA synchronization

Use this reference when a user supplies exact landing-page headings, labels, capitalization, punctuation, or ordered copy changes.

## Rules

1. Preserve the supplied wording, capitalization, punctuation, labels, and item order exactly. Do not normalize copy merely because a visual critic suggests smoother prose.
2. Check rendered text, not only source HTML. A global `text-transform` can silently change correct source copy; use a section-scoped override when only one section needs sentence case.
3. When labels lose suffixes or item counts change, assert both the new exact strings and the absence of prohibited old strings.
4. Update content sentinels, expected counts, and QA fixtures in the same edit as the copy. If a stale assertion fails after a correct UI change, update the assertion source and rerun the full check.
5. Verify casing, wrapping, suffix removal, and overflow in real desktop and mobile renders.

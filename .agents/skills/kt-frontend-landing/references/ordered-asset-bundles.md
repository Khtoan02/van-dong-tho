# Ordered user-supplied asset bundles

Use this reference when numbered final assets replace placeholders or generated mockups in a landing page.

## Workflow

1. Treat the exact folder named by the user as the source of truth. Duplicate folders may contain identical files in a different order; compare dimensions and hashes rather than assuming they are interchangeable.
2. For numbered files, build a temporary labeled contact sheet and verify each image's meaning against the intended card order before editing HTML.
3. Map explicit ordered paths (`1`, `2`, `3`, ...) and assert both the expected item count and every exact source path in QA.
4. Remove all old placeholder/generated references from rendered HTML. Keeping unused source files on disk is acceptable, but the production section must not mix asset generations accidentally.
5. Use native dimensions in `width`/`height`, verify browser `naturalWidth`/`naturalHeight`, and preserve the supplied ratio with `object-fit: contain` unless crop is explicitly approved.
6. Render the complete section at desktop and actual mobile width. Check semantic order, legibility of important text baked into images, crop/stretch, letterboxing, and overflow.
7. Delete temporary contact sheets and other QA-only artifacts before delivery.

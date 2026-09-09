# Responsive heading line control

Use this when the user wants one phrase kept together on mobile without changing the approved desktop heading.

## Phrase-level wrapping

Do not reduce the whole heading or insert global `<br>` tags when only one phrase must stay together.

1. Wrap the semantic phrase in a dedicated nested span.
2. Keep that nested span inline at desktop so the approved desktop line remains unchanged.
3. At the mobile breakpoint, apply `display: inline-block` and `white-space: nowrap` only to the phrase.
4. Let the browser move the whole phrase to the next line when it cannot fit after the preceding words.

```html
<h1>
  <span>XÂY DỰNG <span class="keep-together">SALE FUNNEL</span></span>
  <span>VÀ AUTOMATION CÙNG <em>AI AGENT</em></span>
</h1>
```

```css
h1 .keep-together {
  display: inline;
  white-space: inherit;
}

@media (max-width: 680px) {
  h1 span { white-space: normal; }
  h1 .keep-together {
    display: inline-block;
    white-space: nowrap;
  }
}
```

## Verification

- Render the actual mobile CSS viewport, not just a resized screenshot.
- Record the exact visible line breaks.
- Assert `scrollWidth === innerWidth`.
- Re-render desktop and verify its approved line breaks and spacing are unchanged.
- If a whole line still cannot fit, size that line individually rather than shrinking or scaling the entire heading.

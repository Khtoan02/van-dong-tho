# Impeccable - detector reference (tested 2026-08-04)

Source: https://github.com/pbakaus/impeccable (Paul Bakaus). npm package `impeccable` v3.5.0, skill v4.0.4, Apache 2.0. ~3.3MB installed.

## What it is

Design guidance + QA for AI coding agents: 24 commands, 59 deterministic detector rules. The detector runs standalone with no LLM and no API key - the valuable part for Antigravity, since the `/command` skill system targets Cursor/Claude Code/Codex/Grok harnesses.

## Install modes

```bash
# Non-interactive project install (REQUIRED flags - bare `install` is interactive and hangs in non-TTY)
npx -y impeccable install --scope=project --providers=cursor

# Other providers: claude,codex,grok ; scope: project|global
npx -y impeccable update        # refresh existing install
npx -y impeccable --version
npx -y impeccable help          # list all 24 commands
```

Installs into `.cursor/skills/impeccable/` (SKILL.md + reference/*.md playbooks + scripts/*.mjs) plus `.cursor/agents/` (4 sub-agents) and `.cursor/hooks.json` (preToolUse detector hook). Harmless in a non-Cursor project - just files.

## Detector usage (the part we actually use)

```bash
npx -y impeccable detect <file-or-dir-or-url>...
npx -y impeccable detect index.html --json          # machine-readable, exit 2 when findings
npx -y impeccable detect . --viewport 390x844       # mobile-width pass (URL scans use Puppeteer)
npx -y impeccable detect . --scope type,layout      # limit rule domains
npx -y impeccable detect . --no-advisory            # hide advisory-only findings
```

- HTML files: static analysis including linked CSS. Non-HTML: regex matching. URLs: full browser render.
- Project config: `.impeccable/config.json` / `config.local.json` (detector.ignoreRules, ignoreFiles, ignoreValues).
- Inline ignores travel with the file: `<!-- impeccable-disable overused-font -- reason -->`, `/* impeccable-disable-line rule-id */`, `// impeccable-disable-next-line rule-id`.

## Verified detection example

A test file with Inter font, purple gradient (#667eea→#764ba2) and #888-on-#f5f5f5 text produced exactly:

- `low-contrast` - 3.3:1 vs required 4.5:1 (WCAG AA)
- `overused-font` - Inter/Roboto/Fraunces/Geist/Plus Jakarta Sans/Space Grotesk are on its overused list
- `ai-color-palette` - purple/violet gradients and cyan-on-dark are flagged as AI tells

## Relevance / conflicts for sếp

- **Conflict:** Roboto (sếp's standing default font) is on the overused-font list. Per Impeccable's own rule "the brief wins" - ignore font findings when a brief or sếp's preference dictates the face. Keep honoring contrast/layout/a11y findings.
- **Aligned:** its anti-pattern guidance (no nested cards, no bounce easing, no gray-on-color, no pure black/gray, asymmetric layouts over centered stacks) matches the creative-layout standards sếp already demands.
- 24 commands include: init, shape, craft, document, extract, critique, audit, polish, bolder, quieter, distill, harden, onboard, animate, colorize, typeset, layout, delight, overdrive, clarify, adapt, optimize, live (browser variant iteration). These need an AI harness; in Antigravity use `detect` + read the playbooks under `.cursor/skills/impeccable/reference/` manually if wanted.

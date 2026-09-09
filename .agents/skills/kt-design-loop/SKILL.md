---
name: kt-design-loop
description: Run a three-critic loop until a design clears the bar.
version: 0.2.0
author: Agency Team, Antigravity Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  antigravity:
    tags: [design, critique, quality, iteration, frontend]
    related_skills: [claude-design, kt-frontend-landing]
---

# Design Loop

Take a goal and a real-world reference, extract the mechanisms that make the reference effective, then iterate with a builder and three independent critics until every critic passes. Use rendered output as evidence; do not let implementation intent substitute for visible quality.

Technique credit: the gauntlet loop is inspired by Matt Shumer's Claude of Duty: https://github.com/mshumer/Claude-of-Duty

## When to Use

Trigger on `/kt-design-loop`, `design loop`, `run the critic loop`, `loop this against`, or when the user asks to hold a design against a reference until it wins.

Use for landing pages, websites, visual documents, decks, animations, ads, or other artifacts that can be rendered and compared.

Do not use when there is no renderable output, the user wants only a quick informal review, or the task has no meaningful quality bar.

## Fixed Critic Roles

The skill owns these roles. The user never writes critic prompts.

- **Brief critic** - Does the result accomplish the stated goal? Ignore beauty and implementation.
- **System critic** - Does it obey `design-system.md` or the supplied brand/design rules? Check type scale, spacing, colors, components, and tokens objectively.
- **Craft critic** - Does the rendered result beat the reference against `bar.md`? Judge only side-by-side renders, never code.

Write a specific brief for each critic per run. Keep the roles fixed so they cannot collapse into one opinion.

## Procedure

Complete four phases in order. Do not build during phases 1 to 3.

### Phase 1: Interview

Ask exactly these three questions together, then stop and wait:

1. What are you building, and how long or how big?
2. Name something that already does this brilliantly - a specific URL, video, document, or file that can be opened. If nothing comes to mind, say `skip`.
3. What files should be used - design system, brand guide, script, copy, assets, or existing draft?

If the reference is vague, push once for a specific page or file. A vague bar lets the craft critic invent the comparison.

If the user says `skip`, propose three specific candidate bars with one line explaining each, then wait for a choice. If the user does not choose after being prompted, use the hardest candidate and state that choice.

Completion criterion: the goal, scope, source files, and one fetchable reference are explicit.

### Phase 2: Preflight

This is a check, not a question. Run it before making anything.

1. Fetch and inspect the bar using the browser or `read_file`; capture screenshots or renders where appropriate.
2. Confirm the planned output can be rendered: browser screenshots for sites, frame filmstrip for animation, or page renders for documents.
3. Name required generation tools - image, video, audio, or voice - and verify that they are connected before depending on them.
4. Verify every named input file exists and can be read.
5. Report one block containing:
   - Working
   - Missing or degraded
   - Which critic becomes blind for each missing input

Never continue quietly when a critic cannot see its evidence. If the reference is blocked or absent, ask for another. If the output cannot be rendered, stop because the craft critic cannot operate.

Completion criterion: both the reference and intended output have a verified render path, and every degradation is disclosed.

### Phase 3: Teardown

Inspect the reference thoroughly and write 5 to 7 checkable visual mechanisms to `bar.md` in the active project or deliverable directory.

Use mechanisms, not adjectives. Examples:

- Headline is approximately five times body size, with no more than three type sizes.
- One accent color appears at most twice per viewport.
- Motion resolves in one consistent direction.
- No animation completes in under 400 ms.
- Empty space occupies at least 40 percent of the first viewport.

Every line must be checkable from a render. Show the complete `bar.md` to the user before starting the loop.

Completion criterion: `bar.md` exists, contains 5 to 7 observable mechanisms, and has been shown to the user.

### Phase 4: Loop

Split the goal into the smallest independently improvable pieces. Choose three or four pieces unless the user requests otherwise.

Maintain a live progress file such as `kt-design-loop-progress.md` with:

- Piece and status
- Round count
- Brief critic verdict
- System critic verdict
- Craft critic verdict
- Single biggest gap returned each round
- Gap history

For each piece:

1. **Builder pass** - Build or revise the piece, then render it. The builder may inspect code and source files.
2. **Fresh-context critics** - Run three independent critics in parallel. Use isolated `hermes chat` workers with explicit GPT/Codex model routing when critic tiers differ; use `delegate_task` only when all critics should inherit the parent `gpt-5.6-sol`. Give each only its permitted evidence and a task-specific brief:
   - Brief critic: stated goal plus rendered output; no code and no reference-quality criteria.
   - System critic: design-system or brand rules plus rendered output; no code and no craft bar.
   - Craft critic: `bar.md`, reference render, and output render with neutral labels; no code, build history, or stated intent.
3. Require each critic to return:
   - `PASS` or `FAIL`
   - One-sentence reason
   - If `FAIL`, the single biggest gap only
4. All three must pass. If any fails, choose the largest blocking gap, return only that gap to the builder, revise, rerender, and dispatch three new fresh-context critics.
5. Exit only when all three pass or the user stops the run.

Critics must be harsh. Do not use numeric scores, praise, or cumulative context. Never let a critic read implementation code.

### GPT/Codex Model Routing

Use the `openai-codex` provider for every builder and critic. Route by task weight instead of running all work on the strongest model.

#### Heavy tasks - `gpt-5.6-sol`

Always use `gpt-5.6-sol` for:

- Reference teardown when the visual system is complex or ambiguous.
- Initial architecture and builder passes for substantial pieces.
- Major redesigns after a failed craft round.
- Craft critic comparison against the reference.
- Final integrated review across all pieces.
- Any task requiring strong visual judgment, synthesis, or difficult trade-offs.

#### Medium tasks - choose `gpt-5.5` or `gpt-5.4`

Use a medium GPT model for:

- Brief critic when the goal has multiple constraints.
- Copy hierarchy and conversion-flow checks.
- Targeted revisions whose gap is already explicit.
- Consolidating critic verdicts and selecting the single blocking gap.

Prefer `gpt-5.5`; use `gpt-5.4` when the task is narrower and clearly specified.

#### Light tasks - choose `gpt-5.4-mini`

Use `gpt-5.4-mini` for:

- System critic checks against explicit tokens and rules.
- File/status bookkeeping and progress-page updates.
- Simple existence, consistency, checklist, and formatting checks.
- Mechanical extraction or normalization that requires little judgment.

Escalate automatically to the next tier when a task is ambiguous, a critic cannot reach a defensible binary verdict, or the same gap survives a revision. Never downgrade the Craft critic below `gpt-5.6-sol`.

#### Execution in Antigravity

`delegate_task` children inherit the parent model and do not expose a per-task model parameter. Therefore:

- Use `delegate_task` directly only when all three fresh-context critics should run on `gpt-5.6-sol`.
- To save cost on light or medium work, launch isolated one-shot Antigravity workers with `terminal`, explicitly setting both provider and model:

  `hermes chat -Q --source tool --provider openai-codex -m <model> -q "<self-contained critic brief>"`

- Run independent critic processes in parallel when possible. Each prompt must be self-contained and include only the evidence that critic is allowed to inspect.
- For image-based critics, attach the rendered image with `--image <path>`. When comparing two images, provide a neutral side-by-side comparison image as the single attachment.
- Use `gpt-5.6-sol` in the parent Coder session for the builder unless the current edit is plainly mechanical.
- Record the actual provider and model used for every builder/critic run in `kt-design-loop-progress.md`.
- Verify command completion and capture the real verdict. Never report a routed model unless the worker was actually launched with that explicit model.

If a selected model is unavailable from `openai-codex`, retry once with the next stronger available GPT model. The final fallback is `gpt-5.6-sol`.

### User Checkpoints and Cost

Do not claim token cost because self-reported token counts are unreliable. Report rounds completed, pieces elapsed, and wall-clock progress only when measured.

If the user gives a round, time, or budget ceiling, treat it as a checkpoint: pause before crossing it and ask whether to continue. Without a ceiling, the user stopping the loop is the brake.

## Pitfalls

- **Vague reference** - obtain a specific page, frame, or file before teardown.
- **Fresh-context critics** - every critic must run in a separate `delegate_task` child or isolated `hermes chat` process.
- **Blind craft critic** - no render means no valid craft judgment.
- **Soft verdicts** - use binary pass/fail, never scores.
- **Code-aware criticism** - code reveals intent and biases judgment; critics inspect renders only.
- **Fixed rounds** - winning is the exit condition, not an arbitrary iteration count.
- **Over-specification** - retain only constraints that change observable quality.
- **Unverified routing** - record the actual provider/model command; do not claim a cheaper worker ran unless it did.

## Verification

Before reporting completion, verify:

- [ ] The reference was fetched and rendered.
- [ ] The output was rendered in its real medium.
- [ ] `bar.md` contains 5 to 7 checkable mechanisms.
- [ ] The progress file records every round, gap, provider, and model.
- [ ] Every round used three independent critic contexts.
- [ ] All routed workers used `openai-codex`.
- [ ] Craft critic and heavy builder/review tasks used `gpt-5.6-sol`.
- [ ] Light tasks used a cheaper GPT model when appropriate, or the reason for escalation was recorded.
- [ ] Critics saw rendered evidence and never code.
- [ ] The final round records `PASS` from Brief, System, and Craft.
- [ ] Any missing tools, source files, or model availability limits were disclosed.

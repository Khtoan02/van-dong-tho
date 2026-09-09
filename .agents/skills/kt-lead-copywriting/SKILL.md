---
name: kt-lead-copywriting
description: Write three complete lead-funnel landing pages.
version: 0.2.0
author: Tôm, Antigravity Agent
license: MIT
platforms: [macos, windows, linux]
metadata:
  antigravity:
    tags: [agency, copywriting, lead-funnel, opt-in, lead-magnet]
    related_skills: [but-chi]
---

# Lead Funnel Copywriting Skill

Use this skill when Bút Chì must write production-ready copy for a lead-generation funnel. Every creation run produces three complete landing-page versions, one for each approved structure, plus form microcopy, thank-you copy, and the immediate lead-magnet delivery email.

This skill writes copy. It does not build pages, configure forms, connect CRM fields, create visual assets, invent legal consent language, or write a nurture sequence while that component is temporarily disabled.

## When to Use

Use for:

- Lead magnet funnels for ebooks, checklists, templates, reports, mini-courses, or resource packs.
- Opt-in or squeeze pages.
- Thank-you and next-step pages after lead submission.
- The immediate lead-magnet delivery email.
- Review and improvement of an existing lead funnel.

Do not use for:

- Webinar registration and event follow-up - use `kt-webinar-copywriting`.
- A direct sales page whose main CTA is payment or purchase - use `kt-sales-copywriting`.
- Nurture sequences - temporarily disabled in this skill.
- Banner concepts or visual prompts - route to Bút Màu.
- CRM implementation or form integration.

## Prerequisites

Read the client/project source of truth and assigned brief before writing. Load `but-chi` for shared copywriting, brand-voice, anti-AI-slop, and claim-safety rules.

Read:

- `assets/brief-template.md` when critical input is missing.
- `references/lead-funnel-structures.md` before drafting.
- `templates/output-template.md` before preparing the deliverable.

## Required Inputs

### Critical

1. Client/project.
2. Target audience.
3. Lead magnet or value exchange.
4. Immediate problem it helps solve.
5. Traffic source or channel.
6. Approved CTA.
7. Brand voice or approved writing samples.

### Strongly preferred

8. Proof, credentials, examples, or authority signals.
9. Lead magnet format and delivery method.
10. Required form fields.
11. Privacy/consent requirements supplied by the client.
12. Desired next step after opt-in.
13. Output path.

If more than 3 critical inputs are missing, ask once using `assets/brief-template.md`. If safe drafting is possible, continue and mark every gap as `[CẦN BỔ SUNG: ...]`. If no approved brand voice or writing sample exists, state that the tone cannot yet be verified instead of claiming a match.

## Fixed Output Contract

Every new Lead Funnel copy run must include:

1. **Phiên bản 1 - Landing page tối giản:** headline + subheadline + form.
2. **Phiên bản 2 - Landing page ngắn có lợi ích:** headline + subheadline + 3-5 benefit bullets + registration prompt + form + copy/handoff note for the lead-magnet image.
3. **Phiên bản 3 - Landing page nhiều section:** hero + form + storytelling or benefit section + company/expert profile.
4. Form labels, CTA, reassurance, validation/success microcopy needed by each version.
5. Thank-you page copy.
6. Immediate delivery email containing the promised asset link or an explicit placeholder.

All three landing pages must be complete customer-facing drafts. Do not provide three headlines and one shared body. Do not silently omit a structure because another structure appears stronger.

The nurture sequence is temporarily disabled and must not appear in the deliverable, brief, or copy inventory.

## Procedure

### Step 1 - Diagnose the value exchange

Summarize:

- Audience and current problem.
- Desired quick win.
- Lead magnet and format.
- Why it is relevant now.
- Approved proof.
- Immediate CTA.
- Delivery method.
- Optional next approved step.
- Missing facts.

Completion criterion: the reader can understand what they provide, what they receive, and what happens immediately after registration.

### Step 2 - Plan all three fixed structures

Use `references/lead-funnel-structures.md`. Map the same approved value exchange into Structures 1, 2, and 3. Give each version a distinct conversion job while preserving the same facts and offer.

Completion criterion: all three structures are mapped, complete, non-duplicative, and factually consistent.

### Step 3 - Write three complete landing pages

For each version:

- Write final customer-facing copy for every required section.
- Include the form heading, approved fields, CTA button, reassurance, and success state.
- Use proof only when supplied.
- Use `[CẦN PHÁP LÝ/CLIENT DUYỆT: consent copy]` when approved consent language is absent.
- Use an implementation note for visual placement, but do not generate the image or visual prompt.

Do not write instructions such as `add a benefit here`. Write the actual words or an explicit missing-data placeholder.

Completion criterion: each version can be handed independently to Coder/page builder without borrowing body copy from another version.

### Step 4 - Write thank-you page copy

Use one or both approved types from the brief:

- **Type 1 - Simple confirmation:** registration success + instruction to check email for the resource.
- **Type 2 - Confirmation with next action:** Type 1 plus an approved second product CTA or Zalo group invitation.

Do not invent a product, group, link, access rule, or delivery timing. Use explicit placeholders when assets are pending.

Completion criterion: the new lead knows the registration status and exact next action.

### Step 5 - Write the immediate delivery email

Include:

- Subject line.
- Preview text.
- Thank-you/registration confirmation.
- Lead magnet name and value reminder.
- Access/download link or `[CẦN BỔ SUNG: link nhận quà]`.
- One CTA to access the promised resource.

Do not add follow-up nurture emails.

Completion criterion: the email delivers exactly the promised asset and uses one clear CTA.

### Step 6 - Review existing funnel copy

When asked to review:

1. Map current copy against all three approved structures.
2. Identify missing, duplicated, weak, or AI-sounding sections.
3. Prioritize the three highest-impact issues.
4. Rewrite the affected sections concretely.
5. Preserve approved facts and voice.

Completion criterion: the review identifies whether three complete structure-based versions exist and supplies concrete corrections.

### Step 7 - Final QA and handoff

Follow `templates/output-template.md`. Save the final Markdown file in the requested client/project folder. Include a copy inventory for Coder/CRM implementation and a `Chờ sếp duyệt phiên bản` status.

Completion criterion: all three full versions, thank-you copy, delivery email, and implementation destinations are accounted for.

## Anti-AI-Slop Gate

Before delivery:

- Compare the copy with approved brand/expert samples.
- Remove empty hype, generic superlatives, repetitive sentence patterns, mechanical transitions, bloated lists, and claims without evidence.
- Prefer concrete audience language, a clear value exchange, and natural Vietnamese phrasing.
- Do not report that the voice matches when no reference was supplied.

## Pitfalls

1. **Three headlines instead of three pages:** every version must be a complete structure-based landing page.
2. **Structure drift:** Versions 1, 2, and 3 must follow the fixed structures, not three arbitrary angles in one structure.
3. **Weak value exchange:** make the quick win specific without exaggeration.
4. **Invented consent:** use an approval placeholder.
5. **Thank-you dead end:** always state the immediate next step.
6. **Hidden nurture content:** do not include nurture or follow-up sequences while disabled.
7. **Premature selling:** add a second offer only when approved for Thank-you Type 2.

## Verification

- Exactly three complete landing-page versions exist.
- Version 1 follows the minimal structure.
- Version 2 follows the short benefit structure and contains 3-5 benefit bullets.
- Version 3 follows the multi-section structure and includes a company/expert profile.
- All versions match the same approved audience, lead magnet, facts, CTA, and brand voice.
- Form microcopy, thank-you copy, and the immediate delivery email are present.
- No nurture sequence appears.
- No statistics, testimonials, credentials, deadlines, scarcity, guarantees, or legal text were invented.
- Missing details are marked consistently.
- Vietnamese uses hyphen-minus, not em dash.
- Visual work is handed to Bút Màu; implementation is handed to Coder/CRM.

---
name: client-assets
description: Use before any work on a client's own photos, logo, live page or text — picking which of their photos go in a new site's slots, cropping or retouching them, judging what they use now ("what do you think of my site?"), or building a rubric to score them. A candidate a design round renders goes to design-round instead.
---

# client-assets

A **client asset** is a photo, logo, live page or text the client already has.

## 0. Name the job first

Before any judgement, write which job the question is, in one line:

- **Judging in place**: any client asset, judged where it is used now, for the question the client asked. Run §1, and §2 where many assets are rated.
- **Choosing and preparing**: picking the client's photos for a new design, then cropping and editing them for their slots. Photos only, until a second kind of asset needs it. Run §2–§6.

A question that is both (Is my homepage photo good? Which photos should the new site use?) is two jobs: answer each under its own line, and never let a verdict for one stand as the other's.

## 1. Judging in place

Every verdict runs `design-vault:design-critique` in its in-place mode (its §5): a fresh critic given the client's question, the asset and where it is used.

## 2. The founder's eye first

For any pool of client assets to rate, in either job.

1. **Merge copies of a photo before he sees the pool.** Group copies of one photo by one test: the same pose, the same mouth and the same hands is one shot; a different moment is a separate photo. One card per shot, its copies listed on it. A ruling on any copy binds every copy.
2. **A sample on one contact sheet.** A critic drafts a verdict on 10–15 assets spread across the pool and its uses, on one contact sheet. The founder reacts; his reactions fix the rules. Write each rule with the asset he ruled as its example.
3. **A scoring sheet only where the pool is too big to review by eye.** It follows [references/scoring.md](references/scoring.md), and lives tracked in the project's repo as `docs/brand/scoring-<pool>.md`. Blind scorers and a test set of his rulings come only once the sample shows the rules hold.

## 3. Judge as the slot shows it

Judge each photo as its slot renders it: the actual crop the slot uses, at the target screen size, at 1x and 2x density, by eye. Show the founder that render, never the source file. An enlargement ratio is context only, never a verdict.

## 4. The review page

Build every review page from the plugin's shared shell ([../../review-page/README.md](../../review-page/README.md)): one card per asset (per shot, for photos), rendered as §3 says, his marks and notes read back with `ArtifactData`.

1. **Look before he looks.** Before the page reaches him, view every image on it at display size on one contact sheet, and confirm each shows what its card names. Record the check (each image, the size viewed, what it shows) in the Bound line of the ticket comment that hands him the page, or in your message to him where there is no ticket.
2. **His rules for the page** are a numbered list in a tracked file, `docs/brand/review-rules-<page>.md`, each rule with a check on the page's printed text (what the rendered page must or must not say, read with `python3 ~/design-vault/scripts/browse.py text <url>`). A check that matches nothing fails. A rebuild runs every old check before it ships.
3. **Notes on named items** are grouped by cause, and each cause measured across every item, before any one item is fixed (design-vault#90 W4).

## 5. Edits

1. **One line per edit**: the fault it removes for the viewer. An edit that cannot complete that line is not made.
2. **Prefer the smallest edit**, in this order: a crop, removing text, a recolour, a new background, removing a person. Ask the founder before removing a person.
3. **An edit can change what the photo claims happened**: a shared panel shown as a solo talk, a person filled out of a group. Name what the original shows happened and what the edit shows.
4. **The edit critic** runs under `design-vault:design-critique`, briefed with [references/edit-critic.md](references/edit-critic.md). Two critics judge each edit separately; it ships when both pass it, and a split goes to the founder.

## 6. Originals

Every source file comes from the project's client-originals store (`private/client-originals/`, set up by `design-vault:design-project`), and anything sent to the client is built from it with `python3 ${CLAUDE_PLUGIN_ROOT}/skills/design-project/scripts/client-originals.py send`. A crop, edit or review page reads from the store and writes elsewhere.

Ruled on design-vault#93; evidence in design-vault#89 and design-vault#90.

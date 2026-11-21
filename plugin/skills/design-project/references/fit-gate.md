# Client-fit gate — <client>

<client>'s own gate questions, in the form the vault's rule records set out (design-critique's `rules.md` in the installed design-vault build). One No fails the candidate (design-vault#113).

Report each question PASS, FAIL with what breaks it, or FIT RISK. **A question that rests on something <client> has not settled is a FIT RISK, shown to the founder for a ruling, never "not a defect" or "the client's call".**

A question rests only on what <client> gives as a fact or a goal, which its `strength` names, never on evidence or an estimate such as a guess at who visits.

## Audience

### <key>.audience
- applies-when: any; the candidate as a whole, as its reader first meets it
- question: Say in plain words how the candidate feels (childish, techy, salesy, calm, formal): does that feel fit <§1's audience, its seniority and register: "staff at development banks choosing an advisor: senior, formal, calm">?
- answered-by: look
- writes: register
- yields-to: level 1
- source: the rules file §1, from <client>'s answers; strength: <client fact or client goal>
- era: timeless
- owner: <key>

## The client's own colours and marks

`python3 ${CLAUDE_PLUGIN_ROOT}/skills/design-project/scripts/palette.py` answers `<key>.colours-script` in the installed design-vault build: <client>'s fixed logo colours as `--logo`, the other colours §2 marks fixed as `--fixed`, every colour the candidate's styles declare as `--colour`, and each large grey surface near the page ground as `--surface`. Where §2 records no fixed colour, delete both colour questions.

### <key>.colours-script
- applies-when: web-surface; every colour the candidate's styles declare, against <client>'s fixed colours
- question: Is each colour the candidate declares either one of <the fixed colours from §2, with hex values> or past the near-miss line from every one of them, so that palette.py exits 0?
- answered-by: script
- writes: palette
- yields-to: level 1
- source: the rules file §2, which records the logo colours as fixed; the near-miss line of design-critique's `vault.colour-distance`; strength: client fact
- era: timeless
- owner: <key>

### <key>.colours-look
- applies-when: any; every colour that sits beside <client>'s fixed colours or the mark
- question: Does each colour near <the fixed colours from §2> read as that very colour or as plainly another, with none that looks like a slightly-off copy of one?
- answered-by: look
- writes: palette
- yields-to: <key>.colours-script, level 1
- source: the rules file §2; strength: client fact
- era: timeless
- owner: <key>

### <key>.marks
- applies-when: any; every place one of <client>'s marks appears
- question: Is every mark <the marks from §4, with the colours each is drawn in> used as supplied, in a version on a ground §4's ground table allows, never redrawn, recoloured or cropped?
- answered-by: look
- writes: mark
- yields-to: level 1
- source: the rules file §4; strength: client fact
- era: timeless
- owner: <key>

## Standing rules

One question per rule or test in §6, each a copy of the block below with its own id. Set `applies-when` to the assets the rule covers, `answered-by` to `script` or `code` where one of those answers it, and `era` to `dated` and the review date where the client set it for a season. Once the questions are written, delete this paragraph, and the block too where §6 has no rule.

### <key>.<rule>
- applies-when: any; <the part of the candidate the rule is about>
- question: <the rule from §6 as a question a Yes passes: "Does it read as one experienced advisor, not a firm or an engineering practice?">
- answered-by: look
- writes: <the one property the rule decides>
- yields-to: level 1
- source: the rules file §6; strength: <client fact or client goal>
- era: timeless
- owner: <key>

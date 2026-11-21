# A vault gate for the affordance tally

### vault.affordance
- applies-when: web-surface; each part on the parts map's key, answered part by part
- question: Does vault.affordance hold?
- answered-by: look
- writes: affordance
- yields-to: none
- source: a made-up rule; strength: house judgement
- era: timeless
- owner: vault
- stage: treatment
- target: Build to vault.affordance.
- reasons: design-critique/references/house-principles.md#the-function-walk
- ledger: none
- status: live

### vault.edge-look
- applies-when: any; every part
- question: Does vault.edge-look hold?
- answered-by: look
- writes: edge
- yields-to: none
- source: a made-up rule; strength: house judgement
- era: timeless
- owner: vault
- stage: treatment
- target: Build to vault.edge-look.
- reasons: design-critique/references/house-principles.md#the-function-walk
- ledger: none
- status: live

### vault.one-target
- applies-when: web-surface; every part a visitor can act on
- question: Does vault.one-target hold?
- answered-by: script
- writes: tap target
- yields-to: none
- source: a made-up rule; strength: house judgement
- era: timeless
- owner: vault
- stage: value
- script: parts-map.py
- reasons: design-critique/references/house-principles.md#the-function-walk
- ledger: none
- status: live

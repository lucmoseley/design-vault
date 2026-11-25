# The review page

One shared page for anything the founder reviews card by card: a design round's candidates, a client's photos. It shows one card per item with a note box and the marks the data names, plus one note box for the whole set and, where asked, a single pick across cards. His answers save to the page's own store as he types, so a session reads them back instead of asking for them in chat (#120, ruled on #111).

## items.json

```json
{
  "title": "Hero art, round 2",
  "intro": "One paragraph above the cards: what he is judging and what to do.",
  "marks": [{ "id": "keep", "label": "Keep", "tone": "yes" }, { "id": "drop", "label": "Drop", "tone": "no" }],
  "pick": { "label": "Leader", "none": "No leader" },
  "pageNote": "What should the next round change?",
  "items": [
    { "id": "v1-arches", "name": "Arches", "line": "What it is for, in one line.", "image": "img/v1-arches.webp" },
    { "id": "v2-live", "name": "Water runs", "line": "A playable build.", "link": "https://preview.example/v2", "tag": "can't lead: fails craft gate" }
  ]
}
```

- Each item needs an `id`, a `name`, and an `image` (a file published beside the page) or a `link` (an `http://` or `https://` address for a live page or a motion candidate, which the card opens). `line` and `tag` are optional; a `line` keeps its line breaks. `"pickable": false` takes the card out of the pick, as for a design round's `can't lead` candidate.
- **An item's `id` keys its answers.** A rebuild that keeps an id keeps his note and mark on that card, so never renumber ids between rebuilds. Ids take letters, digits and `_ . ~ : @ + -`; `_page` is the set's own answer.
- `marks`, `pick` and `pageNote` are optional. A `tone` of `yes` or `no` colours a marked card.

## Publishing

1. Copy `index.html`, `review.js` and `page.js` from this folder (`<plugin root>/review-page/`, two levels up from a skill's base directory) into a folder under the working directory or the scratchpad: the Artifact tool publishes only files under those. Set the copy's `<title>` to the review's name.
2. Write `items.json` and the images there, each image at the path its item names.
3. Publish from the account the founder views in: the copied `index.html` as the page, `capabilities: {"db": {}}`, and `files` mapping `review.js`, `page.js`, `items.json` and every image to their copies.
4. **One link per review.** Every rebuild republishes to the same URL and sends only `items.json` and the new or changed images.
   A later session first reads the small page (`Artifact` `read` with the URL), lists its files (`scope: "files"`), then publishes the saved page with `url` and `files`. It never reads the images.

## Reading his answers

`ArtifactData` `list` with the page's `url` and `collection: "answers"`. Each card's answer is a document with the card's id: `{ mark, note, at }`. The set's answer is `_page`: `{ note, pick, at }`, where `pick` is a card id, `none`, or empty. `at` is when he last changed it, in milliseconds. A card he has not touched has no document.

## Changing the page

The saving rules live in `review.js`, and `test/review-page.test.js` tests them against a store double that freezes what it delivers, echoes the page's own writes, and replays older copies late. Copy every snapshot before use: the store freezes what it delivers, and a note written into a frozen answer is lost (#90 P7). A change to the saving rules gets a case there that fails without it.

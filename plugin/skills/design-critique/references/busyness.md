# Busyness

What makes a page look busy, and how busy each kind of visitor's page may be (#289). The records are `vault.busy-cues`, `vault.busy-density`, `vault.box-fills` and `vault.text-style-count`, in [rules/](../rules/). The research behind every line is the source checks on design-vault#289.

A project's rules file wins over every record here ([source precedence](house-principles.md#source-precedence)). [Tone](tone.md#white-space) sets how much white space a tone takes.

## What makes a page busy

Records: `vault.busy-cues`, `vault.element-count`.

- **Why.** A page looks busy when parts of low value compete with the parts the visitor needs, not when it holds many parts (NN/g, 2021), and a busy-looking page can pass by showing "sufficient information, and only sufficient information". Clutter's usual sources are redundant items, decorative icons, type flourishes, over-detailed or watermark images (NN/g homepage guidelines; Whitenton 2013) and borders, backgrounds and shadows used to group what space should group (Gordon 2021; Polaris). Perceived complexity is predicted (R2 .65, Reinecke et al. 2013, 450 sites) mostly by how much of the page is text and non-text content, how many text groups and how many image areas it holds; colour adds little, and symmetry and balance dropped out of the model. Screenshot metrics explain about half of complexity ratings along three lines: amount, organisation and how well parts stand apart (Miniukovich and De Angeli, abstracts). Rosenholtz's Feature Congestion measures clutter as how hard it is to add an item that still draws the eye. No source sets a value above which a web page is too busy, so the record is judged by eye, by the squint test.
- **Trade-off.** Cutting to look minimal can drop what the task needs; `vault.element-count` keeps the needed parts however busy they look.

## How busy for which visitor

Record: `vault.busy-density`.

- **Why.** Density is the value a visitor gets over the time and space the interface takes (Ström-Awn), so the right level follows the task. A working tool for repeat, skilled people goes dense: the Shopify admin "is high density by default", and Material makes high density opt-in for "List, tables, and long forms". A page judged at first sight pays for complexity: appeal falls strongly at high complexity and slightly at low (Reinecke et al. 2013).
- **Trade-off.** Too sparse fails too: NN/g found pages "too sparse" (2018) and, on wide screens, content dispersed across viewports, with "a clear preference for a condensed layout" (2023). Flat signifiers cost 22% more time and hold only where information density is low (Moran 2017).
- **Clash.** What a visitor tolerates follows age and culture: people over 45 liked low complexity more (Reinecke et al.), and Chinese users preferred "fairly high information density" while still missing features on complex sites (Cheng and Nielsen 2016). The record moves a step only where the brief states the audience. The one-step moves are the house's; neither study measured a step. `vault.tone-space` sets the space between groups by tone and yields to this record on a working view's density.

## Coloured boxes

Record: `vault.box-fills`.

- **Why.** A filled, labelled rectangle reads as a button: "giving headings a background color will make them resemble buttons when they're not", and "Avoid having many colorful boxes of different sizes on a page", since people "have difficulty picking out the clickable elements when similar-looking items compete" (NN/g, Loranger 2015). Polaris keeps vibrant fills for "smaller surface areas" such as buttons and badges, and calls bright or contrasting container colours "a cluttered UI"; a grey ground "visually recedes".
- **Trade-off.** No source gives a count of coloured boxes a page may hold; the record judges competition with the controls, not a number. A marketing hero may take a coloured ground on purpose (`docs/research/surface-styling.md` B5.3); Polaris's lines are admin guidance, so the large-container clause binds working views only.

## Text styles

Record: `vault.text-style-count`.

- **Why.** Each extra face, size, weight or colour is one more thing to read as a level of the hierarchy. Apple says to "Minimize the number of typefaces" and use the built-in text styles; GOV.UK sets text from a fixed scale, with bold "sparingly" and the lead paragraph once a page; NN/g's homepage guideline 63 says to "Limit font styles and other text formatting".
- **Trade-off.** Too few styles hide the key elements: "Using the same body size everywhere can make it hard for merchants to identify key elements" (Polaris). NN/g's "no more than 3 sizes" and "a maximum of 2" big elements (Gordon 2021) are expert practice with no study behind them, and a type scale with several heading levels exceeds three sizes; the record holds the two-big-elements line and leaves the size count to the scale.
- **Clash.** The face count is `vault.face-roles`', the weight count `vault.weight-count`'s and the text colours `vault.text-steps`'; this record owns only their combinations.

# Higgsfield "50% off models you select" — research

Date: 2026-10-06. Status: complete. Labels: **Verified** = Higgsfield's own page or page code, with URL and quote. **Unverified** = other sources. **Unknown** = no source found.

Method: the higgsfield.ai pricing page builds its plan cards with JavaScript, so we read the help centre (plain HTML), Higgsfield's blog, the API console pages and their JavaScript bundles, and three public endpoints that need no sign-in. We did not sign in or buy anything.

## Q1. What is the offer?

**Best match — Verified.** The API console (https://console.higgsfield.ai, also called open.higgsfield.ai) has a "max-discount" launch offer. You select models, and those models get their maximum discount.

- FAQ on https://console.higgsfield.ai/pricing: "Sign up to get 15% off all sale models. Choose any 3 models for discounts of up to 75%. Verify your business email and add a card to get $15 on your balance."
- Console banner text (bundle `dashboard-promotions-*.js`): "Up to {N}% off for {days} days – Select {max_selections} discounted models for free". Sub-line: "Celebrating the launch of Higgsfield API with max discount on the most advanced models". Button: "Select discounts".
- The public price list (`GET https://dash.higgsfield.ai/api/v2/pricing/models/`) gives a 50% max discount on most models: Kling 3.0, Kling O3, Wan 2.6, Wan 2.7, Wan 3.0, MiniMax H3, Happy Horse 1.x. This fits the words "50% off models you select".

This offer is on the **API** product, not on a web plan. It needs no paid plan. The brief says the offer was seen on the web app. We found no model-selection discount in the higgsfield.ai web-app code.

**If the offer was on higgsfield.ai — Verified (category only).** The web app shows "Exclusive Offers" (https://higgsfield.ai/creator-hub/help-center/plans/what-are-exclusive-offers): "limited-time deals Higgsfield shows to active subscribers: a discounted plan upgrade or an add-on such as extra credits, Unlimited access to specific models, or priority processing. Each offer is a one-time purchase at a promotional price." "Exclusive Offers are personalized." The web code also has a credit-pack "chase" pop-up ("up to X% off" credit packs, with a countdown). The exact terms of a web offer are **Unknown**.

Other "pick a model" features on the web (Verified): the Creator plan card has "One more Unlimited Model" (pricing-page code). The "Unlimited Models Marketplace" sells "Unlimited access to individual models as bundles" (https://higgsfield.ai/creator-hub/help-center/credits/what-are-unlimited-models-and-which-plans-include-them). These are not percentage discounts.

## Q2. How many models? Can you change them?

API console offer — **Verified**:

- Number: "Choose any 3 models" (FAQ). The live number is the field `max_selections`, with a quota for each type (image, video). "Remove a selected model in this category before choosing another."
- Change: **No.** Confirm dialog: "Confirm your choice, this can’t be changed later." After the claim: "Your picks are already spent".

Web Exclusive Offers: **Unknown** (no selection rules published).

## Q3. Does it expire?

API console offer — **Verified: yes.**

- Confirm dialog: "Discount will be available for the next {N} days." The pricing hero says "{N}-day limited offer".
- More top-ups give a longer period: "Top up ${X} more to get {N}-day max discount". Code fallback values are $200 → 7 days and $1,000 → 30 days. The live values are **Unknown**.
- Partners can get a "1-year max discount" through sales.

Web Exclusive Offers — **Verified: yes.** "The purchase window is shown with a countdown". "Its benefits last for the period stated in the offer". Offers that unlock access "are non-refundable once the access is granted".

## Q4. API or web app?

**Verified.** The two products have separate billing (https://higgsfield.ai/creator-hub/help-center/integrations/what-is-the-higgsfield-api, Sep 16, 2026):

- "Your plan, credits, and Unlimited access exist only on the website; the API runs on its own account balance in US dollars."
- "Having or not having a plan on higgsfield.ai changes nothing about API access or rates."
- "MCP and CLI ... attach Claude, Cursor, or another agent to your existing higgsfield.ai account, and everything they generate deducts your plan credits."

Consequences:

- Web Unlimited and free generations do not apply to the CLI: "any generation made outside it, including through MCP, CLI, Canvas, Supercomputer ... always deducts credits, regardless of plan" (https://higgsfield.ai/creator-hub/help-center/credits/how-credits-work).
- Whether a web percentage discount on credits applies to CLI use is **Unknown**.

## Q5. Prices

**Web plans — Verified.** Higgsfield's blog (https://higgsfield.ai/blog/best-unlimited-ai-video-generators, pages read Sep 11, 2026) and the public plan list (`GET https://fnf-api-gw.higgsfield.ai/fnf/subscriptions/plans`) agree:

| Plan | Monthly | Annual (per month) | Credits per month |
|---|---|---|---|
| Starter | $15 | $15 | 200 |
| Plus | $49 | $39 | 1,000 |
| Ultra | $129 | $99 | 3,000 |

The plan list also holds other variants (Plus $59 / $47 with 1,200 credits; Ultra with 6,000 or 9,000 credits; Creator $250 with 6,000 credits). Which variant an account sees is **Unknown**. Secondary sites quote Starter $19 / 270 credits (**Unverified**).

Extra web credits: Auto-Refill "$1 = 18 credits", "Not available on entry-level plans" (https://higgsfield.ai/creator-hub/help-center/credits/how-does-auto-refill-work). Credit Packs need "an active subscription".

**Web credits per generation.** Higgsfield shows the cost "on the Generate button before you confirm". It publishes no full table. Known: Nano Banana 2 is "2 credits per image" at 1K/2K and 4 credits at 4K (https://higgsfield.ai/blog/unlimited-nano-banana-2-plans). Other models: **Unknown**. `higgsfield generate cost <model> ...` returns the cost before a run.

**API prices — Verified** (`GET https://dash.higgsfield.ai/api/v2/pricing/models/`, read 2026-10-06). "from" price, list → max-discount:

| Model | List | Max-discount |
|---|---|---|
| Kling 3.0 | $0.084/s | $0.042/s (50%) |
| Seedance 2.5 | $0.2057/s | $0.144/s (30%) |
| Seedance 2.0 | $0.1407/s | $0.0985/s (30%) |
| Wan 2.6 / 2.7 | $0.10/s | $0.05/s (50%) |
| Wan 3.0 | $0.05/s | $0.025/s (50%) |
| Ideogram 4.0 | $0.03/image | no discount |
| Qwen Image 3 | $0.04/image | no discount |
| Grok Imagine 2.0 | $0.04/image | no discount |
| Grok Imagine Video 1.5 | $0.08/s | no discount |
| Soul 2 | $0.0032/image | no discount |
| Soul Standard | $0.0938/image | no discount |

GPT Image 2, Nano Banana Pro, Seedream 4.5, Veo and Sora are not in the public API price list. DoP is "priced per generation" (help centre), but its price is not in the list. Per-request cost: `POST https://api.higgsfield.ai/estimate/<model>` (https://docs.higgsfield.ai/docs/concepts/billing-and-retention.md).

## Q6. Read the balance by program

- **Web credits — Verified.** CLI README (https://github.com/higgsfield-ai/cli, v1.1.26): "`higgsfield account` | credits balance, transactions". Higgsfield's skills repo: "Verify: `higgsfield account status`. Expect `<email> — <plan> plan, <N> credits`." Add `--json` for machine output. No public REST endpoint for the web balance is documented.
- **API USD balance — Verified absence in the docs.** The API docs and OpenAPI file list no balance endpoint. The balance is in the console ("Billing holds your current balance"). The console uses a private, session-only `/api/v1/credits/balance/` on dash.higgsfield.ai; it is not part of the documented API.

## Q7. Do credits expire?

**Verified** (https://higgsfield.ai/creator-hub/help-center/credits/how-credits-work and .../top-up-credits-expire):

- Subscription credits: "unused credits expire at renewal". Annual plans reset "every 30 days".
- Credit Pack, Auto-Refill and Boost credits: "90 days from purchase".
- Promo credits: "on the date shown when issued".
- Spend order: "Subscription credits are always spent first", then the balance that expires soonest.
- API funds: "Funds expire one year after they are added to the balance." Minimum top-up "$5".

## Summary

Action: ask the founder whether he saw the offer at higgsfield.ai or at console/open.higgsfield.ai before he selects. The choice is final. Owner: #64 (pick the discounted models and top up).

## Re-check, 8 Oct 2026 (#64)

Re-read from the console's live page code (`console.higgsfield.ai/pricing` and its bundles), the public price list and Higgsfield's pages, with no sign-in. It corrects two points above.

- **Still final — Verified.** The confirm dialog still reads "Confirm your choice, this can’t be changed later. Discount will be available for the next {N} days." (`pricing-*.js`). A model past the quota shows "Your picks are already spent". Picks can be removed only before the claim.
- **How many — Verified, corrected.** 2 video and 1 image: `[{modality:"video",quota:2},{modality:"image",quota:1}]` (`IconTagFilled-*.js`). The live quota comes from the server's offer. The claim button works only when every quota is filled, so all picks are claimed at once.
- **The window — corrected.** The "$200 → 7 days, $1,000 → 30 days" figures in Q3 are not fallbacks. They are dev-preview mock data (`billing-credits-buy-modal-*.js`, used only by mock scenarios that this production build never selects). The pick window is the server field `discount_duration_days`. Its live value is **Unknown** without sign-in. Third parties (MindStudio, 18 Sep, **Unverified**) say "7 days".
- **Two offers, not one — Verified, new.** A separate top-up promotion gives a max discount on *all* sale models for a time, at top-up milestones the server sets (`/api/v1/credits/topup-promotion/`). While its entitlement is active, the console hides and blocks picking: `j=…entitlement?.status==="active"` gates the pick panel, the confirm dialog and the claim. Pick first, top up after.
- **Offer end — Unknown.** No Higgsfield page gives an end date. Higgsfield's blog (1 Oct) calls API discounts "temporary promotions". The offer is still served on 8 Oct, past the third parties' "7 days from release" (16 Sep).
- **Prices — unchanged.** Kling 3.0 50%, Seedance 2.0 and 2.5 30%, Wan 2.7 50%, Marketing Studio Image 15% (its sign-up rate, so the image pick gains nothing). A pick's rate replaces the 15%, not stacking on it: Kling's $0.042 is exactly half of $0.084 (inferred, not stated).
- **Signed-in only:** the live day count, quotas, top-up milestones and campaign end. The console's banner and confirm dialog show the day count before anything is claimed.

Effect on #64: with two video picks, Kling 3.0 and Seedance 2.0 take them, and Wan 2.7 drops out. A top-up is not part of the pick, and one made first can block it.

## Signed-in read, 8 Oct 2026 (#64)

Read from the founder's signed-in console through Claude in Chrome, with nothing clicked. The offer's API bodies could not be read, because the browser tool lists requests without their bodies. The page text settles the window:

- **The window is 7 days.** Dashboard banner: "UP TO 75% OFF FOR 7 DAYS – SELECT 3 DISCOUNTED MODELS FOR FREE". Pricing hero: "GET UP TO 75% OFF ON 1 IMAGE + 2 VIDEO MODELS" / "7-DAY LIMITED OFFER". The code's `discount_duration_days` drives both, so this is the window that starts at the pick.
- **Nothing is claimed yet.** The "Get started" checklist has "Save up to 75% on 3 models" unticked, and "Get 15% off all models" ticked.
- **Max discounts on the account's own table:** Kling 3.0 50%, Seedance 2.0 and 2.5 30%, Marketing Studio Image 15%. Wan 2.7 was not on the table's first page.
- No top-up promotion banner was seen. The dashboard banner has a second slide, which was not read.
- **Still unknown:** whether picks can be made again after the 7 days, and when the offer itself ends.

## Is the pick one-time? 8 Oct 2026 (#64)

From the console's live code and FAQ, with nothing clicked.

- **Most likely once per account. This is inferred: no page states it.**
  - The FAQ calls it "the Higgsfield API launch offer": "Choose any 3 models for discounts of up to 75%."
  - After the claim, the offer's `state` is `max_applied`. The pick panel and hero render only while the server sets `can_advance` (`Ua(e)=!!e?.can_advance&&…`).
  - No string anywhere offers picking again, renewing, or a new round of picks.
  - Only Higgsfield can confirm. Ask support before relying on a second window.
- **A window can be extended by a top-up — Verified (code), amounts server-set.** A server-sent pop-up (`topup_discount_ending_upsell`) reads "{N}-day discount ends soon", "Top up and get {M} days more", and "Top up {$X} to keep your max discount on all models below for {M} more days". The code's sample values are 7 days, $1,000 and 30 days.
- **The offer's own end date: Unknown,** and switchable by the server at any time. The September cashback campaign ended on 30 Sep. Launch promotions are being wound down.
- **Cashback is a separate scheme** that repeats every 30 days. A generation paid from cashback gets no model discount (FAQ: "Generations paid with cashback use the standard price").

Effect on #64: treat the 7 days as the only window. Time the pick to the largest batch of Kling or Seedance renders, not the first clip.

## Support's answer, 8 Oct 2026 (#64)

Reply from Higgsfield Customer Care to the founder's email of 8 Oct, 18:04, which named the API account.

- **The pick is one-time — Verified (support).** "The selected-model discount is part of the welcome discount for a new API key. It runs for one week from activation, and the selected models return to standard pricing afterward. The documented flow describes one welcome-discount period and does not provide a second model-selection window after it ends, so it should be treated as a one-time selection rather than a recurring benefit." This settles §Is the pick one-time?, which had inferred it.
- **"From activation" means from the pick, not from the key's creation.** Inferred: the key was saved on 30 Sep (`~/.higgsfield.env` mtime), and on 8 Oct, eight days later, the console still offered the picks unclaimed (§Signed-in read).
- **Offer end — still Unknown.** "There is currently no published end date for the overall API launch offer, so we cannot confirm a specific cutoff." Support names the live console as the source of the current offer, and https://open.higgsfield.ai for each model's current rate.
- **"Standard pricing" after the week is not defined.** Whether it means the 15% sign-up rate or list price is not stated. The free `/estimate` call after the window will show which.
- The top-up extension (§Is the pick one-time?) was not asked about and goes unmentioned in the reply.

Effect on #64: the plan stands. There is one 7-day window, so time the pick to the largest batch of Kling or Seedance renders. The offer can still be withdrawn before then, at a small cost per clip.

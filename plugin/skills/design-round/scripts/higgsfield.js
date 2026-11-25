#!/usr/bin/env node
/**
 * Renders brand-art and video candidates through Higgsfield's pay-per-request
 * API (design-vault#18, design-vault#62).
 *
 * Usage:
 *   node higgsfield.js [--estimate] --out <r<n>/v<n>-<name>> --model <endpoint id> --prompt <text>
 *                      [--aspect-ratio <w:h>] [--resolution <tier>] [--set <field>=<value>] ... [--max-usd <dollars>]
 *   node higgsfield.js [--estimate] --batch <jobs.json>
 *
 * `--model` is the endpoint id on the model's page at docs.higgsfield.ai, such
 * as `recraft/v4.1/pro/text-to-image`. `--set` adds any other field of that
 * model's request body; a value that parses as JSON is sent as JSON
 * (`--set 'colors=[{"rgb":[40,90,150]}]'`). A jobs file is a JSON array of
 * `{ out, model, prompt, aspect_ratio?, resolution?, params?, max_usd? }`.
 * `--estimate` prices the jobs and stops, taking back any round folder it made
 * to learn whether a run could make it.
 *
 * Some models, among them FLUX.2, GPT Image 2.5 and Seedance 2.0 and 2.5,
 * estimate as a price rule in words with no usd figure (design-vault#49). Such
 * a job runs only with a `max_usd`: the most it can cost, worked out from the
 * rule by whoever writes the job. The ceiling binds on that figure and the
 * ledger records it, since the API reports no actual charge; the console shows
 * what was taken.
 *
 * Environment, read from `~/.higgsfield.env` (`export NAME=value` lines, chmod 600)
 * wherever the process environment lacks it:
 *   HIGGSFIELD_API_KEY            `<key id>:<key secret>`, as the Higgsfield console issues them
 *   HIGGSFIELD_ROUND_CEILING_USD  the most one round may spend, set by the founder
 *
 * For a batch, in order:
 *   1. takes each round's lock, `r<n>/higgsfield.lock`, until the batch ends, so a
 *      second run on the round is refused, as is a run finding the lock of one that
 *      ended without releasing it; a round reached by two spellings, through a
 *      symlink or a case-differing path on /mnt/c, is one round;
 *   2. prices every job through Higgsfield's estimate endpoint, and prints the prices;
 *   3. refuses the whole batch, before submitting anything, where that total
 *      would take a round past its ceiling;
 *   4. appends each job's charge at its estimate to the round's ledger,
 *      `r<n>/higgsfield-spend.jsonl`, with any discount the estimate names,
 *      which its usd is already net of, before submitting it; then submits it,
 *      polls it to the end, and appends each step's line under the job's
 *      idempotency_key, the last of which is the job's charge;
 *   5. saves the image or video as `r<n>/v<n>-<name>.<ext>`, under its sniffed type.
 *
 * A submission refused 403 means the balance ran out: the batch stops there,
 * naming the jobs that ran, since the API has no balance to read beforehand
 * (design-vault#61). A submission that ends on a network fault, a 5xx, an
 * answer with no request_id, or a refusal answering a retry may have reached
 * Higgsfield: the batch stops there too, with that job recorded at its estimate.
 *
 * A failed, moderated or cancelled request, or a submission refused at its
 * first try, is not charged, so its outcome is recorded at $0. One that
 * outlives the timeout, or whose status cannot be read, is recorded at its
 * estimate, since it may still complete and be charged. An
 * estimate that is not a positive usd figure is refused before anything is
 * submitted. A completed request is recorded whatever it returns; an output
 * carrying no URL counts the job failed.
 */
"use strict";
const { render, parseArgs, settings } = require("./higgsfield-client.js");

const USAGE =
  "Usage: node higgsfield.js [--estimate] --out <r<n>/v<n>-<name>> --model <endpoint id> --prompt <text> [--aspect-ratio <w:h>] [--resolution <tier>] [--set <field>=<value>] ... [--max-usd <dollars>]\n" +
  "       node higgsfield.js [--estimate] --batch <jobs.json>";

async function main(argv = process.argv.slice(2)) {
  let parsed;
  try {
    parsed = parseArgs(argv);
  } catch (error) {
    console.error(`higgsfield.js: ${error.message}\n${USAGE}`);
    process.exitCode = 2;
    return;
  }
  try {
    const env = settings(process.env);
    const failed = await render(parsed.jobs, {
      estimateOnly: parsed.estimateOnly,
      credentials: env.HIGGSFIELD_API_KEY,
      ceiling: env.HIGGSFIELD_ROUND_CEILING_USD,
    });
    process.exitCode = failed ? 1 : 0;
  } catch (error) {
    console.error(`higgsfield.js: ${error.message}`);
    process.exitCode = 1;
  }
}

if (require.main === module) main();

module.exports = { main };

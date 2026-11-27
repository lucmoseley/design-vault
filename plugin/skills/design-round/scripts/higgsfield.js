#!/usr/bin/env node
/**
 * Renders brand-art and video candidates through Higgsfield's pay-per-request
 * API.
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
 * estimate as a price rule in words with no usd figure. Such a job runs only
 * with a `max_usd`: the most it can cost, worked out from the rule by whoever
 * writes the job. The ceiling binds on that figure and the ledger records it,
 * since the API reports no actual charge; the console shows what was taken.
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
 * An estimate or submission answered with a network fault, a 5xx, a 408 or a
 * 429 is tried again within its retry deadline, after at least its
 * Retry-After, a submission under the same idempotency key. A submission
 * refused at its first try, or after only 429s and refusals, is not charged: it is
 * recorded at $0 and the batch stops there, naming
 * the jobs that ran and those not submitted. A 403, at any try, means the
 * balance ran out. A submission that ends on a network fault, a 5xx, a 408, an
 * answer with no request_id, or a refusal answering a retry of any of those
 * may have reached Higgsfield: the batch stops there too, with that job
 * recorded at its estimate.
 *
 * A failed, moderated or cancelled request is not charged, so its outcome is
 * recorded at $0. A status read that fails to a network fault, a 5xx, a 408,
 * a 429 or an answer with no status is read again on the poll schedule. One
 * that outlives the timeout, whose status read is refused with another 4xx, or
 * whose status still cannot be read at the timeout, is recorded at its
 * estimate, since it may still complete and be charged. An estimate that is
 * not a positive usd figure is refused before anything is submitted. A
 * completed request is recorded whatever it returns;
 * an output carrying no URL counts the job failed.
 *
 * A ledger line that cannot be written stops the batch, naming how far that
 * job got, with its request id and output URLs where it has them, and the jobs
 * that ran and those not submitted. The one exception is an accepted job's
 * submitted line: the job is polled on, its outcome line stands in for it, and
 * the batch stops only where that outcome line cannot be written either. A
 * completed job's outputs are saved before the batch stops. A write cut off
 * part-way is cut back. A ledger line that is not JSON, as a run
 * killed mid-write leaves, refuses every run on its round, naming its file and
 * line number.
 */
"use strict";
const { render, parseArgs, readSettings } = require("./higgsfield-client.js");

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
    const env = readSettings(process.env);
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

# Practice: node-and-python-cli-scripts
Researched: 2026-11-15

Scope: small Node or Python command-line tools and scripts. Each source has one tier: [standard or field body], [named expert], [survey or curated list] or [unverified]. A tool's own docs earn [standard or field body] only for what that tool does.

## 1. Use the language argument parser. Pass argv in as a parameter.
- Use the standard parser. Do not parse argv by hand. [standard or field body] GNU Coding Standards, 4.2: "Use `getopt_long` to decode arguments, unless the argument syntax makes this unreasonable."
- The runtime parsers are `argparse` (Python) and `util.parseArgs` (Node). [standard or field body] Python argparse docs; Node util docs (each for its own tool).
- Pass an explicit list to the parser. Python: `parse_args(args)`. Node: `parseArgs({ args })`. Tests then need no real process. [standard or field body] Python argparse docs, "Beyond sys.argv"; Node util docs, `args` default.
- Option syntax: one alphanumeric letter after a hyphen. `--` ends the options. [standard or field body] POSIX Utility Conventions, Chapter 12, Guidelines 3, 4 and 10.
- Give each flag a long name too (`--help` and `-h`). Use standard names where a standard exists. [named expert] clig.dev, "Arguments and flags".
- Make argument order not matter where possible. Accept `-` for stdin or stdout when input or output is a file. [named expert] clig.dev, "Arguments and flags".

## 2. Usage errors: short help, stderr, exit 2
- On bad input, show concise help and say how to get more. [named expert] clig.dev, "Help".
- Python: `parser.error(message)` prints usage and message to stderr, then exits 2. [standard or field body] Python argparse docs, "Exiting methods".
- Click (Python): `UsageError.exit_code = 2`. [standard or field body] Click source, `src/click/exceptions.py`.
- Node: an unknown option throws `TypeError` with code `ERR_PARSE_ARGS_UNKNOWN_OPTION` when `strict` is true, the default. [standard or field body] Node source, `lib/internal/errors.js` and `parse_args.js`.
- Catch that error in the script. Print it to stderr and set `process.exitCode = 2`. [unverified] Derived from the Node entry above; no source states it, so it sets no default.

## 3. Exit codes: 0 success, 1 fault, 2 usage
- Exit 0 on success. Exit non-zero on failure. Map the main failure modes to codes. [named expert] clig.dev, "The Basics".
- Fault 1 in three tools: Click `ClickException.exit_code = 1`; Python `sys.exit(obj)` with a non-integer exits 1; Node uncaught exception exits 1. [standard or field body] Click source; Python `sys` docs, `sys.exit`; Node process docs, "Exit codes".
- Python `sys.exit()` and `sys.exit(None)` exit 0. Most systems need integer codes in the range 0 to 127. [standard or field body] Python `sys` docs, `sys.exit`.
- Node `process.exitCode` sets the code. A later `process.exit(code)` overrides it. [standard or field body] Node process docs, `process.exitCode`.
- Conflict: sysexits(3) gives `EX_USAGE` 64 and `EX_DATAERR` 65. [standard or field body] OpenBSD sysexits(3), DESCRIPTION.

## 4. Stdout and stderr
- Main result to stdout. Errors, warnings and log lines to stderr. [named expert] clig.dev, "The Basics" and "Output".
- Do not use stderr as a log file by default. Show no animation when stdout is not a terminal. [named expert] clig.dev, "Output".
- `--help` prints to stdout, then exits successfully. `--version` prints to stdout. The error stream is not stated. [standard or field body] GNU Coding Standards, 4.8.1 and 4.8.2.
- Python: `print_help()` and `print_usage()` default to stdout. `error()` writes to stderr. [standard or field body] Python argparse docs, "Printing help" and "Exiting methods".
- Node: `process.exit()` can end the process before pending stdout writes finish. Set `process.exitCode` and let the process end. [standard or field body] Node process docs, `process.exit([code])`.

## 5. Deterministic output (four sources agree)
- Sort keys before output: Python `json.dumps(obj, sort_keys=True)`. [standard or field body] Python json docs, "Basic Usage".
- Python set iteration order follows string hashes. Those hashes are random unless `PYTHONHASHSEED` is set to an integer. [standard or field body] Python command-line docs, `PYTHONHASHSEED`.
- Sort explicitly. Reproducible Builds gives the Perl case: "To get a deterministic output, the easiest way is to explicitly sort the keys." [standard or field body] Reproducible Builds, "Stable outputs" (scope: build outputs).
- Give a `--json` or `--plain` flag for scripts. [named expert] clig.dev, "Output" and "Future-proofing".
- Timestamps and hostnames in output: no source found. Keep them out of machine output. [unverified] Derived, not sourced, so it sets no default.

## 6. Keep logic pure. The entry point parses argv and calls it.
- Python: put the work in a `main()` function. Keep the `__main__` block short. [standard or field body] Python `__main__` docs, "Idiomatic Usage".
- Node: `if (require.main === module) main();` runs only when the file is the entry point. [standard or field body] Node modules docs, "Accessing the main module".
- Keep decision logic pure and I/O at the edge. [named expert] Gary Bernhardt, "Boundaries" talk page (Destroy All Software), which links his "Functional Core, Imperative Shell" screencast. Neither was read in full.

## 7. Numeric options: convert, check the range, report with exit 2
- Convert the text to an integer when parsing. Reject non-integers there. Python: a `type=` function that raises `ArgumentTypeError`, `TypeError` or `ValueError`. [standard or field body] Python argparse docs, "type".
- Node `parseArgs` accepts only `string` and `boolean` types. The script converts and checks the number itself. [standard or field body] Node source, `parse_args.js`, `validateUnion`.
- Check the range after the data loads. The parser cannot know the range. [unverified] Derived from the two parser docs, so it sets no default.
- The message states the valid range in the user's numbers, for example "1 to N". POSIX: "the utility's diagnostic message shall indicate that the value is out of the supported range." [standard or field body] POSIX Chapter 12, Section 12.1, item 6.
- Rewrite the error for a person. [named expert] clig.dev, "Errors": "Catch errors and rewrite them for humans."
- Python: call `parser.error(message)` for the range error. [standard or field body] Python argparse docs, "Exiting methods".
- Convert once to a value that is already checked. Later code then needs no second check. [named expert] Alexis King, "Parse, don't validate" (2019).

## 8. Remote calls: a timeout on every call, and a total deadline over its retries (three sources agree)
- Set a timeout on every remote call, a request timeout as well as a connection timeout. [named expert] AWS Builders' Library, "Timeouts, retries, and backoff with jitter".
- With no deadline a client can wait "effectively forever"; always set a realistic one, an educated guess validated by load testing. [named expert] gRPC docs, "Deadlines" guide.
- Higgsfield's API: "Set maximum attempts and a total retry deadline." [standard or field body] docs.higgsfield.ai, Errors page, for its own API.
- Choose the value from the downstream service's latency at an accepted false-timeout rate (p99.9 for 0.1%). [named expert] AWS Builders' Library, same article.

## Open points
- Usage code 2 has two agreeing sources (argparse, Click). GNU grep uses 2 for any error and 1 for no match. Three sources do not agree; the convention stays a house choice.
- Survey or curated list: none used. Paywalled sources: none met.
- Reached only in part: GNU html_node page (rate-limited; standards.html read instead); Bernhardt talk and screencast; ECMAScript object key order.

#!/usr/bin/env bash
# design-round-pointer.sh — points a session at the design-round skill the first time it reaches for a
# rendering skill (lucmoseley/mantahostels#3537).
#
# The first rendering-skill call is the moment the rule line names ("before
# rendering a candidate"), so the pointer lands there and nowhere else.
#
# Two routes, one marker:
#   PreToolUse, matcher Skill — the model loads a skill. The name arrives as
#     `.tool_input.skill`, namespaced for a plugin skill (`workflow-core:animate`).
#   UserPromptSubmit — the founder types `/design` or another matched command,
#     which expands in the prompt and makes no Skill call.
#
# IMPLICIT:  injects the design-round pointer, once per session, into a session that loads or types `design`, `prototype`, `animate`, `design-mode` or an `impeccable` skill — plus one clause when ~/design-vault is absent.
# JUSTIFIED: fail-safe — a round rendered without the method skips the direction cards, the fresh critic and the record, and nothing downstream notices.
# DEFEAT:    none needed; it only points. Loading `design-vault:design-round` first spends the marker, so the pointer never repeats what the session already holds.
#
# It never refuses the call and never reads the tracker: every path exits 0, but for
# an unset variable under -u, which exits 1, a non-blocking error to Claude Code.

# No -e: a hook goes on past a failure rather than stop at an untested one (workflow-core#1315).
set -uo pipefail

command -v jq >/dev/null 2>&1 || exit 0

payload="$(cat)"
field() { printf '%s' "$payload" | jq -r "$1 // \"\"" 2>/dev/null; }

event="$(field '.hook_event_name')"

# The rendering skills, by bare name. A plugin skill arrives namespaced
# (`workflow-core:animate`), so the part after the last colon is what matches;
# any skill of the impeccable plugin matches on the plugin's name.
RENDERING=(design prototype animate design-mode)

# classify <name> — sets `matched` for a rendering skill, `spent` for
# design-round itself, neither for anything else.
matched=""
spent=""
classify() {
  local base="${1##*:}" r
  [[ "$base" == design-round ]] && {
    spent=1
    return
  }
  [[ "$1" == impeccable || "$1" == impeccable:* ]] && {
    matched=1
    return
  }
  for r in "${RENDERING[@]}"; do
    [[ "$base" == "$r" ]] && {
      matched=1
      return
    }
  done
}

case "$event" in
  PreToolUse)
    [[ "$(field '.tool_name')" == Skill ]] || exit 0
    classify "$(field '.tool_input.skill')"
    ;;
  UserPromptSubmit)
    # Anchored at the prompt's start: a typed command runs only from there, and a
    # prompt that merely mentions `/design` is not loading it.
    if [[ "$(field '.prompt')" =~ ^[[:space:]]*/([A-Za-z0-9_:-]+)([[:space:]]|$) ]]; then
      classify "${BASH_REMATCH[1]}"
    fi
    ;;
  *) exit 0 ;;
esac

[[ -n "$matched$spent" ]] || exit 0

# Built before the marker is reserved: a firing that produces no text spends
# nothing, so the next one still injects.
out=""
if [[ -n "$matched" ]]; then
  # shellcheck disable=SC2016 # the backticks are markdown, not a substitution
  text='This project runs design rounds through `design-vault:design-round`; invoke it before rendering a candidate.'
  if [[ ! -d "${HOME-}/design-vault" ]]; then
    text+=' The design vault is not at ~/design-vault on this machine: for the brief'"'"'s Reference field, read the project'"'"'s derived export of the library where it has one, or write "none cited".'
  fi
  out="$(jq -nc --arg e "$event" --arg c "$text" \
    '{hookSpecificOutput: {hookEventName: $e, additionalContext: $c}}' 2>/dev/null)"
  [[ -n "$out" ]] || exit 0
fi

# Once per session: a marker keyed on the session id, outside the repo, reserved
# with noclobber so two firings racing each other cannot both win. Only a marker
# that already exists means "said": no session id, or a marker that cannot be
# written, and the pointer is said anyway rather than never.
#
# RESIDUAL: the marker outlives a compaction, so a session whose context was
# summarised away does not get the pointer again.
session="$(field '.session_id')"
if [[ -n "$session" ]]; then
  state_dir="${TMPDIR:-/tmp}/design-round-pointer-${UID:-0}"
  marker="$state_dir/${session//[^A-Za-z0-9_-]/_}"
  mkdir -p "$state_dir" 2>/dev/null
  set -o noclobber
  if ! { : >"$marker"; } 2>/dev/null; then
    [[ -e "$marker" ]] && exit 0
  fi
  set +o noclobber
  # Markers over a day old are swept: a guess. A session running longer may get the pointer again.
  find "$state_dir" -maxdepth 1 -type f -mmin +1440 -delete 2>/dev/null
fi

[[ -n "$out" ]] && printf '%s\n' "$out"
exit 0

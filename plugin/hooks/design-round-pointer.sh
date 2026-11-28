#!/usr/bin/env bash
# Usage: printf '%s' "$hook_payload_json" | bash design-round-pointer.sh
#   PreToolUse, matcher Skill: reads `.tool_input.skill`.
#   UserPromptSubmit: reads a `/command` at the start of `.prompt`.
#   SessionStart, matcher compact: clears `.session_id`'s marker, printing nothing.
#   Prints `{hookSpecificOutput: {hookEventName, additionalContext}}` once per `.session_id`, and once more after each
#   compaction, for a rendering skill; nothing otherwise. Exits 0 on every path, 1 on an unset variable.

# workflow-core#1315
set -uo pipefail

command -v jq >/dev/null 2>&1 || exit 0

payload="$(cat)"
field() { printf '%s' "$payload" | jq -r "$1 // \"\"" 2>/dev/null; }

event="$(field '.hook_event_name')"

session="$(field '.session_id')"
state_dir="${TMPDIR:-/tmp}/design-round-pointer-${UID:-0}"
marker="$state_dir/${session//[^A-Za-z0-9_-]/_}"

RENDERING=(design prototype animate design-mode)

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
    if [[ "$(field '.prompt')" =~ ^[[:space:]]*/([A-Za-z0-9_:-]+)([[:space:]]|$) ]]; then
      classify "${BASH_REMATCH[1]}"
    fi
    ;;
  SessionStart)
    [[ -n "$session" ]] && rm -f "$marker" 2>/dev/null
    exit 0
    ;;
  *) exit 0 ;;
esac

[[ -n "$matched$spent" ]] || exit 0

out=""
if [[ -n "$matched" ]]; then
  text="This project runs design rounds through \`design-vault:design-round\`; invoke it before rendering a candidate."
  if [[ ! -d "${HOME-}/design-vault" ]]; then
    text+=' The design vault is not at ~/design-vault on this machine: for the brief'"'"'s Reference field, read the project'"'"'s derived export of the library where it has one, or write "none cited".'
  fi
  out="$(jq -nc --arg e "$event" --arg c "$text" \
    '{hookSpecificOutput: {hookEventName: $e, additionalContext: $c}}' 2>/dev/null)"
  [[ -n "$out" ]] || exit 0
fi

MARKER_MAX_AGE_MINUTES=1440 # guess, #5
if [[ -n "$session" ]]; then
  mkdir -p "$state_dir" 2>/dev/null
  set -o noclobber
  if ! { : >"$marker"; } 2>/dev/null; then
    [[ -e "$marker" ]] && exit 0
  fi
  set +o noclobber
  find "$state_dir" -maxdepth 1 -type f -mmin "+$MARKER_MAX_AGE_MINUTES" -delete 2>/dev/null
fi

[[ -n "$out" ]] && printf '%s\n' "$out"
exit 0

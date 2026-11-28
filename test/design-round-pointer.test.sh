#!/usr/bin/env bash

set -u
plugin="$(cd "$(dirname "$0")/.." && pwd)/plugin"
hook="$plugin/hooks/design-round-pointer.sh"
scratch="$(mktemp -d)"
trap 'rm -rf "$scratch"' EXIT
export TMPDIR="$scratch/tmp"
mkdir -p "$TMPDIR" "$scratch/home/design-vault" "$scratch/bare-home"

fails=0
pointer='design-vault:design-round'
absent='not at ~/design-vault'

skill() { jq -nc --arg s "$1" --arg id "$2" '{hook_event_name:"PreToolUse",tool_name:"Skill",tool_input:{skill:$s},session_id:$id}'; }
prompt() { jq -nc --arg p "$1" --arg id "$2" '{hook_event_name:"UserPromptSubmit",prompt:$p,session_id:$id}'; }

session_start() {
  local source="$1" id="$2" cmd
  while IFS= read -r cmd; do
    jq -nc --arg s "$source" --arg id "$id" '{hook_event_name:"SessionStart",source:$s,session_id:$id}' |
      CLAUDE_PLUGIN_ROOT="$plugin" bash -c "$cmd"
  done < <(jq -r --arg s "$source" '.hooks.SessionStart[]? | select((.matcher // "") | split("|") | index($s)) | .hooks[].command' "$plugin/hooks/hooks.json")
}

expect() {
  local name="$1" home="$2" payload="$3" want="$4" has="${5:-}" hasnt="${6:-}" out status
  if [[ "$home" == unset ]]; then
    out="$(printf '%s' "$payload" | env -u HOME bash "$hook")"
  else
    out="$(printf '%s' "$payload" | HOME="$home" bash "$hook")"
  fi
  status=$?
  local ok=1
  ((status == 0)) || ok=0
  if [[ "$want" == inject ]]; then
    [[ "$out" == *"$pointer"* ]] || ok=0
    [[ -z "$has" || "$out" == *"$has"* ]] || ok=0
    [[ -z "$hasnt" || "$out" != *"$hasnt"* ]] || ok=0
  else
    [[ -z "$out" ]] || ok=0
  fi
  if ((ok)); then
    echo "ok   $name"
  else
    echo "FAIL $name (exit $status): $out"
    fails=$((fails + 1))
  fi
}

home="$scratch/home"

expect "matched skill injects" "$home" "$(skill workflow-core:prototype s1)" inject '"hookEventName":"PreToolUse"' "$absent"
expect "unmatched skill is silent" "$home" "$(skill workflow-core:tdd s2)" silent
expect "second matched call in the session is silent" "$home" "$(skill animate s1)" silent

for name in design workflow-core:prototype animate workflow-core:design-mode; do
  expect "$name as a session's first skill injects" "$home" "$(skill "$name" "first-$name")" inject
done
expect "design-review is a critique, not a render" "$home" "$(skill design-review s3)" silent
expect "an impeccable skill injects" "$home" "$(skill impeccable:critique s4)" inject
expect "a non-Skill tool is silent" "$home" "$(jq -nc '{hook_event_name:"PreToolUse",tool_name:"Bash",tool_input:{command:"ls"},session_id:"s5"}')" silent

expect "absent vault adds the clause" "$scratch/bare-home" "$(skill design s6)" inject "$absent"
expect "an unset HOME still injects, under the hook's -u (workflow-core#1315)" unset "$(skill design s12)" inject "$absent"

expect "typed /design injects" "$home" "$(prompt '/design a sticker sheet' s7)" inject '"hookEventName":"UserPromptSubmit"'
expect "then its skill call is silent" "$home" "$(skill design s7)" silent
expect "a prompt that mentions /design mid-sentence is silent" "$home" "$(prompt 'what does /design do' s8)" silent
expect "typed /impeccable:polish injects" "$home" "$(prompt '/impeccable:polish' s9)" inject

expect "design-round loaded first is silent" "$home" "$(skill design-vault:design-round s10)" silent
expect "and spends the pointer" "$home" "$(skill prototype s10)" silent

expect "no session id still injects" "$home" "$(skill prototype '')" inject
expect "and injects again" "$home" "$(skill prototype '')" inject

expect "a session's pointer injects" "$home" "$(skill design s13)" inject
expect "and is silent again before a compaction" "$home" "$(skill design s13)" silent
compacted="$(session_start compact s13)"
if [[ -z "$compacted" ]]; then
  echo "ok   a compaction prints nothing"
else
  echo "FAIL a compaction prints nothing: $compacted"
  fails=$((fails + 1))
fi
expect "after a compaction it injects once more" "$home" "$(skill design s13)" inject
expect "and then is silent" "$home" "$(skill design s13)" silent
session_start resume s13 >/dev/null
expect "a resume does not re-arm it" "$home" "$(skill design s13)" silent
session_start compact other-session >/dev/null
expect "another session's compaction does not re-arm it" "$home" "$(skill design s13)" silent

ro="$scratch/ro-tmp"
mkdir -p "$ro/design-round-pointer-${UID:-0}"
chmod 555 "$ro/design-round-pointer-${UID:-0}"
TMPDIR="$ro" expect "an unwritable marker still injects" "$home" "$(skill prototype s11)" inject
TMPDIR="$ro" expect "and injects again" "$home" "$(skill prototype s11)" inject

((fails == 0)) && echo "all passed" || echo "$fails failed"
exit $((fails > 0))

#!/usr/bin/env bash
# Runs test/all.sh's suites side by side (#363): bash test/run-lanes.sh <suite command>…
# Each suite's output is held and printed whole once it ends, under `== <suite> (<s> s)`. Exits 1 naming each red's
# failing test files on stderr, one `FAIL <path>` line each, the shape workflow-core's lander reads (#436): those the
# suite wrote, one a line, to the file VAULT_FAILED_FILES names, else the one `.test.` file its command names. Any
# other red is printed `RED  <suite>`.
# A second or third suite starts only while the machine runs fewer than 3 suites, counted from `ps` (this run's
# own included), and MemAvailable clears that count's rung: core docs/environment.md §6's ceiling and ladder, the
# figures guard-suite-concurrency.sh holds. One suite may always run.
# The suites start longest first, by the seconds each last took green, kept one file a suite in the directory
# VAULT_SUITE_TIMES names; one with none kept starts ahead of them all, and ties keep the order given. So the last
# suite to end is a short one wherever a second lane opens (#457).
# VAULT_SUITE_LANES caps this run's own lanes (1 runs one at a time). VAULT_MEMINFO and VAULT_PS stand in for
# /proc/meminfo and ps in test/run-lanes.test.js.
# VAULT_SUITE_BUDGET, in seconds, refuses the run before any suite starts where the kept seconds, laid longest first
# on the lanes the machine would open now, end past it (#473). A suite with none kept counts as 0 s; lanes that open
# later than the start can still make a refused run fit.
# Once every suite has ended, red or green, each test file's own wall seconds go to workflow-core's run-cost report
# (#370), which names one new or changed against the base that took past its budget, after the suites' output and
# before any FAIL line. A suite that wrote `<path>\t<seconds>` lines to the file VAULT_FILE_SECONDS names, as
# test/failed-files.js does for node --test's many files, is timed by those alone; else the one `.test.` file its
# command names takes the suite's wall seconds, interpreter start included. The report never moves the exit status,
# and is not run where CI is set.

set -u
ceiling=3
max=${VAULT_SUITE_LANES:-$ceiling}
[[ $max =~ ^[1-9][0-9]*$ ]] || { echo "test/run-lanes.sh: VAULT_SUITE_LANES wants 1 or more — got '$max'" >&2 && exit 2; }
meminfo=${VAULT_MEMINFO:-/proc/meminfo}
ps_bin=${VAULT_PS:-ps}
# MemAvailable, in MB, wanted resting before the machine's 1st, 2nd and 3rd concurrent suite. The 1st is never read.
rungs=(0 2500 3400 4050)
# A runner's own line, never a wrapper's: a shell or `timeout` before it is its parent, which has its own line.
suite_line='^([^ ]*/)?(python3?( [^ ]+)* [^ ]*\.test\.py|node( [^ ]+)* --test|pytest|py\.test|python3? -m (pytest|unittest)|(node( [^ ]+)* )?[^ ]*[.]bin/vitest)( |$)'

others() { # the suites running on the machine that are not this run's
  local out pid args n=0
  out="$("$ps_bin" -eo pid=,args= 2>/dev/null)" || return 1
  while read -r pid args; do
    [[ ! $pid =~ ^[0-9]+$ || -n ${lane[$pid]:-} || $args =~ [.]bin/vitest\ list( |$) ]] && continue
    [[ $args =~ $suite_line ]] && n=$((n + 1))
  done <<<"$out"
  echo "$n"
}

available_mb() {
  local line
  line="$(grep -m1 '^MemAvailable:' "$meminfo" 2>/dev/null)" && [[ $line =~ ([0-9]+)\ kB ]] || return 1
  echo $((BASH_REMATCH[1] / 1024))
}

fits() { # fits <count>: whether the machine may run that many suites at once, by the ceiling and its memory rung
  local mb
  (($1 <= ceiling)) && mb="$(available_mb)" && ((mb >= rungs[$1]))
}

opens() { # whether one more suite may start now; where ps or the memory reading fails, no second one does
  local mine=${#lane[@]} n
  ((mine == 0)) && return 0
  ((mine < max)) && n="$(others)" || return 1
  fits $((n + mine + 1))
}

declare -A lane=() began=() log=()
logs="$(mktemp -d)"
reds=()
trap 'rm -rf "$logs"' EXIT
# Each suite runs in a process group of its own, so an interrupted run stops it with the checkers and browsers it
# started: in a script, a suite started with & would otherwise ignore SIGINT, and so would they.
set -m
stop() { # stop <exit status>
  local pid
  for pid in "${!lane[@]}"; do kill -TERM -- "-$pid" 2>/dev/null; done
  exit "$1"
}
trap 'stop 130' INT
trap 'stop 143' TERM

named_files() { # named_files <suite>: the test files its command line names, one a line
  local word
  # shellcheck disable=SC2086 # a suite is a command line, split into its words as it was run
  for word in $1; do [[ $word == *.test.* && -f $word ]] && printf '%s\n' "$word"; done
}

failing() { # failing <suite> <its VAULT_FAILED_FILES>
  local suite=$1 named=$2 files=()
  if [[ -s $named ]]; then
    mapfile -t files <"$named"
  else
    mapfile -t files < <(named_files "$suite")
  fi
  # A red run of several files that recorded none failed as a whole, and pins its fault on no one file.
  if ((${#files[@]} == 1)) || [[ -s $named ]]; then printf 'FAIL %s\n' "${files[@]}"; else printf 'RED  %s\n' "$suite"; fi
}

timings=${VAULT_SUITE_TIMES:-}
[[ -n $timings ]] && ! mkdir -p "$timings" 2>/dev/null && timings=''
timed() { # timed <suite>: the file its last green seconds are kept in
  local sum
  sum="$(printf '%s' "$1" | cksum)"
  echo "$timings/${sum%% *}"
}

kept_secs() { # kept_secs <suite> <default>: its last green seconds, else the default
  local secs=''
  read -r secs 2>/dev/null <"$(timed "$1")"
  [[ $secs =~ ^[0-9]+$ ]] && echo "$secs" || echo "$2"
}

finish() { # finish <pid> <status>
  local suite=${lane[$1]} micros took files=()
  micros=$((${EPOCHREALTIME/./} - ${began[$1]/./}))
  took=$(((micros + 500000) / 1000000))
  echo "== $suite ($took s)"
  if [[ -s ${log[$1]}.seconds ]]; then
    cat "${log[$1]}.seconds" >>"$logs/seconds"
  else
    mapfile -t files < <(named_files "$suite")
    ((${#files[@]} == 1)) && printf '%s\t%d.%06d\n' "${files[0]}" $((micros / 1000000)) $((micros % 1000000)) >>"$logs/seconds"
  fi
  cat "${log[$1]}"
  if (($2)); then
    mapfile -t -O "${#reds[@]}" reds < <(failing "$suite" "${log[$1]}.failed")
  elif [[ -n $timings ]]; then
    # Written aside and moved into place, so a neighbour run reading it never sees half a number.
    echo "$took" >"$timings/.took.$$" && mv -f "$timings/.took.$$" "$(timed "$suite")" 2>/dev/null
  fi
  unset "lane[$1]" "began[$1]" "log[$1]"
}

queue=("$@")
# A suite with no seconds kept sorts as this long, ahead of any real one.
untimed=999999999
if [[ -n $timings ]] && ((${#queue[@]} > 1)); then
  order=()
  for i in "${!queue[@]}"; do
    order+=("$(kept_secs "${queue[i]}" "$untimed")"$'\t'"$i")
  done
  sorted=()
  while IFS=$'\t' read -r _ i; do sorted+=("${queue[i]}"); done < <(printf '%s\n' "${order[@]}" | sort -t$'\t' -k1,1nr -k2,2n)
  queue=("${sorted[@]}")
fi
lanes_now() { # how many lanes opens() would grant at once, read before any suite of this run starts
  local n count=1
  n="$(others)" || { echo 1 && return; }
  while ((count < max)) && fits $((n + count + 1)); do count=$((count + 1)); done
  echo "$count"
}

budget=${VAULT_SUITE_BUDGET:-}
[[ -z $budget || $budget =~ ^[1-9][0-9]*$ ]] ||
  { echo "test/run-lanes.sh: VAULT_SUITE_BUDGET wants whole seconds, 1 or more — got '$budget'" >&2 && exit 2; }
if [[ -n $budget && -n $timings ]]; then
  open_lanes="$(lanes_now)"
  loads=() kept_total=0
  for ((i = 0; i < open_lanes; i++)); do loads+=(0); done
  for suite in "${queue[@]}"; do # in the order they start, each onto the lane that frees first
    secs="$(kept_secs "$suite" 0)"
    kept_total=$((kept_total + secs))
    least=0
    for i in "${!loads[@]}"; do ((loads[i] < loads[least])) && least=$i; done
    loads[least]=$((loads[least] + secs))
  done
  ends=0
  for load in "${loads[@]}"; do ((load > ends)) && ends=$load; done
  if ((ends > budget)); then
    if ((open_lanes == max && max < ceiling)); then
      remedy="VAULT_SUITE_LANES caps this run at $max lane(s); raise it, or run it again once"
    else
      remedy="Run it again once"
    fi
    echo "test/run-lanes.sh: refused before any suite ran: the ${#queue[@]} suites' kept green seconds sum to \
$kept_total s, which on the $open_lanes lane(s) the machine opens now end at about $ends s, past VAULT_SUITE_BUDGET's \
$budget s, the time a gate run has left under workflow-core's suite ceiling (workflow-core#2667). $remedy fewer \
suites run on the machine and more memory is free (#473)." >&2
    exit 1
  fi
fi
started=0
while ((${#queue[@]} || ${#lane[@]})); do
  if ((${#queue[@]})) && opens; then
    started=$((started + 1))
    # shellcheck disable=SC2086 # a suite is a command line, split into its words
    (VAULT_FAILED_FILES=$logs/$started.failed VAULT_FILE_SECONDS=$logs/$started.seconds exec ${queue[0]}) >"$logs/$started" 2>&1 </dev/null &
    log[$!]=$logs/$started
    lane[$!]=${queue[0]}
    began[$!]=$EPOCHREALTIME
    queue=("${queue[@]:1}")
    continue
  fi
  wait -n -p ended "${!lane[@]}"
  finish "$ended" $?
done
# Through the core's own module, which keeps the budget and the wording, called on this tree: its program entry reads
# its root as the main checkout of a worktree, so from a worktree it would judge the wrong tree's files.
if [[ -z ${CI:-} && -s $logs/seconds ]]; then
  # shellcheck disable=SC2016 # the ${…} are JavaScript's template literals
  if ! root="$(git rev-parse --show-toplevel 2>/dev/null)" || ! node -e '
const fs = require("node:fs");
const [vault, root, seconds] = process.argv.slice(1);
const core = require(`${vault}/scripts/lib/resolve-core.js`).resolveCore({ root: vault });
const report = require(`${core}/scripts/lib/run-cost-report.js`);
const timings = {};
for (const line of fs.readFileSync(seconds, "utf8").split("\n").filter(Boolean)) {
  const [file, secs] = line.split("\t");
  timings[file] = Number(secs);
}
for (const line of report.reportForRun(root, timings)) console.log(line);' \
    "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)" "$root" "$logs/seconds"; then
    echo "test/run-lanes.sh: workflow-core's run-cost report would not run, so no test file's cost is judged; the suites' verdict stands (#370)."
  fi
fi
if ((${#reds[@]})); then
  printf '%s\n' "${reds[@]}" >&2
  exit 1
fi

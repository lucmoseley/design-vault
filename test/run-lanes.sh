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

set -u
ceiling=3
max=${VAULT_SUITE_LANES:-$ceiling}
[[ $max =~ ^[1-9][0-9]*$ ]] || { echo "test/run-lanes.sh: VAULT_SUITE_LANES wants 1 or more — got '$max'" >&2 && exit 2; }
meminfo=${VAULT_MEMINFO:-/proc/meminfo}
ps_bin=${VAULT_PS:-ps}
# MemAvailable, in MB, wanted resting before the machine's 1st, 2nd and 3rd concurrent suite. The 1st is never read,
# since one suite may always run.
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

opens() { # whether one more suite may start now; where ps or the memory reading fails, no second one does
  local mine=${#lane[@]} n mb
  ((mine == 0)) && return 0
  ((mine < max)) && n="$(others)" || return 1
  n=$((n + mine + 1))
  ((n <= ceiling)) && mb="$(available_mb)" && ((mb >= rungs[n]))
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

failing() { # failing <suite> <its VAULT_FAILED_FILES>
  local suite=$1 named=$2 word files=()
  if [[ -s $named ]]; then
    mapfile -t files <"$named"
  else
    # shellcheck disable=SC2086 # a suite is a command line, split into its words as it was run
    for word in $suite; do [[ $word == *.test.* && -f $word ]] && files+=("$word"); done
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

finish() { # finish <pid> <status>
  local suite=${lane[$1]} took
  took=$(((${EPOCHREALTIME/./} - ${began[$1]/./} + 500000) / 1000000))
  echo "== $suite ($took s)"
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
    secs=''
    read -r secs 2>/dev/null <"$(timed "${queue[i]}")"
    [[ $secs =~ ^[0-9]+$ ]] || secs=$untimed
    order+=("$secs"$'\t'"$i")
  done
  sorted=()
  while IFS=$'\t' read -r _ i; do sorted+=("${queue[i]}"); done < <(printf '%s\n' "${order[@]}" | sort -t$'\t' -k1,1nr -k2,2n)
  queue=("${sorted[@]}")
fi
started=0
while ((${#queue[@]} || ${#lane[@]})); do
  if ((${#queue[@]})) && opens; then
    started=$((started + 1))
    # shellcheck disable=SC2086 # a suite is a command line, split into its words
    (VAULT_FAILED_FILES=$logs/$started.failed exec ${queue[0]}) >"$logs/$started" 2>&1 </dev/null &
    log[$!]=$logs/$started
    lane[$!]=${queue[0]}
    began[$!]=$EPOCHREALTIME
    queue=("${queue[@]:1}")
    continue
  fi
  wait -n -p ended "${!lane[@]}"
  finish "$ended" $?
done
if ((${#reds[@]})); then
  printf '%s\n' "${reds[@]}" >&2
  exit 1
fi

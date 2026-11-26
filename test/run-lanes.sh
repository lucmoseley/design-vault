#!/usr/bin/env bash
# Usage: bash test/run-lanes.sh <suite command>…
# Each suite's output prints whole once it ends, under `== <suite> (<s> s)`. Exits 0 when every suite passes, 1 when
# any is red or the run is refused, 2 on a malformed setting. Each red prints on stderr one `FAIL <path>` line per
# failing test file (those the suite wrote to the file VAULT_FAILED_FILES names, else the one `.test.` file its
# command names), or `RED  <suite>`.
# VAULT_SUITE_LANES caps the run's lanes (1 runs one suite at a time). VAULT_LANE_WAIT_S is how long a first suite
# waits for the machine to free up before the run is refused (600 by default). VAULT_SUITE_TIMES names the directory
# each suite's last green seconds are kept in; VAULT_SUITE_BUDGET, in seconds, refuses the run before any suite starts
# where those seconds, laid longest first on the lanes open now, end past it. WFC_GATE_SEAT names workflow-core's gate
# seat marker. VAULT_MEMINFO, VAULT_PS and VAULT_CGROUP stand in for /proc/meminfo, ps and the run's cgroup directory.

set -u
ceiling=3
max=${VAULT_SUITE_LANES:-$ceiling}
[[ $max =~ ^[1-9][0-9]*$ ]] || { echo "test/run-lanes.sh: VAULT_SUITE_LANES wants 1 or more — got '$max'" >&2 && exit 2; }
meminfo=${VAULT_MEMINFO:-/proc/meminfo}
ps_bin=${VAULT_PS:-ps}
# guess, #363
rungs=(0 2500 3400 4050)
# guess #434
wait_s=${VAULT_LANE_WAIT_S:-600}
[[ $wait_s =~ ^[0-9]+$ ]] || { echo "test/run-lanes.sh: VAULT_LANE_WAIT_S wants whole seconds — got '$wait_s'" >&2 && exit 2; }
suite_line='^([^ ]*/)?(python3?( [^ ]+)* [^ ]*\.test\.py|node( [^ ]+)* --test|pytest|py\.test|python3? -m (pytest|unittest)|(node( [^ ]+)* )?[^ ]*[.]bin/vitest)( |$)'

others() {
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

fits() {
  local mb
  (($1 <= ceiling)) && mb="$(available_mb)" && ((mb >= rungs[$1]))
}

step() {
  echo $((rungs[$1 + 1] - rungs[$1]))
}

ppid_from() {
  # comm may hold spaces and parentheses: https://man7.org/linux/man-pages/man5/proc_pid_stat.5.html
  read -r _ REPLY _ <<<"${1##*) }"
}

ancestor() {
  local p=$$ stat
  while ((p > 1)); do
    ((p == $1)) && return 0
    read -r stat 2>/dev/null <"/proc/$p/stat" || return 1
    ppid_from "$stat"
    p=$REPLY
  done
  return 1
}

seat_mb=''
if [[ -n ${WFC_GATE_SEAT:-} ]]; then
  for _ in 1 2 3 4 5; do
    seat="$(node -e 'const r = JSON.parse(require("node:fs").readFileSync(process.argv[1], "utf8"));
      if (!(Number.isInteger(r.pid) && r.pid > 1 && Number.isFinite(r.chargeMb) && r.chargeMb > 0)) process.exit(1);
      console.log(r.pid, Math.floor(r.chargeMb));' "$WFC_GATE_SEAT" 2>/dev/null)" && break
    # guess #434
    sleep 0.2
  done
  [[ -n ${seat:-} ]] && read -r seat_pid seat_charge <<<"$seat" && ancestor "$seat_pid" && seat_mb=$seat_charge
fi

lanes_draw() {
  local f stat pid p kb key val charged=0 short=0 mb
  local -A parent=() pss=()
  for f in /proc/[0-9]*/stat; do
    read -r stat 2>/dev/null <"$f" || continue
    pid=${f#/proc/} pid=${pid%/stat}
    ppid_from "$stat"
    parent[$pid]=$REPLY
  done
  for pid in "${!parent[@]}"; do
    p=$pid
    while ((p > 1)) && [[ -z ${lane[$p]:-} ]]; do p=${parent[$p]:-0}; done
    [[ -n ${lane[$p]:-} ]] || continue
    kb=0
    while read -r key val _; do [[ $key == Pss: ]] && kb=$((kb + val)); done 2>/dev/null <"/proc/$pid/smaps_rollup"
    pss[$p]=$((${pss[$p]:-0} + kb))
  done
  for pid in "${!lane[@]}"; do
    mb=$((${pss[$pid]:-0} / 1024))
    if ((mb >= floor[$pid])); then
      charged=$((charged + mb))
    else
      charged=$((charged + floor[$pid])) short=$((short + floor[$pid] - mb))
    fi
  done
  echo "$charged $short"
}

scope_room_mb() {
  local dir=${VAULT_CGROUP:-} line max current key val inactive=''
  if [[ -z $dir ]]; then
    line="$(grep -m1 '^0::' /proc/self/cgroup 2>/dev/null)" || return 1
    dir=/sys/fs/cgroup${line#0::}
  fi
  read -r max 2>/dev/null <"$dir/memory.max" && read -r current 2>/dev/null <"$dir/memory.current" || return 1
  while read -r key val; do [[ $key == inactive_file ]] && inactive=$val; done 2>/dev/null <"$dir/memory.stat"
  [[ $max =~ ^[0-9]+$ && $current =~ ^[0-9]+$ && $inactive =~ ^[0-9]+$ ]] || return 1
  echo $(((max - current + inactive) / 1048576))
}

opens() {
  local mine=${#lane[@]} n mb room need charged short
  ((mine < max && mine < ceiling)) || return 1
  if ((mine)); then
    need="$(step "$mine")"
    read -r charged short < <(lanes_draw)
    room="$(scope_room_mb)" && ((room - short < need)) && return 1
    [[ -n $seat_mb ]] && {
      ((charged + need <= seat_mb))
      return
    }
  elif [[ -n $seat_mb ]]; then
    return 0
  fi
  if ! n="$(others)" || ! mb="$(available_mb)"; then ((mine == 0)) && return 0 || return 1; fi
  ((n + mine + 1 <= ceiling && mb >= rungs[n + mine + 1]))
}

declare -A lane=() began=() log=() floor=()
logs="$(mktemp -d)"
reds=()
trap 'rm -rf "$logs"' EXIT
# Without job control, an asynchronous command ignores SIGINT: https://www.gnu.org/software/bash/manual/html_node/Signals.html
set -m
stop() {
  local pid
  for pid in "${!lane[@]}"; do kill -TERM -- "-$pid" 2>/dev/null; done
  exit "$1"
}
trap 'stop 130' INT
trap 'stop 143' TERM

named_files() {
  local word words
  read -ra words <<<"$1"
  for word in "${words[@]}"; do [[ $word == *.test.* && -f $word ]] && printf '%s\n' "$word"; done
}

failing() {
  local suite=$1 named=$2 files=()
  if [[ -s $named ]]; then
    mapfile -t files <"$named"
  else
    mapfile -t files < <(named_files "$suite")
  fi
  if ((${#files[@]} == 1)) || [[ -s $named ]]; then printf 'FAIL %s\n' "${files[@]}"; else printf 'RED  %s\n' "$suite"; fi
}

timings=${VAULT_SUITE_TIMES:-}
[[ -n $timings ]] && ! mkdir -p "$timings" 2>/dev/null && timings=''
timed() {
  local sum
  sum="$(printf '%s' "$1" | cksum)"
  echo "$timings/${sum%% *}"
}

kept_secs() {
  local secs=''
  read -r secs 2>/dev/null <"$(timed "$1")"
  [[ $secs =~ ^[0-9]+$ ]] && echo "$secs" || echo "$2"
}

finish() {
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
    echo "$took" >"$timings/.took.$$" && mv -f "$timings/.took.$$" "$(timed "$suite")" 2>/dev/null
  fi
  unset "lane[$1]" "began[$1]" "log[$1]" "floor[$1]"
}

queue=("$@")
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
lanes_now() {
  local n='' count=1 room need=0
  [[ -n $seat_mb ]] || n="$(others)" || { echo 1 && return; }
  room="$(scope_room_mb)" || room=''
  while ((count < max && count < ceiling)); do
    need=$((need + $(step "$count")))
    [[ -z $room ]] || ((room >= need)) || break
    if [[ -n $seat_mb ]]; then ((need <= seat_mb)) || break; else fits $((n + count + 1)) || break; fi
    count=$((count + 1))
  done
  echo "$count"
}

budget=${VAULT_SUITE_BUDGET:-}
[[ -z $budget || $budget =~ ^[1-9][0-9]*$ ]] ||
  { echo "test/run-lanes.sh: VAULT_SUITE_BUDGET wants whole seconds, 1 or more — got '$budget'" >&2 && exit 2; }
if [[ -n $budget && -n $timings ]]; then
  open_lanes="$(lanes_now)"
  loads=() kept_total=0
  for ((i = 0; i < open_lanes; i++)); do loads+=(0); done
  for suite in "${queue[@]}"; do
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
wait_began=''
while ((${#queue[@]} || ${#lane[@]})); do
  if ((${#queue[@]})) && opens; then
    wait_began=''
    started=$((started + 1))
    read -ra words <<<"${queue[0]}"
    (VAULT_FAILED_FILES=$logs/$started.failed VAULT_FILE_SECONDS=$logs/$started.seconds exec "${words[@]}") >"$logs/$started" 2>&1 </dev/null &
    log[$!]=$logs/$started
    floor[$!]=0
    ((${#lane[@]})) && floor[$!]="$(step ${#lane[@]})"
    lane[$!]=${queue[0]}
    began[$!]=$EPOCHREALTIME
    queue=("${queue[@]:1}")
    continue
  fi
  if ((!${#lane[@]})); then
    if [[ -z $wait_began ]]; then
      wait_began=$SECONDS
      echo "test/run-lanes.sh: waiting up to $wait_s s for the machine to run fewer suites or free more memory (#434)."
    elif ((SECONDS - wait_began >= wait_s)); then
      echo "test/run-lanes.sh: refused: after $wait_s s the machine still runs too many suites, or has too little \
memory available, for one more (core docs/environment.md §6). Run it again once it frees (#434)." >&2
      exit 1
    fi
    # guess #434
    sleep 1
    continue
  fi
  wait -n -p ended "${!lane[@]}"
  finish "$ended" $?
done
# #370
if [[ -z ${CI:-} && -s $logs/seconds ]]; then
  root="$(git rev-parse --show-toplevel 2>/dev/null)" || root=$PWD
  node "$(dirname "${BASH_SOURCE[0]}")/run-cost.js" "$root" "$logs/seconds" 2>/dev/null ||
    echo "test/run-lanes.sh: workflow-core's run-cost report would not run; the suites' verdict stands (#370)."
fi
if ((${#reds[@]})); then
  printf '%s\n' "${reds[@]}" >&2
  exit 1
fi

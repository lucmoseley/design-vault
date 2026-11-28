# shellcheck shell=bash
# #629
meminfo=${VAULT_MEMINFO:-/proc/meminfo}
ps_bin=${VAULT_PS:-ps}

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

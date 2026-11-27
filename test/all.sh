#!/usr/bin/env bash
# Usage:
#   bash test/all.sh                          every suite; inside a commit, only the suites its staged files can break
#   VAULT_ALL_SUITES=1 bash test/all.sh       every suite, inside a commit too
#   bash test/all.sh [--plan] <test file>…    only those files: a .test.js one under node --test, any other by its suite
#   bash test/all.sh [--plan] --shard=k/n     every nth suite of the list, from the kth on
#   --plan prints what would run and runs nothing. A red prints `FAIL <path>` per failing file.
#   A missing tool fails the run naming its install step.

set -u
# #491
vault="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)" || exit 1
cd "$vault" || exit 1
# code-edges loads: failed-files.js
registry='node --test --test-reporter=./test/failed-files.js	npm
bash test/design-round-pointer.test.sh
python3 test/cutout.test.py	images
python3 test/check-render.test.py	images
python3 test/check-logo.test.py	images chromium
python3 test/check-clip.test.py
python3 test/check-flow.test.py	chromium npm
python3 test/runner.test.py	chromium
python3 test/planted-faults-runner.test.py
python3 test/check-flow-records.test.py	images chromium
python3 test/check-frames.test.py	chromium
python3 test/check-overlay.test.py	images chromium
python3 test/check-measure.test.py	chromium
python3 test/face-profile.test.py	images chromium
python3 test/contact-sheet.test.py	images chromium
python3 test/check-layout.test.py	chromium
python3 test/check-access.test.py	images chromium
python3 test/check-access-contrast.test.py	images chromium
python3 test/check-access-pointer.test.py	images chromium
python3 test/palette.test.py
python3 test/colour-space.test.py	images
python3 test/rule-table.test.py
python3 test/answers-file.test.py
python3 test/siblings.test.py
python3 test/crash-exit.test.py	images
python3 test/child.test.py	chromium
python3 test/probe.test.py	chromium
python3 test/parts-map.test.py	images chromium
python3 test/look.test.py	images chromium
python3 test/check-load.test.py	chromium
python3 test/check-load-files.test.py	chromium
python3 test/drive-overlay.test.py	chromium openssl
python3 test/conditions.test.py	chromium
python3 test/look-renders.test.py	images chromium npm
python3 test/check-seams.test.py	images chromium npm
python3 test/drive-form.test.py	chromium
python3 test/check-cross.test.py	chromium
python3 test/check-dom.test.py	images chromium
python3 test/check-markup.test.py	chromium
python3 test/check-style.test.py	images chromium
python3 test/check-state.test.py	images chromium
python3 test/check-text.test.py	chromium
python3 test/drive-pointer.test.py	chromium
python3 test/video-sheet.test.py	images video'
suites=()
declare -A needs=()
while IFS=$'\t' read -r suite need; do
  for word in ${need:-}; do
    [[ $word == images || $word == chromium || $word == openssl || $word == video || $word == npm ]] || { echo "test/all.sh: $suite needs '$word', which is none of images, chromium, openssl, video and npm" >&2 && exit 2; }
  done
  suites+=("$suite")
  needs[$suite]=${need:-}
  [[ $suite == 'node '* ]] && node_suite=$suite
done <<<"$registry"
plan_only=0
shard=''
while [[ ${1:-} == --plan || ${1:-} == --shard=* ]]; do
  if [[ $1 == --plan ]]; then
    plan_only=1
  else
    shard=${1#--shard=}
    if ! [[ $shard =~ ^([1-9][0-9]*)/([1-9][0-9]*)$ ]] || ((BASH_REMATCH[1] > BASH_REMATCH[2])); then
      echo "test/all.sh: --shard wants k/n with 1 <= k <= n — got '$shard'" >&2 && exit 2
    fi
  fi
  shift
done
[[ -n $shard ]] && (($#)) && { echo "test/all.sh: --shard takes no test files" >&2 && exit 2; }
named=()
node_files=()
for file in "$@"; do
  file=${file#./}
  suite=''
  if [[ $file == *.test.js ]]; then
    [[ -f $file ]] || { echo "test/all.sh: no $file — name a test file on disk" >&2 && exit 2; }
    [[ " ${node_files[*]} " == *" $file "* ]] || node_files+=("$file")
    continue
  fi
  for listed in "${suites[@]}"; do [[ ${listed##* } == "$file" ]] && suite=$listed; done
  if [[ -z $suite ]]; then
    [[ -f $file ]] || { echo "test/all.sh: no $file — name a .test.js file or a suite file this list runs" >&2 && exit 2; }
    echo "SKIP $file — no suite lists it"
    continue
  fi
  [[ " ${named[*]} " == *" $suite "* ]] || named+=("$suite")
done
if ((${#node_files[@]})); then
  named=("$node_suite ${node_files[*]}" "${named[@]}")
  needs["$node_suite ${node_files[*]}"]=${needs[$node_suite]}
fi
if (($#)) && ((!${#named[@]})); then
  echo "no named file has a suite to run"
  exit 0
fi
in_commit=0
if ((!$#)) && [[ (-n ${GIT_INDEX_FILE:-} || -n ${WFC_GATE_SEAT:-}) && -z ${VAULT_ALL_SUITES:-} ]] &&
  staged="$(git diff --cached --name-only --no-renames)"; then
  in_commit=1
fi
copies="$(mktemp -d)"
trap 'rm -rf "$copies"' EXIT
sides=()
if ((in_commit)); then
  if [[ -v WFC_MERGE_PARENTS ]]; then
    parents=$WFC_MERGE_PARENTS
    [[ $parents == 'unread: '* ]] && echo "merge parents unread, so judged against HEAD alone: ${parents#unread: }" && parents=''
  else
    parents="$(cat "$(git rev-parse --path-format=absolute --git-path MERGE_HEAD)" 2>/dev/null)"
    [[ -n $parents ]] || parents="$(compgen -e | sed -n 's/^GITHEAD_//p')"
  fi
  printf '%s\n' "$staged" >"$copies/HEAD.paths"
  git diff --cached --name-only --no-renames --diff-filter=D >"$copies/HEAD.gone"
  git show HEAD:test/all.sh >"$copies/HEAD.head" 2>/dev/null || rm -f "$copies/HEAD.head"
  sides=(HEAD)
  for parent in $parents; do
    side="$copies/$parent"
    if [[ $parent =~ ^[0-9a-f]{40}([0-9a-f]{24})?$ ]] && git diff --cached --name-only --no-renames "$parent" >"$side.paths" 2>/dev/null &&
      git diff --cached --name-only --no-renames --diff-filter=D "$parent" >"$side.gone" 2>/dev/null; then
      git show "$parent:test/all.sh" >"$side.head" 2>/dev/null || rm -f "$side.head"
      sides+=("$parent")
    else
      echo "merge parent $parent will not read, so the commit is not judged against it"
    fi
  done
  git show :test/all.sh >"$copies/staged" 2>/dev/null || rm -f "$copies/staged"
fi
[[ -n ${VAULT_SUITE_TIMES:-} ]] || ! common="$(git rev-parse --path-format=absolute --git-common-dir 2>/dev/null)" ||
  export VAULT_SUITE_TIMES="$common/vault-suite-times"
mapfile -t local_env < <(git rev-parse --local-env-vars)
unset "${local_env[@]}"

run=("${suites[@]}")
(($#)) && run=("${named[@]}")
if ((in_commit)); then
  if plan="$(VAULT_SIDES_DIR="$copies" VAULT_SIDES="${sides[*]}" VAULT_RUNNER_STAGED="$copies/staged" \
    node "$vault/test/select-suites.js" --select "${suites[@]}")" && [[ -n $plan ]]; then
    selected=()
    everything=0
    while IFS=$'\t' read -r verdict suite why; do
      case $verdict in
        all) echo "all suites: $suite" && everything=1 ;;
        run) selected+=("$suite") ;;
        skip) echo "SKIP $suite — $why" ;;
      esac
    done <<<"$plan"
    ((everything)) || run=("${selected[@]}")
  else
    echo "all suites: test/select-suites.js could not choose"
  fi
fi
if [[ -n $shard ]]; then
  shard_suites=() k=${shard%/*} n=${shard#*/}
  for i in "${!run[@]}"; do ((i % n == k - 1)) && shard_suites+=("${run[i]}"); done
  run=("${shard_suites[@]}")
  ((${#run[@]})) || { echo "shard $shard holds no suite" && exit 0; }
fi
if ((plan_only)); then
  printf 'RUN %s\n' "${run[@]}"
  exit 0
fi

missing=0
need() {
  local what="$1" install="$2"
  shift 2
  if ! "$@" >/dev/null 2>&1; then
    echo "MISSING $what — install: $install" >&2
    missing=$((missing + 1))
  fi
}

need node 'Node, from nodejs.org or nvm' command -v node
need jq 'sudo apt install jq' command -v jq
suites_needing() {
  local suite list=()
  for suite in "${run[@]}"; do
    [[ " ${needs[$suite]:-} " == *" $1 "* ]] && list+=("${suite#python3 }")
  done
  ((${#list[@]})) || return 1
  local out=${list[0]} i
  for ((i = 1; i < ${#list[@]}; i++)); do
    if ((i == ${#list[@]} - 1)); then out+=" and ${list[i]}"; else out+=", ${list[i]}"; fi
  done
  printf '%s' "$out"
}
if [ -f plugin/package.json ] && for_npm="$(suites_needing npm)"; then
  need "the plugin's npm package parse5, for $for_npm" 'npm ci --ignore-scripts --prefix plugin' \
    node -e 'require("./plugin/node_modules/parse5")'
fi
if [[ " ${run[*]} " == *" python3 "* ]]; then
  pip_install='python3 -m pip install --only-binary :all: -r plugin/requirements.txt'
  need python3 'Python 3, from miniforge (the machine-wide Python)' command -v python3
  if for_images="$(suites_needing images)"; then
    for module in numpy PIL scipy; do
      need "the Python package $module, for $for_images" "$pip_install" \
        python3 -c "import $module"
    done
  fi
  if for_video="$(suites_needing video)"; then
    need "the Python package av, for $for_video" "$pip_install" \
      python3 -c "import av"
  fi
  if for_chromium="$(suites_needing chromium)"; then
    need "the Python package playwright, for $for_chromium" \
      "$pip_install && python3 -m playwright install chromium" \
      python3 -c 'import playwright.sync_api'
    python3 -c 'import playwright.sync_api' 2>/dev/null &&
      need "Playwright's Chromium, for $for_chromium" \
        'python3 -m playwright install chromium' \
        python3 -c 'from playwright.sync_api import sync_playwright
with sync_playwright() as p: p.chromium.launch().close()'
  fi
  if for_openssl="$(suites_needing openssl)"; then
    need "the openssl command, for $for_openssl" 'sudo apt install openssl' command -v openssl
  fi
fi
if ((missing)); then
  echo "test/all.sh: $missing missing — no suite was run." >&2
  exit 1
fi

if [[ (-n ${WFC_GATE_SEAT:-} || in_commit -eq 1) && -z ${VAULT_SUITE_BUDGET:-} ]]; then
  if ceiling_ms="$(node -e 'const core = require(process.argv[1]).resolveCore();
process.stdout.write(String(require(`${core}/scripts/lib/suite-ceiling.js`).ceilingMs()))' "$vault/scripts/lib/resolve-core.js")" &&
    [[ $ceiling_ms =~ ^[0-9]+$ ]] && ((ceiling_ms / 1000 > SECONDS)); then
    export VAULT_SUITE_BUDGET=$((ceiling_ms / 1000 - SECONDS))
  else
    echo "the suite ceiling will not read from workflow-core or is already spent, so this run is not judged against it before it starts"
  fi
fi
bash "$vault/test/run-lanes.sh" "${run[@]}" || exit 1
if (($#)); then echo "${#run[@]} named suite(s) passed"; elif [[ -n $shard ]]; then echo "${#run[@]} suites of shard $shard passed"; else echo "${#run[@]} of ${#suites[@]} suites passed"; fi

#!/usr/bin/env bash
set -euo pipefail
umask 077

mode="${1:---due}"
case "$mode" in
  --due|--now|--dry-run) ;;
  *) echo "Usage: bash $0 [--due|--now|--dry-run]" >&2; exit 2 ;;
esac

state="${SYNERGY_PUBLICATION_STATE_DIR:-${XDG_STATE_HOME:-$HOME/.local/state}/synergy-publications}"
remote="${SYNERGY_PUBLICATION_REMOTE:-git@github.com:gt-synergy-lab/gt-synergy-lab.github.io.git}"
codex_bin="${SYNERGY_CODEX_BIN:-codex}"
mkdir -p "$state"
state="$(cd "$state" && pwd)"
exec 9>"$state/update.lock"
flock -n 9 || exit 0

now="$(date +%s)"
last_success=0
last_attempt=0
if [[ -f "$state/last-success" ]]; then read -r last_success < "$state/last-success"; fi
if [[ -f "$state/last-attempt" ]]; then read -r last_attempt < "$state/last-attempt"; fi
if [[ "$mode" == --due ]]; then
  if (( now - last_success < 30 * 24 * 60 * 60 || now - last_attempt < 24 * 60 * 60 )); then
    exit 0
  fi
fi

if [[ "$mode" != --dry-run ]]; then
  printf '%s\n' "$now" > "$state/last-attempt"
fi
printf '\n[%s] Starting Publications and Research News update (%s)\n' "$(date -Is)" "$mode"
"$codex_bin" login status

checkout="$(mktemp -d)"
trap 'rm -rf -- "$checkout"' EXIT
export GIT_TERMINAL_PROMPT=0
export GIT_SSH_COMMAND="${GIT_SSH_COMMAND:-ssh -o BatchMode=yes -o ConnectTimeout=15}"
git clone --quiet --depth 1 --branch main -- "$remote" "$checkout"
cd "$checkout"

python3 -B scripts/refresh_publications.py --best-effort
"$codex_bin" exec --sandbox workspace-write -c 'approval_policy="never"' \
  -c 'web_search="live"' - < scripts/monthly_publications.md 9>&-
python3 -B scripts/prepare_publication_update.py --cache-key "publication-refresh-$now-$$"
node --test tests/publication-metadata.test.js
python3 -B -m unittest discover -s tests

git add -- index.html pages/news.html pages/publication.html assets/js/publications.js assets/scripts/pub_list
git diff --cached --check
if [[ "$mode" == --dry-run ]]; then
  git diff --cached --stat
  exit 0
fi

if ! git diff --cached --quiet; then
  git -c user.name='Synergy Lab Publications' -c user.email='synergy-publications@users.noreply.github.com' \
    commit -m "Refresh Publications and Research News"
  git push origin HEAD:refs/heads/main
  printf 'Pushed %s; GitHub Pages will deploy from main.\n' "$(git rev-parse --short HEAD)"
else
  echo 'No verified publication or news changes.'
fi
printf '%s\n' "$(date +%s)" > "$state/last-success.tmp"
mv "$state/last-success.tmp" "$state/last-success"

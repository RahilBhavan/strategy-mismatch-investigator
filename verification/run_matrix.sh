#!/usr/bin/env bash
# Run the browser checks in Chromium and WebKit inside Microsoft's Playwright Ubuntu image.
# Each check starts its own app server and throwaway database. Needs podman.
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
image=mcr.microsoft.com/playwright/python:v1.64.1-noble
for engine in ${ENGINES:-chromium webkit}; do
  for check in ${CHECKS:-browser_check keyboard_check layout_checks contrast_audit assistive_check}; do
    echo "== $engine $check"
    podman run --rm --network host -e ENGINE="$engine" -e PYTHONDONTWRITEBYTECODE=1 \
      -v "$root":/w:Z -w /w "$image" \
      bash -c "pip install -q --disable-pip-version-check playwright==1.64.1 >/dev/null 2>&1; python verification/$check.py" | tail -3
  done
done

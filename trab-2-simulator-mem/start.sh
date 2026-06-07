#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

[ -d .venv ] || python3 -m venv .venv
source .venv/bin/activate
python -m pip install --quiet --upgrade pip
python -m pip install --quiet notebook matplotlib
jupyter notebook "$@"

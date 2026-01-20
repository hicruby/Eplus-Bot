#!/usr/bin/env bash
set -e
python -m playwright install >/dev/null 2>&1 || true
python -u playwright_py/src/play_eplus_bot.py --config config/config.yaml --selectors config/selectors.json

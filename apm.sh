#!/bin/bash
# APM Runner for Linux/macOS

set -e

APM_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/apm"
VENV_PYTHON="$APM_DIR/venv/bin/python3"
TMP_FILE="/tmp/apm_goto.tmp"

if [ -x "$VENV_PYTHON" ]; then
    RUNNER_PYTHON="$VENV_PYTHON"
else
    RUNNER_PYTHON="python3"
fi

"$RUNNER_PYTHON" "$APM_DIR/apm.py" "$@"

if [ -f "$TMP_FILE" ]; then
    APM_GOTO_PATH="$(cat "$TMP_FILE")"
    rm -f "$TMP_FILE"
    if [ -n "$APM_GOTO_PATH" ]; then
        cd "$APM_GOTO_PATH" || true
    fi
fi

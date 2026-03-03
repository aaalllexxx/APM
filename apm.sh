#!/bin/bash
# APM Runner for Linux/macOS
python3 ~/.config/apm/apm.py "$@"
if [ -f "/tmp/apm_goto.tmp" ]; then
    cd "$(cat /tmp/apm_goto.tmp)" || true
    rm -f /tmp/apm_goto.tmp
fi

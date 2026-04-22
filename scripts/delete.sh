#!/bin/bash
# APM Uninstaller for Linux/macOS

set -e

APM_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/apm"
BIN_DIR="$HOME/.local/bin"
TARGET_LINK="$BIN_DIR/apm"

echo "[+] Uninstalling APM..."

if [ -d "$APM_DIR" ]; then
    rm -rf "$APM_DIR"
    echo "[+] Removed $APM_DIR"
else
    echo "[*] $APM_DIR was not found"
fi

if [ -L "$TARGET_LINK" ] || [ -f "$TARGET_LINK" ]; then
    rm -f "$TARGET_LINK"
    echo "[+] Removed $TARGET_LINK"
else
    echo "[*] $TARGET_LINK was not found"
fi

echo "[+] APM uninstalled successfully!"

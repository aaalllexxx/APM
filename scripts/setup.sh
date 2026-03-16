#!/bin/bash
# AEngine Unified Installer for Linux/macOS
# This script sets up APM, Security module, and all project dependencies.

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APM_DIR="$HOME/.config/apm"

echo "=========================================="
echo "    AEngine Zero-Configuration Setup"
echo "=========================================="

# Create config directory if not exists
mkdir -p "$APM_DIR"

# Install Python dependencies in a local venv
echo "[+] Creating virtual environment in $APM_DIR/venv..."
python3 -m venv "$APM_DIR/venv" || { echo "[-] Failed to create venv"; exit 1; }

echo "[+] Updating pip..."
"$APM_DIR/venv/bin/python3" -m pip install --upgrade pip

echo "[+] Installing project dependencies..."
if [ -f "$PROJECT_ROOT/requirements.txt" ]; then
    "$APM_DIR/venv/bin/python3" -m pip install -r "$PROJECT_ROOT/requirements.txt" || {
        echo "[!] Pip failed, attempting with --break-system-packages..."
        "$APM_DIR/venv/bin/python3" -m pip install -r "$PROJECT_ROOT/requirements.txt" --break-system-packages
    }
else
    echo "[!] requirements.txt not found in $PROJECT_ROOT"
fi

# Copy APM files to global config
echo "[+] Synchronizing APM modules..."
mkdir -p "$APM_DIR/modules"
mkdir -p "$APM_DIR/scripts"
mkdir -p "$APM_DIR/sources"

# Copy core APM files
cp -r "$PROJECT_ROOT/APM/"* "$APM_DIR/"

# Ensure runner is executable
chmod +x "$APM_DIR/apm.sh"

# Create symlink in /usr/local/bin
echo "[+] Registering 'apm' command..."
if [ -w /usr/local/bin ]; then
    ln -sf "$APM_DIR/apm.sh" /usr/local/bin/apm
else
    echo "[*] Requesting sudo for symlink creation..."
    sudo ln -sf "$APM_DIR/apm.sh" /usr/local/bin/apm
fi

echo ""
echo "[+] Setup complete! AEngine is ready to use."
echo "[+] Use 'apm' to manage your projects."
echo "=========================================="

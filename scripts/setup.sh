#!/bin/bash
# APM Installer for Linux/macOS

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APM_DIR="$HOME/.config/apm"

echo "[+] Installing APM..."

# Install Python dependencies
echo "[+] Installing Python dependencies..."
cd "$SCRIPT_DIR/.."
pip3 install -r requirements.txt --user

# Create config directory
echo "[+] Creating config directory..."
mkdir -p "$APM_DIR"

# Copy files
echo "[+] Copying files..."
cp -r "$SCRIPT_DIR/../"* "$APM_DIR/"

# Make runner executable
chmod +x "$APM_DIR/apm.sh"

# Create symlink in /usr/local/bin
echo "[+] Creating symlink..."
if [ -w /usr/local/bin ]; then
    ln -sf "$APM_DIR/apm.sh" /usr/local/bin/apm
else
    sudo ln -sf "$APM_DIR/apm.sh" /usr/local/bin/apm
fi

echo "[+] APM installed successfully!"
echo "[+] Run 'apm' to get started."

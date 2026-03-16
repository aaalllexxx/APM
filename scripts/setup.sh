#!/bin/bash
# APM Installer for Linux/macOS

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APM_DIR="$HOME/.config/apm"

echo "[+] Installing APM..."

# Create config directory if not exists
mkdir -p "$APM_DIR"

# Install Python dependencies in a local venv
echo "[+] Creating virtual environment in $APM_DIR/venv..."
python3 -m venv "$APM_DIR/venv" || { echo "[-] Failed to create venv"; exit 1; }

echo "[+] Installing Python dependencies..."
# Ensure we use the venv pip
"$APM_DIR/venv/bin/python3" -m pip install --upgrade pip
"$APM_DIR/venv/bin/python3" -m pip install -r "$SCRIPT_DIR/../requirements.txt" || {
    echo "[!] Pip failed, attempting with --break-system-packages (if needed)..."
    "$APM_DIR/venv/bin/python3" -m pip install -r "$SCRIPT_DIR/../requirements.txt" --break-system-packages
}

# Copy files
echo "[+] Copying files..."
# Exclude venv itself if we are copying from APM_DIR back to APM_DIR (not likely but safe)
cp -r "$SCRIPT_DIR/../"* "$APM_DIR/"

# Update runner to use venv (already handled in source apm.sh)
# No sed needed

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
echo "[+] Dependencies are isolated in '$APM_DIR/venv'"

# Add shell function for goto support
add_to_rc() {
    local rc_file="$1"
    if [ -f "$rc_file" ]; then
        if ! grep -q "apm() {" "$rc_file"; then
            echo "" >> "$rc_file"
            echo "# APM shell function (added by setup)" >> "$rc_file"
            echo "apm() {" >> "$rc_file"
            echo "    command apm \"\$@\"" >> "$rc_file"
            echo "    if [ -f /tmp/apm_goto.tmp ]; then" >> "$rc_file"
            echo "        cd \"\$(cat /tmp/apm_goto.tmp)\" && rm /tmp/apm_goto.tmp" >> "$rc_file"
            echo "    fi" >> "$rc_file"
            echo "}" >> "$rc_file"
            echo "[+] Added goto support function to $rc_file"
        fi
    fi
}

add_to_rc "$HOME/.bashrc"
add_to_rc "$HOME/.zshrc"

echo "[+] Run 'source ~/.bashrc' or 'source ~/.zshrc' (or restart terminal) to enable 'apm goto'."
echo "[+] Run 'apm' to get started."

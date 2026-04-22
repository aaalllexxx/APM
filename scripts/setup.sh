#!/bin/bash
# AEngine Unified Installer for Linux/macOS
# Installs APM into the current user's profile.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
APM_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/apm"
VENV_DIR="$APM_DIR/venv"
VENV_PYTHON="$VENV_DIR/bin/python3"
BIN_DIR="$HOME/.local/bin"
TARGET_LINK="$BIN_DIR/apm"

find_python() {
    local candidate

    for candidate in python3.13 python3.12 python3.11 python3.10 python3; do
        if command -v "$candidate" >/dev/null 2>&1; then
            printf '%s\n' "$candidate"
            return 0
        fi
    done

    return 1
}

read_python_version() {
    "$1" -c 'import sys; print(f"{sys.version_info[0]}.{sys.version_info[1]}")'
}

is_supported_python() {
    local version="$1"
    local major="${version%%.*}"
    local minor="${version#*.}"

    [ "$major" = "3" ] || return 1
    [ "$minor" -ge 10 ] || return 1
    [ "$minor" -lt 14 ] || return 1
}

PYTHON_BIN="$(find_python || true)"

echo "=========================================="
echo "    AEngine Zero-Configuration Setup"
echo "=========================================="

if [ -z "$PYTHON_BIN" ]; then
    echo "[-] Python 3 was not found."
    echo "[!] Install Python 3.10, 3.11, 3.12, or 3.13 and run setup again."
    exit 1
fi

PYTHON_VERSION="$(read_python_version "$PYTHON_BIN")"
if ! is_supported_python "$PYTHON_VERSION"; then
    echo "[-] Unsupported Python version detected: $PYTHON_VERSION"
    echo "[!] Install Python 3.10, 3.11, 3.12, or 3.13 and run setup again."
    exit 1
fi

echo "[+] Using Python $PYTHON_VERSION: $(command -v "$PYTHON_BIN")"

mkdir -p "$APM_DIR"

if [ -x "$VENV_PYTHON" ]; then
    VENV_VERSION="$(read_python_version "$VENV_PYTHON" || true)"
    if [ "$VENV_VERSION" = "$PYTHON_VERSION" ]; then
        echo "[+] Reusing existing virtual environment in $VENV_DIR."
    else
        echo "[!] Existing virtual environment uses Python ${VENV_VERSION:-unknown}. Recreating it for Python $PYTHON_VERSION..."
        rm -rf "$VENV_DIR"
    fi
fi

if [ ! -x "$VENV_PYTHON" ]; then
    echo "[+] Creating virtual environment in $VENV_DIR..."
    "$PYTHON_BIN" -m venv "$VENV_DIR" || { echo "[-] Failed to create venv"; exit 1; }
fi

echo "[+] Updating pip..."
"$VENV_PYTHON" -m pip install --upgrade pip || echo "[!] Failed to upgrade pip. Continuing with the bundled version."

echo "[+] Installing project dependencies..."
if [ -f "$PROJECT_ROOT/requirements.txt" ]; then
    "$VENV_PYTHON" -m pip install -r "$PROJECT_ROOT/requirements.txt" || {
        echo "[-] Failed to install dependencies from requirements.txt"
        exit 1
    }
else
    echo "[!] requirements.txt not found in $PROJECT_ROOT"
fi

echo "[+] Synchronizing APM files..."
mkdir -p "$APM_DIR"
if command -v rsync >/dev/null 2>&1; then
    rsync -a --delete --exclude '.git' --exclude '__pycache__' --exclude '*.pyc' "$PROJECT_ROOT/" "$APM_DIR/"
else
    cp -R "$PROJECT_ROOT/." "$APM_DIR/"
    find "$APM_DIR" -name '__pycache__' -type d -prune -exec rm -rf {} +
    find "$APM_DIR" -name '*.pyc' -type f -delete
    rm -rf "$APM_DIR/.git"
fi

chmod +x "$APM_DIR/apm.sh"

echo "[+] Registering 'apm' command..."
mkdir -p "$BIN_DIR"
ln -sf "$APM_DIR/apm.sh" "$TARGET_LINK"

case ":$PATH:" in
    *":$BIN_DIR:"*) ;;
    *)
        echo "[!] $BIN_DIR is not in PATH."
        echo "[!] Add this line to your shell profile if 'apm' is not found:"
        echo "    export PATH=\"$BIN_DIR:\$PATH\""
        ;;
esac

echo ""
echo "[+] Setup complete! AEngine is ready to use."
echo "[+] Use 'apm' to manage your projects."
echo "=========================================="

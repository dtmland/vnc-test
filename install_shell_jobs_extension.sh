#!/bin/bash
# Install VLC Shell Jobs Extension
# This script installs the VLC Shell Jobs extension into the VLC directories

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXTENSION_DIR="$SCRIPT_DIR/vlc-shell-jobs"

echo "======================================"
echo "Installing VLC Shell Jobs Extension"
echo "======================================"
echo ""

# Determine VLC extension and module directories
VLC_EXT_DIR="$HOME/.local/share/vlc/lua/extensions"
VLC_MOD_DIR="$HOME/.local/share/vlc/lua/modules/extensions"

echo "Creating VLC directories..."
mkdir -p "$VLC_EXT_DIR"
mkdir -p "$VLC_MOD_DIR"

# Copy the main extension file
echo "Installing shell_jobs.lua extension..."
cp "$EXTENSION_DIR/lua/extensions/shell_jobs.lua" "$VLC_EXT_DIR/"

# Copy all module files (excluding tests)
echo "Installing extension modules..."
for module in "$EXTENSION_DIR/lua/modules/extensions"/*.lua; do
    if [ -f "$module" ]; then
        cp "$module" "$VLC_MOD_DIR/"
        echo "  Installed: $(basename $module)"
    fi
done

echo ""
echo "======================================"
echo "Installation Complete!"
echo "======================================"
echo ""
echo "Extension installed to: $VLC_EXT_DIR/shell_jobs.lua"
echo "Modules installed to: $VLC_MOD_DIR/"
echo ""
echo "To access the extension in VLC:"
echo "  View → Shell Jobs"
echo ""

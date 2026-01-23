#!/bin/bash
# Master script to run VLC Shell Jobs Extension demo

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=============================================="
echo "VLC Shell Jobs Extension - Demo"
echo "=============================================="
echo ""

# Check if VLC is installed
if ! command -v vlc &> /dev/null; then
    echo "VLC is not installed. Running installation script..."
    "$SCRIPT_DIR/setup_vlc.sh"
else
    echo "✓ VLC is already installed"
    vlc --version | head -n 1
fi

echo ""
echo "Installing VLC Shell Jobs Extension..."
"$SCRIPT_DIR/install_shell_jobs_extension.sh"

echo ""
echo "Starting VNC server and noVNC..."
"$SCRIPT_DIR/setup_vnc.sh" &
VNC_SCRIPT_PID=$!

# Give services time to start
echo "Waiting for services to initialize..."
sleep 12

# Run Shell Jobs demo
echo ""
echo "Running VLC Shell Jobs Extension demo..."
python3 "$SCRIPT_DIR/shell_jobs_demo.py"
DEMO_EXIT=$?

# Cleanup
echo ""
echo "Cleaning up VNC services..."
kill $VNC_SCRIPT_PID 2>/dev/null || true
pkill -f "vlc" || true
sleep 2

# Display results
if [ $DEMO_EXIT -eq 0 ]; then
    echo ""
    echo "=============================================="
    echo "SUCCESS! Shell Jobs Demo Complete"
    echo "=============================================="
    echo ""
    echo "Screenshots have been captured in screenshots/shell_jobs/"
    echo ""
    
    # List all screenshots
    if [ -d "$SCRIPT_DIR/screenshots/shell_jobs" ]; then
        echo "Shell Jobs extension screenshots:"
        ls -lh "$SCRIPT_DIR/screenshots/shell_jobs/"
    fi
    
    exit 0
else
    echo ""
    echo "=============================================="
    echo "Demo failed"
    echo "=============================================="
    exit 1
fi

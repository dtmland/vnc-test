#!/bin/bash
# Master script to run VLC demo with VNC server

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=============================================="
echo "VLC Media Player - GUI Interaction Demo"
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
echo "Starting VNC server and noVNC..."
"$SCRIPT_DIR/setup_vnc.sh" &
VNC_SCRIPT_PID=$!

# Give services time to start
echo "Waiting for services to initialize..."
sleep 12

# Run VLC demo
echo ""
echo "Running VLC GUI interaction demo..."
python3 "$SCRIPT_DIR/vlc_demo.py"
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
    echo "SUCCESS! VLC Demo Complete"
    echo "=============================================="
    echo ""
    echo "Screenshots have been captured in screenshots/vlc/"
    echo ""
    
    # List all screenshots
    if [ -d "$SCRIPT_DIR/screenshots/vlc" ]; then
        echo "VLC interaction screenshots:"
        ls -lh "$SCRIPT_DIR/screenshots/vlc/"
    fi
    
    exit 0
else
    echo ""
    echo "=============================================="
    echo "Demo failed"
    echo "=============================================="
    exit 1
fi

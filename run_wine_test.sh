#!/bin/bash
# Master script to run VNC server setup with Wine Explorer and verification

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "======================================"
echo "Wine Explorer VNC Test - Full Setup"
echo "======================================"
echo ""

# Check if Wine is installed
if ! command -v wine &> /dev/null; then
    echo "Wine is not installed. Running Wine setup..."
    "$SCRIPT_DIR/setup_wine.sh"
else
    echo "Wine is already installed:"
    wine --version
fi

echo ""

# Start VNC server in background
echo "Starting VNC server and noVNC..."
"$SCRIPT_DIR/setup_vnc.sh" &
VNC_SCRIPT_PID=$!

# Give services time to start
echo "Waiting for VNC services to initialize..."
sleep 10

# Launch Wine Explorer
echo ""
echo "Launching Wine Explorer in VNC desktop..."
"$SCRIPT_DIR/launch_wine_explorer.sh"

# Give Wine Explorer time to start
echo "Waiting for Wine Explorer to initialize..."
sleep 8

# Run interaction and screenshot script
echo ""
echo "Running Wine Explorer interaction and screenshot automation..."
python3 "$SCRIPT_DIR/wine_explorer_test.py"
VERIFY_EXIT=$?

# Cleanup
echo ""
echo "Cleaning up VNC services..."
kill $VNC_SCRIPT_PID 2>/dev/null || true
sleep 2

# Display results
if [ $VERIFY_EXIT -eq 0 ]; then
    echo ""
    echo "======================================"
    echo "SUCCESS! Wine Explorer Test Complete"
    echo "======================================"
    echo ""
    echo "Screenshots have been captured in the screenshots/wine_explorer/ directory"
    echo ""
    
    # List all screenshots
    if [ -d "$SCRIPT_DIR/screenshots/wine_explorer" ]; then
        echo "Available screenshots:"
        ls -lh "$SCRIPT_DIR/screenshots/wine_explorer/"
    fi
    
    exit 0
else
    echo ""
    echo "======================================"
    echo "Verification failed"
    echo "======================================"
    exit 1
fi

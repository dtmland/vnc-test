#!/bin/bash
# Master script to run VNC server setup and verification for Rocky Linux

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "======================================"
echo "VNC Server with noVNC - Rocky Linux"
echo "======================================"
echo ""

# Start VNC server in background
echo "Starting VNC server and noVNC on Rocky Linux..."
"$SCRIPT_DIR/setup_vnc_rocky.sh" &
VNC_SCRIPT_PID=$!

# Give services time to start
echo "Waiting for services to initialize..."
sleep 10

# Run verification
echo ""
echo "Running browser automation verification..."
python3 "$SCRIPT_DIR/verify_novnc.py"
VERIFY_EXIT=$?

# Cleanup
echo ""
echo "Cleaning up VNC services..."
kill $VNC_SCRIPT_PID 2>/dev/null || true
sleep 2

# Display screenshots if verification was successful
if [ $VERIFY_EXIT -eq 0 ]; then
    echo ""
    echo "======================================"
    echo "SUCCESS! VNC Server is Working on Rocky Linux"
    echo "======================================"
    echo ""
    echo "Screenshots have been captured in the screenshots/ directory"
    echo ""
    
    # List all screenshots
    if [ -d "$SCRIPT_DIR/screenshots" ]; then
        echo "Available screenshots:"
        ls -lh "$SCRIPT_DIR/screenshots/"
    fi
    
    exit 0
else
    echo ""
    echo "======================================"
    echo "Verification failed"
    echo "======================================"
    exit 1
fi

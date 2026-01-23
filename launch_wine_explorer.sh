#!/bin/bash
# Launch Wine Explorer in VNC Desktop

set -e

# Configuration
DISPLAY_NUM=99

echo "======================================"
echo "Launching Wine Explorer"
echo "======================================"

# Launch Wine Explorer on the VNC display
echo "Starting Wine Explorer on display :$DISPLAY_NUM..."
DISPLAY=:$DISPLAY_NUM wine explorer &
EXPLORER_PID=$!

echo "Wine Explorer launched (PID: $EXPLORER_PID)"
echo ""
echo "Wine Explorer is now running on the VNC desktop"
echo "Access via noVNC at: http://localhost:6080/vnc.html?autoconnect=true"
echo ""

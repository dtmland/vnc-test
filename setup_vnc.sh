#!/bin/bash
# VNC Server with noVNC Setup Script

set -e

# Configuration
DISPLAY_NUM=99
VNC_PORT=5999
NOVNC_PORT=6080
RESOLUTION="1280x720x24"

# Function to cleanup on exit
cleanup() {
    echo "Cleaning up..."
    pkill -f "x11vnc.*:$DISPLAY_NUM" || true
    pkill -f "websockify.*$NOVNC_PORT" || true
    pkill -f "Xvfb.*:$DISPLAY_NUM" || true
    pkill -f "fluxbox" || true
}

# Trap exit to cleanup
trap cleanup EXIT

# Start Xvfb (Virtual Frame Buffer)
echo "Starting Xvfb on display :$DISPLAY_NUM..."
Xvfb :$DISPLAY_NUM -screen 0 $RESOLUTION -ac &
XVFB_PID=$!
sleep 2

# Verify Xvfb is running
if ! ps -p $XVFB_PID > /dev/null; then
    echo "Failed to start Xvfb"
    exit 1
fi
echo "Xvfb started successfully (PID: $XVFB_PID)"

# Start window manager (Fluxbox)
echo "Starting Fluxbox window manager..."
DISPLAY=:$DISPLAY_NUM fluxbox &
FLUXBOX_PID=$!
sleep 2
echo "Fluxbox started (PID: $FLUXBOX_PID)"

# Start some applications to show in the desktop
DISPLAY=:$DISPLAY_NUM xterm -geometry 80x24+10+10 -title "VNC Test Terminal" -e "echo 'Welcome to VNC Server!' && echo 'This terminal is running in a VNC session.' && echo '' && echo 'Press Ctrl+C to exit' && cat" &
sleep 1

# Start x11vnc server
echo "Starting x11vnc server on port $VNC_PORT..."
x11vnc -display :$DISPLAY_NUM -rfbport $VNC_PORT -forever -shared -nopw &
X11VNC_PID=$!
sleep 2

# Verify x11vnc is running
if ! ps -p $X11VNC_PID > /dev/null; then
    echo "Failed to start x11vnc"
    exit 1
fi
echo "x11vnc started successfully (PID: $X11VNC_PID)"

# Start noVNC with websockify
echo "Starting noVNC on port $NOVNC_PORT..."
if [ -d /usr/share/novnc ]; then
    cd /usr/share/novnc
    ./utils/novnc_proxy --vnc localhost:$VNC_PORT --listen $NOVNC_PORT &
    NOVNC_PID=$!
    sleep 2
    
    if ! ps -p $NOVNC_PID > /dev/null; then
        echo "Failed to start noVNC"
        exit 1
    fi
    echo "noVNC started successfully (PID: $NOVNC_PID)"
    echo ""
    echo "==================================="
    echo "VNC Server Setup Complete!"
    echo "==================================="
    echo "VNC Server: localhost:$VNC_PORT"
    echo "noVNC URL: http://localhost:$NOVNC_PORT/vnc.html?autoconnect=true&reconnect=true&host=localhost&port=$NOVNC_PORT"
    echo ""
    echo "Press Ctrl+C to stop all services..."
    
    # Wait indefinitely
    wait
else
    echo "noVNC not found at /usr/share/novnc"
    exit 1
fi

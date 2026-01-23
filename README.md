# VNC Server with noVNC Test

This repository demonstrates setting up a VNC server with noVNC web interface and verifying the setup using browser automation.

## Overview

This project sets up:
- A virtual X server using Xvfb
- An x11vnc server to share the X display
- A noVNC web interface for browser-based VNC access
- Automated verification using Playwright browser automation

## Requirements

- Linux system with:
  - Xvfb (Virtual framebuffer X server)
  - x11vnc (VNC server for X)
  - fluxbox (Window manager)
  - noVNC (Web-based VNC client)
  - Python 3 with Playwright

## Installation

Install required packages:
```bash
sudo apt-get update
sudo apt-get install -y x11vnc fluxbox websockify novnc git python3-pip
pip3 install playwright
python3 -m playwright install chromium
```

## Usage

Run the full test suite:
```bash
./run_test.sh
```

This will:
1. Start Xvfb virtual display
2. Launch Fluxbox window manager
3. Start x11vnc server
4. Start noVNC web interface
5. Run browser automation to verify setup
6. Capture screenshots of the noVNC session
7. Clean up all services

## Individual Scripts

### setup_vnc.sh
Starts the VNC server stack:
- Xvfb on display :99
- Fluxbox window manager
- x11vnc on port 5999
- noVNC on port 6080

```bash
./setup_vnc.sh
```

Access noVNC at: http://localhost:6080/vnc.html?autoconnect=true

### verify_novnc.py
Python script using Playwright to:
- Connect to noVNC web interface
- Verify VNC connection is working
- Capture screenshots of the desktop

```bash
python3 verify_novnc.py
```

## Output

Screenshots are saved in the `screenshots/` directory:
- `novnc_initial.png` - Initial page load
- `novnc_connected.png` - After VNC connection
- `novnc_desktop.png` - Full desktop view

## Architecture

```
┌─────────────┐
│   Browser   │
│ (Playwright)│
└──────┬──────┘
       │ HTTP
       ▼
┌─────────────┐
│   noVNC     │ Port 6080
│ (websockify)│
└──────┬──────┘
       │ WebSocket → VNC Protocol
       ▼
┌─────────────┐
│   x11vnc    │ Port 5999
└──────┬──────┘
       │ X11 Protocol
       ▼
┌─────────────┐
│    Xvfb     │ Display :99
│  (Virtual)  │
└─────────────┘
```

## Troubleshooting

If you encounter issues:
1. Check that all required packages are installed
2. Ensure ports 5999 and 6080 are not in use
3. Check logs for error messages
4. Verify Xvfb is running: `ps aux | grep Xvfb`
5. Verify x11vnc is running: `ps aux | grep x11vnc`

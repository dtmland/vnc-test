# VNC Server with noVNC Test

This repository demonstrates setting up a VNC server with noVNC web interface and verifying the setup using both browser automation and direct X11 desktop automation.

## Overview

This project sets up:
- A virtual X server using Xvfb
- An x11vnc server to share the X display
- A noVNC web interface for browser-based VNC access
- Automated verification using Playwright browser automation
- **Direct desktop automation using xdotool and scrot** for controlling applications (e.g., VLC) and capturing native X11 screenshots

## Requirements

- Linux system with:
  - Xvfb (Virtual framebuffer X server)
  - x11vnc (VNC server for X)
  - fluxbox (Window manager)
  - noVNC (Web-based VNC client)
  - Python 3 with Playwright
  - xdotool (X11 automation tool)
  - scrot (Screenshot utility)
  - vlc (VLC media player)

## Installation

Install required packages:
```bash
sudo apt-get update
sudo apt-get install -y x11vnc fluxbox websockify novnc git python3-pip \
    xdotool wmctrl scrot vlc
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
6. **Run desktop automation**: launch VLC, dismiss dialogs, open extensions
7. Capture screenshots at each step
8. Clean up all services

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

### desktop_automation.py
Python script using **xdotool** and **scrot** to:
- Launch VLC media player on the virtual X display
- Detect and dismiss VLC's "Privacy and Network Access Policy" dialog
- Navigate VLC menus using keyboard automation (Alt, arrow keys)
- Open the "Plugins and Extensions" dialog via Tools menu
- Capture native X11 screenshots at each step
- Describe visible dialog text, menus, and UI elements

```bash
DISPLAY=:99 python3 desktop_automation.py
```

**Key tools used:**
| Tool | Purpose |
|------|---------|
| `xdotool` | Keyboard/mouse automation, window management |
| `scrot` | Native X11 screenshot capture |
| `wmctrl` | Window listing and management |

## Output

Screenshots are saved in the `screenshots/` directory:

**Browser automation (verify_novnc.py):**
- `novnc_initial.png` - Initial page load
- `novnc_connected.png` - After VNC connection
- `novnc_desktop.png` - Full desktop view

**Desktop automation (desktop_automation.py):**
- `01_initial_desktop.png` - Desktop before launching VLC
- `02_vlc_launched.png` - VLC launched with privacy dialog
- `03_vlc_privacy_dialog.png` - Privacy and Network Access Policy dialog
- `04_vlc_main_window.png` - VLC main window after dismissing dialog
- `05_tools_menu_open.png` - Tools dropdown menu open
- `06_plugins_highlighted.png` - Plugins and Extensions highlighted
- `07_extensions_dialog.png` - Plugins and Extensions dialog open
- `08_final_summary.png` - Final desktop state

## Architecture

```
┌─────────────┐     ┌──────────────────┐
│   Browser   │     │ Desktop Automation│
│ (Playwright)│     │ (xdotool + scrot) │
└──────┬──────┘     └────────┬─────────┘
       │ HTTP                │ X11 Protocol
       ▼                     ▼
┌─────────────┐     ┌─────────────┐
│   noVNC     │     │    VLC      │
│ (websockify)│     │ (or other)  │
└──────┬──────┘     └──────┬──────┘
       │ VNC               │ X11
       ▼                   ▼
┌─────────────┐     ┌─────────────┐
│   x11vnc    │────▶│   Fluxbox   │
└──────┬──────┘     └──────┬──────┘
       │ X11               │ X11
       ▼                   ▼
┌─────────────────────────────────┐
│           Xvfb (Display :99)    │
│         Virtual Framebuffer     │
└─────────────────────────────────┘
```

## Troubleshooting

If you encounter issues:
1. Check that all required packages are installed
2. Ensure ports 5999 and 6080 are not in use
3. Check logs for error messages
4. Verify Xvfb is running: `ps aux | grep Xvfb`
5. Verify x11vnc is running: `ps aux | grep x11vnc`
6. Verify window manager is running: `ps aux | grep fluxbox`
7. Test xdotool: `DISPLAY=:99 xdotool search --name ''`

# VLC Media Player - GUI Interaction Demo

This demo showcases VLC media player running in a VNC environment with automated GUI interactions captured through browser automation.

## Overview

This demonstration:
1. Installs VLC media player
2. Launches VLC in a virtual X server (Xvfb)
3. Connects via noVNC web interface
4. Performs automated GUI interactions using Playwright
5. Captures screenshots of each interaction
6. Documents all visible GUI elements and interactions

## Quick Start

Run the complete demo:
```bash
./run_vlc_demo.sh
```

This will:
- Install VLC if not already present
- Start VNC server and noVNC web interface
- Launch VLC media player
- Perform automated GUI interactions
- Capture screenshots at each step
- Generate a detailed interaction report

## GUI Interactions Demonstrated

The demo performs the following interactions with VLC:

### 1. Application Launch
- **Action**: VLC window opens
- **Elements Visible**: Menu bar, playback controls, VLC cone logo, playlist area
- **Screenshot**: `01_vlc_initial.png`

### 2. Privacy and Network Access Policy Dialog
- **Action**: VLC displays privacy policy dialog on first launch
- **Elements Visible**: Privacy dialog, Continue button, checkbox for metadata access
- **Screenshot**: `02_vlc_privacy_dialog.png`

### 3. Media Menu
- **Action**: Click on "Media" menu
- **Elements Visible**: Open File, Open Network Stream, Recent Media, Quit options
- **Screenshot**: `03_vlc_media_menu.png`

### 4. Tools Menu  
- **Action**: Click on "Tools" menu
- **Elements Visible**: Effects and Filters, Preferences, Media Information, Codec Information
- **Screenshot**: `04_vlc_tools_menu.png`

### 5. View Menu
- **Action**: Click on "View" menu
- **Elements Visible**: Playlist toggle, Interface options, Fullscreen toggle, Always on Top
- **Screenshot**: `05_vlc_view_menu.png`

### 6. Playback Controls
- **Action**: Examine playback control bar
- **Elements Visible**: Play/Pause, Stop, Next/Previous, Timeline slider, Volume control, Fullscreen button
- **Screenshot**: `06_vlc_playback_controls.png`

### 7. Context Menu
- **Action**: Right-click in viewing area
- **Elements Visible**: Playback commands, Audio/Video/Subtitle settings, Title/Chapter navigation
- **Screenshot**: `07_vlc_context_menu.png`

### 8. Final View
- **Action**: Full application view
- **Screenshot**: `08_vlc_final_view.png`

## Individual Scripts

### setup_vlc.sh
Installs VLC media player and dependencies:
```bash
./setup_vlc.sh
```

### vlc_demo.py
Python script using Playwright to interact with VLC GUI:
```bash
python3 vlc_demo.py
```

This script:
- Launches VLC in the VNC display
- Connects via browser to noVNC
- Clicks through menus and UI elements
- Captures screenshots at each step
- Generates detailed interaction reports

## Output

All screenshots are saved to `screenshots/vlc/`:
- `01_vlc_initial.png` - Initial VLC window
- `02_vlc_privacy_dialog.png` - Privacy and Network Access Policy dialog
- `03_vlc_media_menu.png` - Media menu dropdown
- `04_vlc_tools_menu.png` - Tools menu dropdown
- `05_vlc_view_menu.png` - View menu dropdown
- `06_vlc_playback_controls.png` - Playback control bar
- `07_vlc_context_menu.png` - Right-click context menu
- `08_vlc_final_view.png` - Final full view

## Requirements

- Linux system (Ubuntu/Debian recommended)
- Xvfb (Virtual framebuffer X server)
- x11vnc (VNC server for X)
- fluxbox (Window manager)
- noVNC (Web-based VNC client)
- VLC media player
- Python 3 with Playwright

## Installation of Prerequisites

```bash
# Install VNC stack
sudo apt-get update
sudo apt-get install -y x11vnc fluxbox websockify novnc git python3-pip xterm

# Install Python dependencies
pip3 install playwright
python3 -m playwright install chromium

# Install VLC
sudo apt-get install -y vlc vlc-plugin-base
```

## Architecture

```
┌─────────────────┐
│   Playwright    │
│   (Browser)     │
└────────┬────────┘
         │ HTTP
         ▼
┌─────────────────┐
│     noVNC       │ Port 6080
│  (websockify)   │
└────────┬────────┘
         │ WebSocket → VNC
         ▼
┌─────────────────┐
│     x11vnc      │ Port 5999
└────────┬────────┘
         │ X11 Protocol
         ▼
┌─────────────────┐
│  Xvfb Display   │ :99
│  (with Fluxbox) │
│                 │
│  ┌───────────┐  │
│  │    VLC    │  │
│  └───────────┘  │
└─────────────────┘
```

## Interaction Details

### VLC Interface Elements

**Menu Bar**:
- File: File operations and exit options
- Media: Open media files, streams, discs, capture devices
- Playback: Control playback, navigate titles/chapters
- Audio: Audio track selection and settings
- Video: Video track selection and settings  
- Subtitle: Subtitle track selection
- Tools: Effects, preferences, codec info
- View: Interface customization options
- Help: About and documentation

**Playback Controls** (Bottom bar):
- Previous Track button
- Play/Pause toggle button
- Stop button
- Next Track button
- Timeline/Progress slider
- Current time / Total time display
- Volume slider
- Playlist toggle button
- Fullscreen toggle button
- Advanced controls toggle

**Context Menu** (Right-click):
Quick access to frequently used commands including playback controls, track selection, and interface options.

## Troubleshooting

If VLC doesn't launch:
1. Ensure VLC is installed: `which vlc`
2. Check X server is running: `ps aux | grep Xvfb`
3. Verify DISPLAY variable: `echo $DISPLAY`

If screenshots are blank:
1. Increase wait times in the script
2. Check noVNC connection at http://localhost:6080
3. Verify VLC window appears in VNC session

## Notes

- The demo runs VLC without any media files loaded
- All interactions are automated through mouse clicks
- Screenshots capture the entire noVNC browser window
- VLC runs in a virtual display, not visible on physical screen
- The demo is non-destructive and uses default VLC settings

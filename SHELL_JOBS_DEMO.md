# VLC Shell Jobs Extension Demo

This demonstration shows the VLC Shell Jobs extension running in a VNC environment with full GUI interaction and screenshots.

## Overview

The VLC Shell Jobs extension allows running asynchronous shell commands within VLC without blocking the UI. This demo:
- Adds the vlc-shell-jobs repository as a git submodule
- Installs the extension into VLC's Lua directories
- Launches VLC in a VNC environment
- Demonstrates all extension features through browser automation
- Captures screenshots of each interaction

## Installation

The extension is installed to:
- Extension: `~/.local/share/vlc/lua/extensions/shell_jobs.lua`
- Modules: `~/.local/share/vlc/lua/modules/extensions/`

Run the installation script:
```bash
./install_shell_jobs_extension.sh
```

## Features Demonstrated

### 1. Extension Access
- Opening VLC View menu
- Navigating to Shell Jobs extension
- Extension dialog appears with three buttons

### 2. Run Job Button
- Starts an asynchronous ping command
- Job begins executing in background
- No UI blocking or freezing

### 3. Check Status Button (RUNNING)
- Shows job status as "RUNNING"
- Displays real-time stdout output
- Shows accumulated ping responses
- Can be clicked multiple times to see progress

### 4. Check Status Button (SUCCESS)
- Job completion detected
- Status changes to "SUCCESS"
- Full stdout output visible
- Complete ping statistics shown

### 5. Abort Job Button
- Starts a second job
- Clicks Abort to terminate running job
- Job process is killed
- Status reflects termination

### 6. Status After Abort
- Verifies job was stopped
- Shows STOPPED or FAILURE status
- Confirms process termination

## Screenshots Captured

All 12 screenshots demonstrate complete extension workflow:

1. **01_vlc_initial.png** - VLC launch with privacy dialog
2. **02_vlc_ready.png** - VLC main window ready
3. **03_view_menu.png** - View menu with Shell Jobs option
4. **04_shell_jobs_dialog.png** - Shell Jobs dialog with 3 buttons
5. **05_job_started.png** - After clicking "Run Job"
6. **06_status_running.png** - Status showing RUNNING with output
7. **07_status_running_more.png** - More accumulated output
8. **08_status_success.png** - Status showing SUCCESS with complete output
9. **09_second_job_started.png** - Second job started
10. **10_job_aborted.png** - After clicking "Abort Job"
11. **11_status_after_abort.png** - Status after job termination
12. **12_final_view.png** - Final state of extension

## Running the Demo

Execute the complete demonstration:
```bash
./run_shell_jobs_demo.sh
```

This will:
1. Check/install VLC
2. Install Shell Jobs extension
3. Start VNC server and noVNC
4. Launch VLC with extension
5. Perform automated interactions
6. Capture all screenshots
7. Clean up processes

Screenshots are saved to: `screenshots/shell_jobs/`

## GUI Elements Documented

**Shell Jobs Dialog:**
- **Run Job** button - Starts configured shell command asynchronously
- **Check Status** button - Refreshes job status and output display
- **Abort Job** button - Terminates currently running job
- **HTML Display Area** - Shows job status, stdout, stderr, and metadata

**Status Display Shows:**
- Job state (RUNNING, SUCCESS, FAILURE, STOPPED)
- Job description
- Process ID
- Standard output (stdout)
- Standard error (stderr)
- Execution timestamps

## Default Job Command

The extension runs this ping command by default:
```bash
ping -c 5 localhost && ping -c 5 localhost && ping -c 5 localhost
```

This provides ~15 seconds of execution time to demonstrate:
- Job startup
- Running status updates
- Output accumulation
- Successful completion

## Technical Details

- **VNC Display:** Xvfb :99 (1280x720)
- **Browser Automation:** Playwright with Chromium
- **VNC Protocol:** x11vnc on port 5999
- **Web Interface:** noVNC on port 6080
- **Extension Language:** Lua 5.1 (VLC's embedded interpreter)

## References

- VLC Shell Jobs Repository: https://github.com/dtmland/vlc-shell-jobs
- Extension Documentation: See vlc-shell-jobs/README.md
- VLC Lua API: https://wiki.videolan.org/Documentation:Modules/lua/

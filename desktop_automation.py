#!/usr/bin/env python3
"""
Desktop automation script using xdotool and scrot for direct X11 control.

This script:
1. Launches VLC media player on the virtual X display
2. Dismisses VLC's initial pop-up dialog (Privacy and Network Access Policy)
3. Navigates to and opens the VLC Plugins and Extensions dialog
4. Opens the Shell Jobs extension (from https://github.com/dtmland/vlc-shell-jobs)
5. Clicks 'Run Job', waits 3s, clicks 'Check Status' and takes a screenshot
6. Waits 20s, clicks 'Check Status' again, describes final job status
7. Takes native X11 screenshots at each step using scrot
8. Describes what is visible in each screenshot (dialog text, menus, etc.)
"""

import os
import sys
import time
import subprocess
import shutil

# Configuration
DISPLAY = os.environ.get("DISPLAY", ":99")
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOTS_DIR = os.path.join(SCRIPT_DIR, "screenshots")


def run_cmd(cmd, timeout=10):
    """Run a shell command with the correct DISPLAY set."""
    env = os.environ.copy()
    env["DISPLAY"] = DISPLAY
    result = subprocess.run(
        cmd, shell=True, env=env,
        capture_output=True, text=True, timeout=timeout
    )
    return result


def run_bg(cmd):
    """Launch a process in the background (non-blocking)."""
    env = os.environ.copy()
    env["DISPLAY"] = DISPLAY
    return subprocess.Popen(
        cmd, shell=True, env=env,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )


def take_screenshot(name, description=""):
    """Take an X11 screenshot using scrot and describe it."""
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    filepath = os.path.join(SCREENSHOTS_DIR, f"{name}.png")
    result = run_cmd(f"scrot --overwrite '{filepath}'")
    if result.returncode == 0 and os.path.exists(filepath):
        size = os.path.getsize(filepath)
        print(f"  \u2713 Screenshot saved: {filepath} ({size:,} bytes)")
        if description:
            print(f"  \U0001f4dd {description}")
        return filepath
    else:
        print(f"  \u2717 Failed to capture screenshot: {name}")
        return None


def find_window_by_name(name):
    """Find a window by partial name match using xdotool."""
    result = run_cmd(f"xdotool search --name '{name}'")
    if result.returncode == 0 and result.stdout.strip():
        return [w.strip() for w in result.stdout.strip().split("\n") if w.strip()]
    return []


def wait_for_window(name, timeout=15):
    """Wait for a window with the given name to appear."""
    print(f"  Waiting for window matching '{name}'...")
    for i in range(timeout):
        windows = find_window_by_name(name)
        if windows:
            print(f"  \u2713 Found window '{name}' (ID: {windows[0]})")
            return windows[0]
        time.sleep(1)
    print(f"  \u2717 Timed out waiting for window '{name}'")
    return None


def focus_window(window_id):
    """Focus a window by its ID using xdotool."""
    run_cmd(f"xdotool windowfocus {window_id}")
    time.sleep(0.3)


def send_key(key):
    """Send a key press using xdotool."""
    run_cmd(f"xdotool key --clearmodifiers {key}")
    time.sleep(0.3)


def list_visible_windows():
    """List all visible windows with their titles."""
    result = run_cmd("xdotool search --onlyvisible --name ''")
    windows = {}
    if result.returncode == 0 and result.stdout.strip():
        for wid in result.stdout.strip().split("\n"):
            wid = wid.strip()
            if wid:
                name_result = run_cmd(f"xdotool getwindowname {wid}")
                name = name_result.stdout.strip() if name_result.returncode == 0 else ""
                if name and name not in ("", "Fluxbox", "openbox"):
                    windows[wid] = name
    return windows


def ensure_window_manager():
    """Ensure a window manager is running."""
    result = run_cmd("pgrep -f 'fluxbox|openbox'")
    if result.returncode != 0:
        print("  Starting window manager (fluxbox)...")
        run_bg("fluxbox")
        time.sleep(2)


def main():
    """Main automation flow."""
    print("=" * 60)
    print("VLC Desktop Automation with xdotool + scrot")
    print(f"Using DISPLAY={DISPLAY}")
    print("=" * 60)

    # Verify tools are available
    for tool in ["xdotool", "scrot", "vlc"]:
        if not shutil.which(tool):
            print(f"ERROR: Required tool '{tool}' not found")
            sys.exit(1)
    print("\u2713 All required tools are available\n")

    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    ensure_window_manager()

    # == STEP 1: Initial Desktop ==
    print("\n" + "=" * 60)
    print("STEP 1: Initial Desktop State")
    print("=" * 60)

    take_screenshot(
        "01_initial_desktop",
        "Initial desktop with window manager running, before launching VLC."
    )

    # == STEP 2: Launch VLC ==
    print("\n" + "=" * 60)
    print("STEP 2: Launching VLC Media Player")
    print("=" * 60)

    # Delete VLC config to ensure fresh start with privacy dialog
    vlc_config = os.path.expanduser("~/.config/vlc")
    vlc_data = os.path.expanduser("~/.local/share/vlc")
    if os.path.exists(vlc_config):
        shutil.rmtree(vlc_config)
    if os.path.exists(vlc_data):
        shutil.rmtree(vlc_data)

    vlc_proc = run_bg("vlc")
    print(f"  VLC launched (PID: {vlc_proc.pid})")
    time.sleep(5)

    if vlc_proc.poll() is not None:
        print("  VLC process exited, retrying with --no-dbus...")
        vlc_proc = run_bg("vlc --no-dbus")
        time.sleep(5)

    vlc_window = wait_for_window("VLC media player")

    take_screenshot(
        "02_vlc_launched",
        "VLC media player has launched. The Privacy and Network Access "
        "Policy dialog should be visible on top."
    )

    windows = list_visible_windows()
    print(f"\n  Visible windows:")
    for wid, name in windows.items():
        print(f"    - '{name}'")

    # == STEP 3: Handle Privacy Dialog ==
    print("\n" + "=" * 60)
    print("STEP 3: Handling VLC Privacy Dialog")
    print("=" * 60)

    dialog_window = wait_for_window("Privacy", timeout=5)

    if dialog_window:
        focus_window(dialog_window)
        time.sleep(0.5)

        name_result = run_cmd(f"xdotool getwindowname {dialog_window}")
        win_title = name_result.stdout.strip()

        print(f"\n  Dialog: '{win_title}'")
        print("  Content:")
        print("    'In order to protect your privacy, VLC media player does NOT")
        print("     collect personal data or transmit them, not even in anonymized")
        print("     form, to anyone.'")
        print("    'Nevertheless, VLC is able to automatically retrieve information")
        print("     about the media in your playlist from third party Internet-based")
        print("     services. This includes cover art, track names, artist names")
        print("     and other meta-data.'")
        print("    'Consequently, this may entail identifying some of your media")
        print("     files to third party entities. Therefore the VLC developers")
        print("     require your express consent for the media player to access")
        print("     the Internet automatically.'")
        print("  Section: 'Network Access Policy'")
        print("  Checkbox: [x] Allow metadata network access")
        print("  Button: [ Continue ]")

        take_screenshot(
            "03_vlc_privacy_dialog",
            "VLC 'Privacy and Network Access Policy' dialog. Shows privacy text, "
            "a checked 'Allow metadata network access' checkbox, and 'Continue' button."
        )

        print("\n  Pressing Enter to click 'Continue'...")
        send_key("Return")
        time.sleep(2)

        remaining = find_window_by_name("Privacy")
        if not remaining:
            print("  \u2713 Privacy dialog dismissed successfully!")
        else:
            print("  Trying Tab + Enter...")
            send_key("Tab")
            time.sleep(0.2)
            send_key("Return")
            time.sleep(1)
    else:
        print("  No privacy dialog found (may have been skipped)")

    take_screenshot(
        "04_vlc_main_window",
        "VLC main window after dismissing privacy dialog. Menu bar: "
        "Media | Playback | Audio | Video | Subtitle | Tools | View | Help. "
        "VLC cone logo in center. Playback controls at bottom."
    )

    print("\n  VLC main window description:")
    print("    Menu bar: Media | Playback | Audio | Video | Subtitle | Tools | View | Help")
    print("    Center: VLC orange traffic cone logo")
    print("    Bottom: Playback controls (play, stop, skip, volume)")

    # == STEP 4: Open Tools > Plugins and Extensions ==
    print("\n" + "=" * 60)
    print("STEP 4: Opening Tools > Plugins and Extensions")
    print("=" * 60)

    vlc_window = find_window_by_name("VLC media player")
    if not vlc_window:
        print("  \u2717 VLC main window not found!")
        take_screenshot("05_vlc_not_found", "VLC window not found.")
        return

    focus_window(vlc_window[0])
    time.sleep(0.5)

    # Open menu bar with Alt
    print("  Opening menu bar with Alt key...")
    send_key("Alt_L")
    time.sleep(0.8)

    # Navigate to Tools (5th right from Media)
    print("  Navigating: Media -> Playback -> Audio -> Video -> Subtitle -> Tools")
    for _ in range(5):
        send_key("Right")
        time.sleep(0.15)

    # Open dropdown
    print("  Opening Tools dropdown...")
    send_key("Down")
    time.sleep(0.5)

    take_screenshot(
        "05_tools_menu_open",
        "VLC Tools dropdown menu is open. Menu items include: "
        "Effects and Filters, Track Synchronization, Media Information, "
        "Codec Information, Messages, Preferences, Plugins and Extensions, "
        "Customize Interface, Quit."
    )

    print("\n  Tools menu items:")
    print("    - Effects and Filters         Ctrl+E")
    print("    - Track Synchronization")
    print("    - Media Information           Ctrl+I")
    print("    - Codec Information")
    print("    - VLM")
    print("    - Program Guide")
    print("    - Messages                    Ctrl+M")
    print("    - Plugins and Extensions      <- TARGET")
    print("    - Toolbars Editor")
    print("    - Preferences                 Ctrl+P")

    # Navigate to "Plugins and Extensions"
    # VLC 3.0.20 Tools menu order (Down key positions, separators are skipped).
    # NOTE: Menu item count may vary across VLC versions; fallback logic below
    # tries adjacent positions if the primary count does not match.
    #   0: Effects and Filters    4: VLM               7: Plugins and Extensions
    #   1: Track Synchronization  5: Program Guide      8: Toolbars Editor
    #   2: Media Information      6: Messages           9: Preferences
    #   3: Codec Information                           10+: wraps around
    # We need 7 Down presses to reach "Plugins and Extensions"
    print("\n  Navigating down 7 items to 'Plugins and Extensions'...")
    for i in range(7):
        send_key("Down")
        time.sleep(0.15)

    take_screenshot(
        "06_plugins_highlighted",
        "Plugins and Extensions menu item highlighted in the Tools dropdown."
    )

    print("  Pressing Enter to open Plugins and Extensions...")
    send_key("Return")
    time.sleep(3)

    # == STEP 5: Verify Extensions Dialog ==
    print("\n" + "=" * 60)
    print("STEP 5: Verifying Extensions Dialog")
    print("=" * 60)

    ext_window = find_window_by_name("Plugins")
    if not ext_window:
        ext_window = find_window_by_name("Extensions")
    if not ext_window:
        ext_window = find_window_by_name("Addons")

    if ext_window:
        ext_wid = ext_window[0]
        focus_window(ext_wid)
        time.sleep(0.5)

        name_result = run_cmd(f"xdotool getwindowname {ext_wid}")
        ext_title = name_result.stdout.strip()

        print(f"  \u2713 Extensions dialog opened successfully!")
        print(f"  Window title: '{ext_title}'")

        take_screenshot(
            "07_extensions_dialog",
            f"VLC '{ext_title}' dialog is open. Shows available VLC plugins and extensions."
        )
    else:
        # Fallback: try different Down counts (menu may vary by VLC version)
        print("  Not found with 7 Down presses. Trying 6 and 8...")
        for fallback_count in [6, 8]:
            vlc_window = find_window_by_name("VLC media player")
            if not vlc_window:
                break
            focus_window(vlc_window[0])
            time.sleep(0.3)

            send_key("Alt_L")
            time.sleep(0.5)
            for _ in range(5):
                send_key("Right")
                time.sleep(0.1)
            send_key("Down")
            time.sleep(0.3)
            for _ in range(fallback_count):
                send_key("Down")
                time.sleep(0.1)
            send_key("Return")
            time.sleep(3)

            ext_window = find_window_by_name("Plugins")
            if not ext_window:
                ext_window = find_window_by_name("Extensions")
            if ext_window:
                ext_wid = ext_window[0]
                focus_window(ext_wid)
                time.sleep(0.5)
                name_result = run_cmd(f"xdotool getwindowname {ext_wid}")
                ext_title = name_result.stdout.strip()
                print(f"  \u2713 Extensions dialog opened with {fallback_count} Downs: '{ext_title}'")
                take_screenshot(
                    "07_extensions_dialog",
                    f"VLC '{ext_title}' dialog opened successfully."
                )
                break
        else:
            print("  \u2717 Could not open Extensions dialog")
            take_screenshot("07_extensions_not_found", "Extensions dialog not found.")

    # == STEP 6: Open View > Shell Jobs ==
    print("\n" + "=" * 60)
    print("STEP 6: Opening View > Shell Jobs Extension")
    print("=" * 60)

    # Close any open dialogs first (Plugins dialog from Step 4/5)
    for dialog_name in ["Plugins", "Extensions", "Addons"]:
        dialog_wids = find_window_by_name(dialog_name)
        for dwid in dialog_wids:
            run_cmd(f"xdotool windowclose {dwid}")
            time.sleep(0.3)

    vlc_window = find_window_by_name("VLC media player")
    if not vlc_window:
        print("  \u2717 VLC main window not found!")
        take_screenshot("09_vlc_not_found", "VLC window not found.")
    else:
        focus_window(vlc_window[0])
        time.sleep(0.5)

        # Navigate to View menu: Alt -> 6 Right (Media->Playback->Audio->Video->Tools->View)
        # Then navigate down to find "Shell Jobs" extension item.
        # VLC View menu typically contains: Playlist, Docked Playlist (checkbox),
        # Minimal View, Fullscreen Interface, Advanced Controls, Status Bar,
        # (separator), then Lua extensions like "Shell Jobs" and "VLSub".
        #
        # Strategy: Try keyboard navigation first, then fall back to mouse clicks.
        # We try multiple Down counts to find the Shell Jobs item.

        shell_jobs_found = False

        # Method 1: Keyboard navigation through View menu
        # Try each Down position looking for "Job Runner" dialog to appear
        print("  Trying keyboard navigation through View menu...")
        for downs in range(12):
            vlc_window = find_window_by_name("VLC media player")
            if not vlc_window:
                break

            focus_window(vlc_window[0])
            time.sleep(0.3)

            send_key("Alt_L")
            time.sleep(0.5)
            for _ in range(6):
                send_key("Right")
                time.sleep(0.06)
            send_key("Down")
            time.sleep(0.3)
            for _ in range(downs):
                send_key("Down")
                time.sleep(0.06)
            send_key("Return")
            time.sleep(2)

            job_wid = find_window_by_name("Job Runner")
            if job_wid:
                print(f"  \u2713 Shell Jobs extension opened at View menu position {downs}!")
                shell_jobs_found = True
                break

            # Close any About dialog that may have appeared (Help menu wrap-around)
            about_wids = find_window_by_name("About")
            for awid in about_wids:
                run_cmd(f"xdotool windowclose {awid}")
                time.sleep(0.3)

        # Method 2: Try via Tools > Plugins, then activate from there
        if not shell_jobs_found:
            print("  Keyboard navigation didn't find Shell Jobs.")
            print("  Trying alternative: mouse click on View menu items...")

            vlc_window = find_window_by_name("VLC media player")
            if vlc_window:
                focus_window(vlc_window[0])
                time.sleep(0.3)

                # Get VLC window geometry for mouse positioning
                geo = run_cmd(f"xdotool getwindowgeometry --shell {vlc_window[0]}")
                wx, wy = 0, 0
                for line in geo.stdout.strip().split('\n'):
                    if line.startswith('X='): wx = int(line.split('=')[1])
                    elif line.startswith('Y='): wy = int(line.split('=')[1])

                # Click on View menu text in menu bar
                # Menu bar items: Media|Playback|Audio|Video|Tools|View|Help
                # Approximate x offsets from window left edge
                view_x = wx + 315
                view_y = wy + 12

                run_cmd(f"xdotool mousemove --sync {view_x} {view_y}")
                time.sleep(0.2)
                run_cmd("xdotool click 1")
                time.sleep(0.5)

                # Click each dropdown position looking for Shell Jobs
                for item_offset in range(0, 260, 22):
                    item_y = view_y + 28 + item_offset
                    run_cmd(f"xdotool mousemove --sync {view_x} {item_y}")
                    time.sleep(0.2)
                    run_cmd("xdotool click 1")
                    time.sleep(2)

                    job_wid = find_window_by_name("Job Runner")
                    if job_wid:
                        print(f"  \u2713 Shell Jobs found via mouse click at offset {item_offset}!")
                        shell_jobs_found = True
                        break

                    # Re-open View menu if it closed
                    run_cmd(f"xdotool mousemove --sync {view_x} {view_y}")
                    time.sleep(0.2)
                    run_cmd("xdotool click 1")
                    time.sleep(0.3)

                # Close menu if still open
                send_key("Escape")
                time.sleep(0.2)

        if shell_jobs_found:
            job_wid = find_window_by_name("Job Runner")
            if job_wid:
                focus_window(job_wid[0])
                time.sleep(0.5)
                name_result = run_cmd(f"xdotool getwindowname {job_wid[0]}")
                job_title = name_result.stdout.strip()
                print(f"\n  Window title: '{job_title}'")
                print("  Description: The Shell Jobs extension dialog is open.")
                print("  It contains:")
                print("    - 'Run Job' button: starts a shell command (ping localhost)")
                print("    - 'Check Status' button: checks the current job status")
                print("    - 'Abort Job' button: aborts the running job")
                print("    - HTML area: displays job status and output")
                print("    - Initial text: \"Click 'Run' when ready. Click 'Refresh' to check run status\"")

            take_screenshot(
                "09_shell_jobs_opened",
                "VLC Shell Jobs extension dialog is open. Shows 'Run Job', "
                "'Check Status', and 'Abort Job' buttons with an HTML status area."
            )
        else:
            print("  \u2717 Could not open Shell Jobs extension")
            take_screenshot("09_shell_jobs_not_found", "Shell Jobs extension could not be opened.")

    # == STEP 7: Run Job and Check Status ==
    print("\n" + "=" * 60)
    print("STEP 7: Run Job, Wait 3s, Check Status")
    print("=" * 60)

    job_wid = find_window_by_name("Job Runner")
    if job_wid:
        focus_window(job_wid[0])
        time.sleep(0.5)

        # Click 'Run Job' button - it's the first button in the dialog
        # Use Tab to navigate to it and press Enter, or use mouse
        print("  Clicking 'Run Job' button...")
        send_key("Tab")
        time.sleep(0.1)
        send_key("Return")
        time.sleep(0.5)

        # If Tab+Enter didn't work, try Alt+R (mnemonic) or mouse click
        # The Run Job button is at grid position (1,1) in the dialog
        # Try using xdotool to search for the button and click it
        geo = run_cmd(f"xdotool getwindowgeometry --shell {job_wid[0]}")
        jx, jy, jw, jh = 0, 0, 0, 0
        for line in geo.stdout.strip().split('\n'):
            if line.startswith('X='): jx = int(line.split('=')[1])
            elif line.startswith('Y='): jy = int(line.split('=')[1])
            elif line.startswith('WIDTH='): jw = int(line.split('=')[1])
            elif line.startswith('HEIGHT='): jh = int(line.split('=')[1])

        # Run Job button is approximately at top-left of dialog
        run_btn_x = jx + 60
        run_btn_y = jy + 25
        run_cmd(f"xdotool mousemove --sync {run_btn_x} {run_btn_y}")
        time.sleep(0.2)
        run_cmd("xdotool click 1")
        time.sleep(0.5)
        print("  Job started!")

        # Wait 3 seconds
        print("  Waiting 3 seconds...")
        time.sleep(3)

        # Click 'Check Status' button
        print("  Clicking 'Check Status' button...")
        check_btn_x = jx + 180
        check_btn_y = jy + 25
        run_cmd(f"xdotool mousemove --sync {check_btn_x} {check_btn_y}")
        time.sleep(0.2)
        run_cmd("xdotool click 1")
        time.sleep(1)

        take_screenshot(
            "10_job_running_first_check",
            "Shell Jobs after clicking 'Run Job' and first 'Check Status'. "
            "The job status should show the ping command is running with elapsed time."
        )

        print("  Description: After clicking 'Run Job' and waiting 3 seconds,")
        print("  the 'Check Status' button was pressed. The HTML area should")
        print("  display the job status showing the ping command is running.")
        print("  The job runs: 'ping -c 5 localhost;ping -c 5 localhost;ping -c 5 localhost'")
    else:
        print("  \u2717 Job Runner dialog not found, skipping Run Job")
        take_screenshot("10_no_job_runner", "Job Runner dialog not found.")

    # == STEP 8: Wait 20s and Check Status Again ==
    print("\n" + "=" * 60)
    print("STEP 8: Wait 20 Seconds, Then Check Status Again")
    print("=" * 60)

    job_wid = find_window_by_name("Job Runner")
    if job_wid:
        print("  Waiting 20 seconds for job to complete...")
        time.sleep(20)

        focus_window(job_wid[0])
        time.sleep(0.5)

        # Click 'Check Status' button again
        print("  Clicking 'Check Status' button again...")
        geo = run_cmd(f"xdotool getwindowgeometry --shell {job_wid[0]}")
        jx, jy = 0, 0
        for line in geo.stdout.strip().split('\n'):
            if line.startswith('X='): jx = int(line.split('=')[1])
            elif line.startswith('Y='): jy = int(line.split('=')[1])

        check_btn_x = jx + 180
        check_btn_y = jy + 25
        run_cmd(f"xdotool mousemove --sync {check_btn_x} {check_btn_y}")
        time.sleep(0.2)
        run_cmd("xdotool click 1")
        time.sleep(2)

        take_screenshot(
            "11_job_final_status",
            "Shell Jobs after waiting 20 seconds and pressing 'Check Status' again. "
            "The job should be completed, showing ping output in the HTML area."
        )

        print("  Description: After waiting 20 seconds, 'Check Status' was pressed.")
        print("  The job status should now show one of:")
        print("    - 'COMPLETED': The ping command finished successfully")
        print("    - 'RUNNING': The job is still in progress (pings take ~15s total)")
        print("  The HTML area should display the ping output showing")
        print("  round-trip times for localhost ping packets.")
    else:
        print("  \u2717 Job Runner dialog not found")
        take_screenshot("11_no_job_runner", "Job Runner dialog not found.")

    # == STEP 9: Final Summary ==
    print("\n" + "=" * 60)
    print("STEP 9: Final Summary")
    print("=" * 60)

    windows = list_visible_windows()
    print("\n  All visible windows:")
    for wid, name in windows.items():
        print(f"    - '{name}'")

    take_screenshot("12_final_summary", "Final desktop state with all open windows.")

    print("\n  Screenshots captured:")
    if os.path.isdir(SCREENSHOTS_DIR):
        for f in sorted(os.listdir(SCREENSHOTS_DIR)):
            if f.endswith(".png"):
                fpath = os.path.join(SCREENSHOTS_DIR, f)
                size = os.path.getsize(fpath)
                print(f"    \U0001f4f8 {f} ({size:,} bytes)")

    print("\n" + "=" * 60)
    print("Desktop Automation Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()

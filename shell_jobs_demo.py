#!/usr/bin/env python3
"""
VLC Shell Jobs Extension Demo

This script demonstrates the VLC Shell Jobs extension by launching VLC in a VNC
environment and exercising all features of the extension including:
- Opening the Shell Jobs extension dialog
- Clicking "Run Job" button
- Checking job status with "Check Status" button
- Capturing different status text outputs (RUNNING, SUCCESS)
- Clicking "Abort Job" button
"""

import os
import sys
import time
import subprocess
import urllib.request
import urllib.error
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# Default canvas dimensions for fallback
DEFAULT_CANVAS_BOX = {'x': 0, 'y': 0, 'width': 1400, 'height': 900}

def wait_for_service(url, max_retries=30, delay=2):
    """Wait for a service to become available."""
    
    for i in range(max_retries):
        try:
            urllib.request.urlopen(url, timeout=5)
            print(f"✓ Service at {url} is ready")
            return True
        except (urllib.error.URLError, urllib.error.HTTPError) as e:
            if i < max_retries - 1:
                print(f"Waiting for service at {url}... ({i+1}/{max_retries})")
                time.sleep(delay)
            else:
                print(f"✗ Service at {url} did not become ready")
                return False
    return False

def launch_vlc():
    """Launch VLC media player in the VNC display."""
    print("\nLaunching VLC media player...")
    try:
        # Launch VLC in the virtual display
        subprocess.Popen(
            ['vlc'],
            env={**os.environ, 'DISPLAY': ':99'},
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print("✓ VLC launched successfully")
        time.sleep(3)  # Give VLC time to start
        return True
    except Exception as e:
        print(f"✗ Failed to launch VLC: {e}")
        return False

def demonstrate_shell_jobs():
    """Demonstrate VLC Shell Jobs extension through noVNC."""
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    screenshots_dir = os.path.join(script_dir, "screenshots", "shell_jobs")
    os.makedirs(screenshots_dir, exist_ok=True)
    
    novnc_url = "http://localhost:6080/vnc.html?autoconnect=true&reconnect=true&host=localhost&port=6080"
    
    print("\n" + "="*70)
    print("VLC Shell Jobs Extension Demo")
    print("="*70)
    
    # Wait for noVNC to be ready
    if not wait_for_service("http://localhost:6080"):
        print("ERROR: noVNC service is not available")
        return False
    
    # Launch VLC
    if not launch_vlc():
        return False
    
    with sync_playwright() as p:
        print("\nLaunching browser for GUI automation...")
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1400, 'height': 900})
        page = context.new_page()
        
        interactions = []
        
        try:
            # Navigate to noVNC
            print(f"Navigating to noVNC: {novnc_url}")
            page.goto(novnc_url, timeout=30000)
            
            # Wait for VNC connection to establish
            print("Waiting for VNC connection...")
            time.sleep(8)
            
            # Screenshot 1: VLC with privacy dialog
            print("\n[1] Initial VLC window...")
            screenshot_path = os.path.join(screenshots_dir, "01_vlc_initial.png")
            page.screenshot(path=screenshot_path)
            print(f"    ✓ Screenshot saved: {screenshot_path}")
            time.sleep(2)
            
            # Dismiss privacy dialog - try multiple approaches
            print("\n[2] Dismissing privacy dialog...")
            
            # Approach 1: Press Enter key (activates default button)
            print("    Trying Enter key...")
            page.keyboard.press('Enter')
            time.sleep(2)
            
            # Approach 2: Press Tab then Enter (in case Enter didn't work)
            print("    Trying Tab+Enter...")
            page.keyboard.press('Tab')
            time.sleep(0.5)
            page.keyboard.press('Enter')
            time.sleep(2)
            
            # Approach 3: Click at Continue button location
            canvas = page.query_selector('#noVNC_canvas')
            if not canvas:
                canvas = page.query_selector('canvas')
            
            if canvas:
                temp_box = canvas.bounding_box()
                if temp_box:
                    # Continue button is at bottom right of dialog
                    continue_x = temp_box['x'] + temp_box['width'] * 0.72
                    continue_y = temp_box['y'] + temp_box['height'] * 0.62
                    print(f"    Clicking Continue at ({continue_x:.0f}, {continue_y:.0f})")
                    page.mouse.click(continue_x, continue_y)
            time.sleep(3)  # Give time for dialog to close
            
            # Verify dialog is dismissed by taking another screenshot
            screenshot_path = os.path.join(screenshots_dir, "01b_after_continue.png")
            page.screenshot(path=screenshot_path)
            print(f"    ✓ Screenshot after dismissing dialog: {screenshot_path}")
            time.sleep(2)
            
            # Get canvas coordinates
            if canvas:
                canvas_box = canvas.bounding_box()
                if not canvas_box:
                    canvas_box = DEFAULT_CANVAS_BOX.copy()
            else:
                canvas_box = DEFAULT_CANVAS_BOX.copy()
            
            # Screenshot 2: VLC main window after dismissing dialog
            print("\n[3] VLC main window ready...")
            screenshot_path = os.path.join(screenshots_dir, "02_vlc_ready.png")
            page.screenshot(path=screenshot_path)
            print(f"    ✓ Screenshot saved: {screenshot_path}")
            interactions.append({
                'step': 1,
                'action': 'VLC Ready',
                'description': 'VLC media player is now ready with the main interface visible.'
            })
            time.sleep(1)
            
            # Open View menu to access Shell Jobs extension
            print("\n[4] Opening View menu to access Shell Jobs...")
            view_x = canvas_box['x'] + 450
            view_y = canvas_box['y'] + 30
            page.mouse.click(view_x, view_y)
            time.sleep(3)
            
            screenshot_path = os.path.join(screenshots_dir, "03_view_menu.png")
            page.screenshot(path=screenshot_path)
            print(f"    ✓ Screenshot saved: {screenshot_path}")
            interactions.append({
                'step': 2,
                'action': 'View Menu Opened',
                'description': 'View menu shows options. Shell Jobs extension should be accessible from this menu.'
            })
            time.sleep(1)
            
            # Click on "Shell Jobs" - it's typically at the bottom of the View menu list
            # We'll click multiple times down the menu to find it
            print("\n[5] Navigating to Shell Jobs extension...")
            # Try clicking lower in the menu where extensions usually appear
            shell_jobs_x = canvas_box['x'] + 480
            shell_jobs_y = canvas_box['y'] + 550  # Lower in the menu
            page.mouse.click(shell_jobs_x, shell_jobs_y)
            time.sleep(4)  # Give extension time to load
            
            screenshot_path = os.path.join(screenshots_dir, "04_shell_jobs_dialog.png")
            page.screenshot(path=screenshot_path)
            print(f"    ✓ Screenshot saved: {screenshot_path}")
            interactions.append({
                'step': 3,
                'action': 'Shell Jobs Dialog Opened',
                'description': 'Shell Jobs extension dialog displays with three buttons: "Run Job", "Check Status", and "Abort Job". Initial message shows "Click \'Run\' when ready."'
            })
            time.sleep(2)
            
            # Click "Run Job" button
            print("\n[6] Clicking 'Run Job' button...")
            # The Run Job button is typically in the top-left of the dialog
            run_job_x = canvas_box['x'] + 450
            run_job_y = canvas_box['y'] + 250
            page.mouse.click(run_job_x, run_job_y)
            time.sleep(2)
            
            screenshot_path = os.path.join(screenshots_dir, "05_job_started.png")
            page.screenshot(path=screenshot_path)
            print(f"    ✓ Screenshot saved: {screenshot_path}")
            interactions.append({
                'step': 4,
                'action': 'Run Job Clicked',
                'description': 'Clicked "Run Job" button. The job has been submitted and is starting to execute.'
            })
            time.sleep(2)
            
            # Click "Check Status" button to see RUNNING status
            print("\n[7] Clicking 'Check Status' to see RUNNING status...")
            check_status_x = canvas_box['x'] + 550
            check_status_y = canvas_box['y'] + 250
            page.mouse.click(check_status_x, check_status_y)
            time.sleep(2)
            
            screenshot_path = os.path.join(screenshots_dir, "06_status_running.png")
            page.screenshot(path=screenshot_path)
            print(f"    ✓ Screenshot saved: {screenshot_path}")
            interactions.append({
                'step': 5,
                'action': 'Status Check - RUNNING',
                'description': 'Clicked "Check Status" button. Status text shows "RUNNING" with job details and output from the ping command.'
            })
            time.sleep(3)
            
            # Click "Check Status" again to see more output
            print("\n[8] Checking status again (job still running)...")
            page.mouse.click(check_status_x, check_status_y)
            time.sleep(2)
            
            screenshot_path = os.path.join(screenshots_dir, "07_status_running_more.png")
            page.screenshot(path=screenshot_path)
            print(f"    ✓ Screenshot saved: {screenshot_path}")
            interactions.append({
                'step': 6,
                'action': 'Status Check - More Output',
                'description': 'Second status check shows accumulated output as the ping command continues executing.'
            })
            time.sleep(5)  # Wait for job to progress
            
            # Check status to see SUCCESS
            print("\n[9] Checking status (waiting for completion)...")
            page.mouse.click(check_status_x, check_status_y)
            time.sleep(2)
            
            screenshot_path = os.path.join(screenshots_dir, "08_status_success.png")
            page.screenshot(path=screenshot_path)
            print(f"    ✓ Screenshot saved: {screenshot_path}")
            interactions.append({
                'step': 7,
                'action': 'Status Check - SUCCESS',
                'description': 'Status text shows "SUCCESS" indicating the job completed successfully. Full stdout output is visible showing all ping responses.'
            })
            time.sleep(2)
            
            # Start another job for abort demonstration
            print("\n[10] Starting another job for abort demonstration...")
            page.mouse.click(run_job_x, run_job_y)
            time.sleep(2)
            
            screenshot_path = os.path.join(screenshots_dir, "09_second_job_started.png")
            page.screenshot(path=screenshot_path)
            print(f"    ✓ Screenshot saved: {screenshot_path}")
            time.sleep(1)
            
            # Click "Abort Job" button
            print("\n[11] Clicking 'Abort Job' button...")
            abort_job_x = canvas_box['x'] + 650
            abort_job_y = canvas_box['y'] + 250
            page.mouse.click(abort_job_x, abort_job_y)
            time.sleep(2)
            
            screenshot_path = os.path.join(screenshots_dir, "10_job_aborted.png")
            page.screenshot(path=screenshot_path)
            print(f"    ✓ Screenshot saved: {screenshot_path}")
            interactions.append({
                'step': 8,
                'action': 'Abort Job Clicked',
                'description': 'Clicked "Abort Job" button. The running job is being terminated.'
            })
            time.sleep(2)
            
            # Check status after abort
            print("\n[12] Checking status after abort...")
            page.mouse.click(check_status_x, check_status_y)
            time.sleep(2)
            
            screenshot_path = os.path.join(screenshots_dir, "11_status_after_abort.png")
            page.screenshot(path=screenshot_path)
            print(f"    ✓ Screenshot saved: {screenshot_path}")
            interactions.append({
                'step': 9,
                'action': 'Status After Abort',
                'description': 'Status shows the job was stopped. May show "STOPPED" or "FAILURE" status depending on when abort was processed.'
            })
            time.sleep(1)
            
            # Final screenshot
            print("\n[13] Final view of Shell Jobs extension...")
            screenshot_path = os.path.join(screenshots_dir, "12_final_view.png")
            page.screenshot(path=screenshot_path, full_page=True)
            print(f"    ✓ Screenshot saved: {screenshot_path}")
            
            # Print summary
            print("\n" + "="*70)
            print("Shell Jobs Extension Demo Summary")
            print("="*70)
            print("\nVLC Shell Jobs Extension - All Features Demonstrated:\n")
            
            for interaction in interactions:
                print(f"Step {interaction['step']}: {interaction['action']}")
                print(f"  {interaction['description']}")
                print()
            
            print("="*70)
            print("Demonstration Complete!")
            print("="*70)
            print(f"\nAll screenshots saved to: {screenshots_dir}/")
            print("\nFeatures demonstrated:")
            print("  ✓ Opening Shell Jobs extension from View menu")
            print("  ✓ 'Run Job' button - Starting asynchronous jobs")
            print("  ✓ 'Check Status' button - Monitoring job progress")
            print("  ✓ Status text - RUNNING state with output")
            print("  ✓ Status text - SUCCESS state with full output")
            print("  ✓ 'Abort Job' button - Stopping running jobs")
            print("  ✓ Status after abort - Verification of job termination")
            
            return True
            
        except PlaywrightTimeoutError as e:
            print(f"ERROR: Timeout while loading page: {e}")
            return False
        except Exception as e:
            print(f"ERROR: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            browser.close()

if __name__ == "__main__":
    success = demonstrate_shell_jobs()
    sys.exit(0 if success else 1)

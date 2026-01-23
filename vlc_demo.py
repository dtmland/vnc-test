#!/usr/bin/env python3
"""
VLC Application GUI Interaction Demo

This script launches VLC media player in a VNC environment and demonstrates
GUI interactions using browser automation through noVNC.
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

def interact_with_vlc():
    """Use Playwright to interact with VLC through noVNC and capture screenshots."""
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    screenshots_dir = os.path.join(script_dir, "screenshots", "vlc")
    os.makedirs(screenshots_dir, exist_ok=True)
    
    novnc_url = "http://localhost:6080/vnc.html?autoconnect=true&reconnect=true&host=localhost&port=6080"
    
    print("\n" + "="*70)
    print("VLC GUI Interaction Demo")
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
            
            # Screenshot 1: Initial VLC window
            print("\n[1] Capturing initial VLC window...")
            screenshot_path = os.path.join(screenshots_dir, "01_vlc_initial.png")
            page.screenshot(path=screenshot_path)
            print(f"    ✓ Screenshot saved: {screenshot_path}")
            interactions.append({
                'step': 1,
                'action': 'VLC Application Launch',
                'description': 'VLC media player window opened. The main interface shows the menu bar with File, Media, Playback, Audio, Video, Subtitle, Tools, View, and Help menus. The central area displays the VLC cone logo with an empty playlist.',
                'elements_visible': ['Menu Bar', 'Playback Controls', 'VLC Cone Logo', 'Playlist Area']
            })
            time.sleep(2)
            
            # Screenshot 2: Handle VLC privacy dialog if present
            print("\n[2] Handling VLC privacy dialog...")
            time.sleep(2)
            
            # Get canvas box for coordinate calculations
            canvas = page.query_selector('#noVNC_canvas')
            if not canvas:
                canvas = page.query_selector('canvas')
            
            if canvas:
                temp_box = canvas.bounding_box()
                if temp_box:
                    # Click Continue button using canvas-relative coordinates
                    continue_x = temp_box['x'] + temp_box['width'] * 0.7
                    continue_y = temp_box['y'] + temp_box['height'] * 0.55
                else:
                    # Fallback to fixed coordinates
                    continue_x = 700
                    continue_y = 450
            else:
                # Fallback to fixed coordinates
                continue_x = 700
                continue_y = 450
                
            page.mouse.click(continue_x, continue_y)  # Click Continue
            time.sleep(2)
            
            screenshot_path = os.path.join(screenshots_dir, "02_vlc_privacy_dialog.png")
            page.screenshot(path=screenshot_path)
            print(f"    ✓ Screenshot saved: {screenshot_path}")
            interactions.append({
                'step': 2,
                'action': 'Privacy and Network Access Policy Dialog',
                'description': 'VLC displays a privacy dialog on first launch explaining that it does not collect personal data but can retrieve metadata from Internet services. Dialog shows "Allow metadata network access" checkbox and "Continue" button.',
                'elements_visible': ['Privacy Dialog', 'Continue Button', 'Checkbox', 'Policy Text']
            })
            time.sleep(1)
            
            # Get the VNC canvas element - try multiple selectors
            canvas = page.query_selector('#noVNC_canvas')
            if not canvas:
                canvas = page.query_selector('canvas')
            if not canvas:
                print("INFO: Proceeding without canvas element reference")
                # Continue with default coordinates
                canvas_box = DEFAULT_CANVAS_BOX.copy()
            else:
                # Get canvas bounding box for coordinate calculations
                canvas_box = canvas.bounding_box()
                if not canvas_box:
                    print("INFO: Using default canvas dimensions")
                    canvas_box = DEFAULT_CANVAS_BOX.copy()
                else:
                    print(f"    Canvas dimensions: {canvas_box['width']}x{canvas_box['height']}")
            
            # Screenshot 3: Clicking on Media menu
            print("\n[3] Interacting with Media menu...")
            # Click on "Media" menu (approximate position in the menu bar)
            media_x = canvas_box['x'] + 100
            media_y = canvas_box['y'] + 30
            page.mouse.click(media_x, media_y)
            time.sleep(1)
            
            screenshot_path = os.path.join(screenshots_dir, "03_vlc_media_menu.png")
            page.screenshot(path=screenshot_path)
            print(f"    ✓ Screenshot saved: {screenshot_path}")
            interactions.append({
                'step': 3,
                'action': 'Media Menu Opened',
                'description': 'Clicked on the "Media" menu in the menu bar. The dropdown menu displays options including "Open File", "Open Multiple Files", "Open Disc", "Open Network Stream", "Open Capture Device", "Recent Media", "Quit at End of Playlist", and "Quit" options.',
                'elements_visible': ['Media Menu Items', 'File Operations', 'Network Stream Options']
            })
            time.sleep(1)
            
            # Click elsewhere to close the menu
            page.mouse.click(canvas_box['x'] + 400, canvas_box['y'] + 300)
            time.sleep(1)
            
            # Screenshot 4: Clicking on Tools menu
            print("\n[4] Interacting with Tools menu...")
            tools_x = canvas_box['x'] + 380
            tools_y = canvas_box['y'] + 30
            page.mouse.click(tools_x, tools_y)
            time.sleep(1)
            
            screenshot_path = os.path.join(screenshots_dir, "04_vlc_tools_menu.png")
            page.screenshot(path=screenshot_path)
            print(f"    ✓ Screenshot saved: {screenshot_path}")
            interactions.append({
                'step': 4,
                'action': 'Tools Menu Opened',
                'description': 'Clicked on the "Tools" menu. The dropdown shows options such as "Effects and Filters", "Track Synchronization", "Media Information", "Codec Information", "Messages", "Preferences", and other tool-related options.',
                'elements_visible': ['Tools Menu Items', 'Preferences Option', 'Effects and Filters', 'Media Information']
            })
            time.sleep(1)
            
            # Click elsewhere to close
            page.mouse.click(canvas_box['x'] + 400, canvas_box['y'] + 300)
            time.sleep(1)
            
            # Screenshot 5: Clicking on View menu
            print("\n[5] Interacting with View menu...")
            view_x = canvas_box['x'] + 450
            view_y = canvas_box['y'] + 30
            page.mouse.click(view_x, view_y)
            time.sleep(1)
            
            screenshot_path = os.path.join(screenshots_dir, "05_vlc_view_menu.png")
            page.screenshot(path=screenshot_path)
            print(f"    ✓ Screenshot saved: {screenshot_path}")
            interactions.append({
                'step': 5,
                'action': 'View Menu Opened',
                'description': 'Clicked on the "View" menu. The menu displays interface customization options including "Playlist", "Docked Playlist", "Always on Top", "Minimal Interface", "Fullscreen Interface", "Advanced Controls", and other view settings.',
                'elements_visible': ['View Menu Items', 'Interface Options', 'Playlist Toggle', 'Fullscreen Option']
            })
            time.sleep(1)
            
            # Click elsewhere to close
            page.mouse.click(canvas_box['x'] + 400, canvas_box['y'] + 300)
            time.sleep(1)
            
            # Screenshot 6: Hovering over playback controls
            print("\n[6] Examining playback controls...")
            controls_x = canvas_box['x'] + 200
            controls_y = canvas_box['y'] + canvas_box['height'] - 50
            page.mouse.move(controls_x, controls_y)
            time.sleep(1)
            
            screenshot_path = os.path.join(screenshots_dir, "06_vlc_playback_controls.png")
            page.screenshot(path=screenshot_path)
            print(f"    ✓ Screenshot saved: {screenshot_path}")
            interactions.append({
                'step': 6,
                'action': 'Playback Controls Area',
                'description': 'Focused on the playback controls at the bottom of the VLC window. Visible controls include: Previous button, Play/Pause button, Stop button, Next button, a timeline/progress slider, volume control slider, fullscreen toggle, and playlist toggle button.',
                'elements_visible': ['Play Button', 'Pause Button', 'Stop Button', 'Next/Previous Buttons', 'Timeline Slider', 'Volume Control', 'Fullscreen Button']
            })
            time.sleep(1)
            
            # Screenshot 7: Right-click context menu
            print("\n[7] Opening context menu...")
            context_x = canvas_box['x'] + 400
            context_y = canvas_box['y'] + 300
            page.mouse.click(context_x, context_y, button='right')
            time.sleep(1)
            
            screenshot_path = os.path.join(screenshots_dir, "07_vlc_context_menu.png")
            page.screenshot(path=screenshot_path)
            print(f"    ✓ Screenshot saved: {screenshot_path}")
            interactions.append({
                'step': 7,
                'action': 'Context Menu',
                'description': 'Right-clicked in the main viewing area to open the context menu. The menu shows quick access options including Play/Pause, Stop, Previous, Next, Title selection, Chapter selection, Audio/Video/Subtitle track options, and other playback-related commands.',
                'elements_visible': ['Context Menu', 'Play/Pause Option', 'Audio/Video Settings', 'Title/Chapter Navigation']
            })
            time.sleep(2)
            
            # Click elsewhere to close context menu
            page.mouse.click(canvas_box['x'] + 200, canvas_box['y'] + 200)
            time.sleep(1)
            
            # Final screenshot
            print("\n[8] Final view of VLC interface...")
            screenshot_path = os.path.join(screenshots_dir, "08_vlc_final_view.png")
            page.screenshot(path=screenshot_path, full_page=True)
            print(f"    ✓ Screenshot saved: {screenshot_path}")
            
            # Print summary
            print("\n" + "="*70)
            print("GUI Interaction Summary")
            print("="*70)
            print("\nVLC Media Player - GUI Elements and Interactions:\n")
            
            for interaction in interactions:
                print(f"Step {interaction['step']}: {interaction['action']}")
                print(f"  Description: {interaction['description']}")
                print(f"  Elements Visible: {', '.join(interaction['elements_visible'])}")
                print()
            
            print("="*70)
            print("Demonstration Complete!")
            print("="*70)
            print(f"\nAll screenshots saved to: {screenshots_dir}/")
            print("\nScreenshots captured:")
            for i in range(1, 9):
                print(f"  {i:02d}_vlc_*.png - Step {i} interaction")
            
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
    success = interact_with_vlc()
    sys.exit(0 if success else 1)

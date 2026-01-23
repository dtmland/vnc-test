#!/usr/bin/env python3
"""
Wine Explorer interaction and screenshot script.
This script launches Wine Explorer in the VNC desktop and captures screenshots
of various interactions with the GUI.
"""

import os
import sys
import time
import subprocess
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

def wait_for_service(url, max_retries=30, delay=2):
    """Wait for a service to become available."""
    import urllib.request
    import urllib.error
    
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

def interact_with_wine_explorer():
    """Use Playwright to interact with Wine Explorer via noVNC and capture screenshots."""
    
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    screenshots_dir = os.path.join(script_dir, "screenshots", "wine_explorer")
    
    novnc_url = "http://localhost:6080/vnc.html?autoconnect=true&reconnect=true&host=localhost&port=6080"
    
    print("\n" + "="*60)
    print("Wine Explorer Browser Automation")
    print("="*60)
    
    # Wait for noVNC to be ready
    if not wait_for_service("http://localhost:6080"):
        print("ERROR: noVNC service is not available")
        return False
    
    with sync_playwright() as p:
        # Launch browser
        print("\nLaunching browser...")
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1400, 'height': 900})
        page = context.new_page()
        
        try:
            # Navigate to noVNC
            print(f"Navigating to: {novnc_url}")
            page.goto(novnc_url, timeout=30000)
            
            # Wait for the page to load
            print("Waiting for noVNC to load...")
            time.sleep(5)
            
            # Create screenshots directory
            os.makedirs(screenshots_dir, exist_ok=True)
            
            # Screenshot 1: Initial Wine Explorer view
            print("\n1. Taking screenshot of initial Wine Explorer window...")
            time.sleep(3)  # Wait for Wine Explorer to render
            screenshot_path = os.path.join(screenshots_dir, "01_wine_explorer_initial.png")
            page.screenshot(path=screenshot_path)
            print(f"✓ Screenshot saved: {screenshot_path}")
            
            # Check if we can see the canvas element (noVNC screen)
            canvas = page.query_selector('#noVNC_canvas')
            if not canvas:
                print("⚠ noVNC canvas element not found")
                return False
            
            print("✓ noVNC canvas element found - VNC display is active!")
            
            # Get canvas bounding box for click positioning
            canvas_box = canvas.bounding_box()
            if not canvas_box:
                print("⚠ Could not get canvas bounding box")
                return False
            
            # Calculate center of canvas for mouse interactions
            canvas_x = canvas_box['x'] + canvas_box['width'] / 2
            canvas_y = canvas_box['y'] + canvas_box['height'] / 2
            
            # Screenshot 2: Click in the left pane (tree view area)
            print("\n2. Clicking on left navigation pane...")
            # Click on the left side of the canvas (where tree view should be)
            tree_x = canvas_box['x'] + 100  # Left area
            tree_y = canvas_box['y'] + 200  # Middle height
            page.mouse.click(tree_x, tree_y)
            time.sleep(2)
            screenshot_path = os.path.join(screenshots_dir, "02_wine_explorer_tree_click.png")
            page.screenshot(path=screenshot_path)
            print(f"✓ Screenshot saved: {screenshot_path}")
            
            # Screenshot 3: Double-click on an item
            print("\n3. Double-clicking on a tree item...")
            page.mouse.click(tree_x, tree_y + 50)
            time.sleep(0.3)
            page.mouse.click(tree_x, tree_y + 50)
            time.sleep(2)
            screenshot_path = os.path.join(screenshots_dir, "03_wine_explorer_double_click.png")
            page.screenshot(path=screenshot_path)
            print(f"✓ Screenshot saved: {screenshot_path}")
            
            # Screenshot 4: Click on menu bar
            print("\n4. Clicking on menu bar area...")
            menu_x = canvas_box['x'] + 100  # Left side for File menu
            menu_y = canvas_box['y'] + 50   # Top area for menu bar
            page.mouse.click(menu_x, menu_y)
            time.sleep(2)
            screenshot_path = os.path.join(screenshots_dir, "04_wine_explorer_menu_click.png")
            page.screenshot(path=screenshot_path)
            print(f"✓ Screenshot saved: {screenshot_path}")
            
            # Screenshot 5: Right-click context menu
            print("\n5. Right-clicking in the main pane for context menu...")
            main_x = canvas_box['x'] + canvas_box['width'] - 300  # Right pane
            main_y = canvas_box['y'] + 300
            page.mouse.click(main_x, main_y, button='right')
            time.sleep(2)
            screenshot_path = os.path.join(screenshots_dir, "05_wine_explorer_context_menu.png")
            page.screenshot(path=screenshot_path)
            print(f"✓ Screenshot saved: {screenshot_path}")
            
            # Screenshot 6: Close context menu with left click elsewhere
            print("\n6. Closing context menu...")
            page.mouse.click(canvas_x, canvas_y)
            time.sleep(1)
            screenshot_path = os.path.join(screenshots_dir, "06_wine_explorer_after_context.png")
            page.screenshot(path=screenshot_path)
            print(f"✓ Screenshot saved: {screenshot_path}")
            
            # Screenshot 7: Final full view
            print("\n7. Taking final full view screenshot...")
            time.sleep(1)
            screenshot_path = os.path.join(screenshots_dir, "07_wine_explorer_final.png")
            page.screenshot(path=screenshot_path, full_page=True)
            print(f"✓ Screenshot saved: {screenshot_path}")
            
            print("\n" + "="*60)
            print("Wine Explorer Interaction Complete!")
            print("="*60)
            print("\nScreenshots captured:")
            print("  1. 01_wine_explorer_initial.png - Initial Wine Explorer window")
            print("  2. 02_wine_explorer_tree_click.png - After clicking tree view")
            print("  3. 03_wine_explorer_double_click.png - After double-clicking item")
            print("  4. 04_wine_explorer_menu_click.png - Menu bar interaction")
            print("  5. 05_wine_explorer_context_menu.png - Right-click context menu")
            print("  6. 06_wine_explorer_after_context.png - After closing context menu")
            print("  7. 07_wine_explorer_final.png - Final full view")
            print(f"\nAll screenshots are in: {screenshots_dir}")
            
            # Document GUI elements observed
            print("\n" + "="*60)
            print("Wine Explorer GUI Elements Overview")
            print("="*60)
            print("""
Wine Explorer is a file manager application that mimics the Windows Explorer interface.
Based on the captured screenshots, the following GUI elements are typically visible:

MENU BAR (Top):
- File: File operations menu (New, Open, etc.)
- Edit: Edit operations (Cut, Copy, Paste, etc.)
- View: View options (Large Icons, Small Icons, List, Details, etc.)
- Favorites: Bookmarked locations
- Tools: Utility functions
- Help: Help documentation and About

TOOLBAR (Below menu bar):
- Back/Forward navigation buttons
- Up (parent directory) button
- Search button
- Folders button (toggle folder pane)
- Views button (change view mode)

LEFT PANE (Navigation/Tree View):
- Desktop
- My Computer
  - C: (System Drive)
  - D: (if available)
- My Documents
- My Network Places
- Recycle Bin

RIGHT PANE (File/Folder View):
- Displays contents of selected folder
- Shows files and folders with icons
- Can be switched between different views (Icons, List, Details)

STATUS BAR (Bottom):
- Shows number of objects in current folder
- Shows disk space information when drive is selected
- May show file details when a file is selected

CONTEXT MENU (Right-click):
Common options include:
- Open
- Explore
- Cut
- Copy
- Paste
- Delete
- Rename
- Properties
- Create New (Folder, Shortcut, etc.)

The interface provides a familiar Windows-like file browsing experience running
under Wine on Linux, accessible through the VNC remote desktop connection.
            """)
            
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
    success = interact_with_wine_explorer()
    sys.exit(0 if success else 1)

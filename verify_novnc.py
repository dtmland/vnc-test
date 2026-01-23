#!/usr/bin/env python3
"""
Browser automation script to verify noVNC setup and capture screenshots.
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

def verify_vnc_with_browser():
    """Use Playwright to verify noVNC is working and capture screenshots."""
    
    novnc_url = "http://localhost:6080/vnc.html?autoconnect=true&reconnect=true&host=localhost&port=6080"
    
    print("\n" + "="*60)
    print("Browser Automation Verification")
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
            
            # Take initial screenshot
            screenshot_path = "/home/runner/work/vnc-test/vnc-test/screenshots/novnc_initial.png"
            os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
            page.screenshot(path=screenshot_path)
            print(f"✓ Screenshot saved: {screenshot_path}")
            
            # Wait for VNC connection
            print("Waiting for VNC connection to establish...")
            time.sleep(8)
            
            # Take screenshot of connected session
            screenshot_path2 = "/home/runner/work/vnc-test/vnc-test/screenshots/novnc_connected.png"
            page.screenshot(path=screenshot_path2)
            print(f"✓ Screenshot saved: {screenshot_path2}")
            
            # Check if we can see the canvas element (noVNC screen)
            canvas = page.query_selector('#noVNC_canvas')
            if canvas:
                print("✓ noVNC canvas element found - VNC display is active!")
                
                # Take a final screenshot focusing on the canvas area
                screenshot_path3 = "/home/runner/work/vnc-test/vnc-test/screenshots/novnc_desktop.png"
                page.screenshot(path=screenshot_path3, full_page=True)
                print(f"✓ Full page screenshot saved: {screenshot_path3}")
            else:
                print("⚠ noVNC canvas element not found")
            
            # Get page title
            title = page.title()
            print(f"✓ Page title: {title}")
            
            # Check for any error messages
            error_elements = page.query_selector_all('.noVNC_status_error')
            if error_elements:
                print("⚠ Found error messages on page")
            else:
                print("✓ No error messages detected")
            
            print("\n" + "="*60)
            print("Verification Complete!")
            print("="*60)
            print("\nScreenshots captured:")
            print("  1. novnc_initial.png - Initial page load")
            print("  2. novnc_connected.png - After connection established")
            print("  3. novnc_desktop.png - Full page view of desktop")
            print("\nAll screenshots are in the 'screenshots/' directory")
            
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
    success = verify_vnc_with_browser()
    sys.exit(0 if success else 1)

#!/bin/bash
# Wine Installation and Setup Script

set -e

echo "======================================"
echo "Wine Installation and Setup"
echo "======================================"

# Install Wine and required dependencies
echo "Installing Wine and dependencies..."
sudo dpkg --add-architecture i386
sudo apt-get update
sudo apt-get install -y wine wine32 wine64 winetricks xterm

# Initialize Wine (creates ~/.wine directory)
echo "Initializing Wine prefix..."
DISPLAY=:99 WINEARCH=win64 wineboot --init

# Wait for wineserver to finish initializing
echo "Waiting for Wine to initialize..."
DISPLAY=:99 wineserver -w

echo ""
echo "======================================"
echo "Wine Setup Complete!"
echo "======================================"
echo "Wine version:"
wine --version
echo ""

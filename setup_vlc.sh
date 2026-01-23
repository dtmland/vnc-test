#!/bin/bash
# VLC Installation and Setup Script

set -e

echo "======================================"
echo "Installing VLC Media Player"
echo "======================================"

# Update package lists
echo "Updating package lists..."
sudo apt-get update -qq

# Install VLC
echo "Installing VLC and dependencies..."
sudo apt-get install -y vlc vlc-plugin-base xterm

echo ""
echo "======================================"
echo "VLC Installation Complete!"
echo "======================================"
echo ""
echo "VLC version:"
vlc --version | head -n 1

echo ""
echo "Ready to run VLC demo!"

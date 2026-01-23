# Rocky Linux VNC Server Setup

This directory contains Rocky Linux versions of the VNC server setup scripts.

## Quick Start

### Using Docker (Recommended)

```bash
# Build the Rocky Linux image
docker build -f Dockerfile.rocky -t vnc-rocky .

# Run the container
docker run -p 6080:6080 -p 5999:5999 vnc-rocky

# Or use docker-compose
docker-compose -f docker-compose.rocky.yml up
```

Then open your browser to: http://localhost:6080/vnc.html?autoconnect=true

### Manual Installation on Rocky Linux

```bash
# Install EPEL repository (required for additional packages)
sudo dnf install -y epel-release

# Install VNC server components
sudo dnf install -y \
    xorg-x11-server-Xvfb \
    x11vnc \
    fluxbox \
    xterm \
    python3 \
    python3-pip \
    git \
    novnc

# Install Playwright for browser automation
pip3 install playwright
python3 -m playwright install chromium
python3 -m playwright install-deps chromium

# Run the test
./run_test_rocky.sh
```

## Files

- **Dockerfile.rocky** - Rocky Linux 9 container definition
- **setup_vnc_rocky.sh** - Script to start VNC server stack on Rocky Linux
- **run_test_rocky.sh** - Full test suite runner for Rocky Linux
- **docker-compose.rocky.yml** - Docker Compose configuration

## Package Differences from Ubuntu

Rocky Linux uses different package names compared to Ubuntu/Debian:

| Component | Ubuntu/Debian | Rocky Linux |
|-----------|---------------|-------------|
| Virtual X Server | `xvfb` | `xorg-x11-server-Xvfb` |
| Package Manager | `apt-get` | `dnf` |
| Extra Packages | N/A | Requires EPEL repository |
| Python Deps | Auto-installed | Need `playwright install-deps` |

## Port Configuration

Both versions use the same ports:
- **5999** - VNC server port
- **6080** - noVNC web interface port

## Architecture

The Rocky Linux version follows the same architecture as the Ubuntu version:

```
Browser → noVNC (port 6080) → x11vnc (port 5999) → Xvfb (display :99)
```

## Troubleshooting

### Docker Build Fails with Network Error

If you encounter network/DNS errors when building:
```bash
# Check DNS resolution
ping mirrors.rockylinux.org

# May need to configure Docker DNS or use a proxy
```

### noVNC Not Starting

Check if noVNC is installed:
```bash
ls -la /usr/share/novnc
```

On most distributions including Ubuntu and Rocky Linux, noVNC is typically installed to `/usr/share/novnc`. However, if you installed from source or a different package, verify the path:
```bash
# Find noVNC installation
find /usr -name "novnc_proxy" 2>/dev/null
```

Update the `setup_vnc_rocky.sh` script if your installation path differs.

## Verification

The `run_test_rocky.sh` script includes automated verification using Playwright:
1. Starts the VNC server stack
2. Launches a headless browser
3. Connects to noVNC interface
4. Captures screenshots
5. Verifies the connection
6. Cleans up all services

Screenshots are saved to the `screenshots/` directory.

## Notes

- The terminal title shows "VNC Test Terminal - Rocky Linux" to distinguish from Ubuntu
- All scripts use the same display (:99), VNC port (5999), and noVNC port (6080)
- The verification script (verify_novnc.py) is shared between both versions

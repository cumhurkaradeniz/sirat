#!/usr/bin/env bash
set -e

echo "☪ Installing Sirat v1.1.0..."

if command -v apt-get >/dev/null 2>&1; then
    sudo apt-get update
    sudo apt-get install -y python3 python3-pyqt5 python3-pyqt5.qtmultimedia libqt5multimedia5-plugins libnotify-bin
elif command -v dnf >/dev/null 2>&1; then
    sudo dnf install -y python3 python3-qt5 qt5-qtmultimedia gstreamer1-plugins-good libnotify
elif command -v pacman >/dev/null 2>&1; then
    sudo pacman -Sy --noconfirm python python-pyqt5 qt5-multimedia gst-plugins-good libnotify
elif command -v zypper >/dev/null 2>&1; then
    sudo zypper install -y python3 python3-qt5 libQt5Multimedia5 gst-plugins-good libnotify-tools
else
    echo "⚠️ Package manager not detected. Ensure Python 3 and PyQt5 + QtMultimedia are installed."
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

sudo rm -rf /usr/local/share/sirat
sudo mkdir -p /usr/local/share/sirat /usr/local/bin /usr/local/share/applications /usr/local/share/icons/hicolor/256x256/apps

sudo cp -r "$SCRIPT_DIR"/{app.py,icon.png,modules,data,locales} /usr/local/share/sirat/
sudo cp -f "$SCRIPT_DIR/icon.png" /usr/local/share/icons/hicolor/256x256/apps/sirat.png

sudo tee /usr/local/bin/sirat >/dev/null << 'RUN'
#!/usr/bin/env bash
exec python3 /usr/local/share/sirat/app.py "$@"
RUN
sudo chmod +x /usr/local/bin/sirat

sudo tee /usr/local/share/applications/sirat.desktop >/dev/null << 'DESK'
[Desktop Entry]
Name=Sirat
Comment=Universal Islamic Companion for Linux
Exec=/usr/local/bin/sirat
Icon=sirat
Terminal=false
Type=Application
Categories=Utility;Education;
StartupWMClass=sirat
DESK

sudo gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
echo "✅ Sirat installed successfully! You can launch it from your application menu or run 'sirat'."

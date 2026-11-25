#!/bin/bash
set -e
mkdir -p pkg/DEBIAN pkg/usr/share/sirat pkg/usr/share/applications pkg/usr/bin pkg/usr/share/icons/hicolor/256x256/apps
cp -r app.py icon.png modules data pkg/usr/share/sirat/
cp icon.png pkg/usr/share/icons/hicolor/256x256/apps/sirat.png
cat << 'CTRL' > pkg/DEBIAN/control
Package: sirat
Version: 1.0.0
Section: utils
Priority: optional
Architecture: all
Depends: python3, python3-pyqt5, python3-pyqt5.qtmultimedia, libqt5multimedia5-plugins
Maintainer: Cumhur Karadeniz <cumhurkaradeniz@github.com>
Description: Lightweight and modern Islamic Companion for Linux (Prayer Times, Quran, Hadith, Guide)
CTRL
printf '#!/bin/bash\nexec python3 /usr/share/sirat/app.py "$@"\n' > pkg/usr/bin/sirat && chmod +x pkg/usr/bin/sirat
cat << 'DSK' > pkg/usr/share/applications/sirat.desktop
[Desktop Entry]
Name=Sirat
Comment=Universal Islamic Companion for Linux
Exec=sirat
Icon=sirat
Terminal=false
Type=Application
Categories=Utility;Education;
StartupWMClass=sirat
DSK
dpkg-deb --root-owner-group --build pkg sirat_1.0.0_all.deb && rm -rf pkg

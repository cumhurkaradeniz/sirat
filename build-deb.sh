#!/bin/bash
set -e

rm -rf pkg sirat_1.1.0_all.deb

mkdir -p pkg/DEBIAN \
         pkg/usr/share/sirat \
         pkg/usr/share/applications \
         pkg/usr/bin \
         pkg/usr/share/icons/hicolor/256x256/apps \
         pkg/usr/share/icons/hicolor/scalable/apps

cp -r app.py icon.png modules data locales pkg/usr/share/sirat/
find pkg/usr/share/sirat -type d -name "__pycache__" -exec rm -rf {} +
chmod -R a+rX pkg/usr/share/sirat

cp icon.png pkg/usr/share/icons/hicolor/256x256/apps/sirat.png
if [ -f icon.svg ]; then
    cp icon.svg pkg/usr/share/icons/hicolor/scalable/apps/sirat.svg
fi

SIZE=$(du -sk pkg/usr | cut -f1)

cat << CTRL > pkg/DEBIAN/control
Package: sirat
Version: 1.1.0
Section: utils
Priority: optional
Architecture: all
Installed-Size: ${SIZE}
Depends: python3, python3-pyqt5, python3-pyqt5.qtmultimedia, libqt5multimedia5-plugins, libnotify-bin, pulseaudio-utils | pipewire-bin | alsa-utils
Maintainer: Cumhur Karadeniz <cumhurkaradeniz@github.com>
Description: Lightweight and modern Islamic Companion for Linux
 Sirat is a free, open-source Islamic companion application for Linux
 featuring accurate prayer times, adhan notifications, Quran reader,
 Hadith collection, Islamic days, guide, and digital dhikr counter.
CTRL

printf '#!/bin/bash\nexec python3 /usr/share/sirat/app.py "$@"\n' > pkg/usr/bin/sirat
chmod 755 pkg/usr/bin/sirat

cat << 'DSK' > pkg/usr/share/applications/sirat.desktop
[Desktop Entry]
Name=Sirat
GenericName=Islamic Companion
Comment=Universal Islamic Companion for Linux
Exec=sirat
Icon=sirat
Terminal=false
Type=Application
Categories=Utility;Education;
Keywords=Islam;Prayer;Quran;Hadith;Adhan;Namaz;
StartupWMClass=sirat
DSK

dpkg-deb --root-owner-group --build pkg sirat_1.1.0_all.deb
rm -rf pkg
echo "✅ sirat_1.1.0_all.deb başarıyla derlendi!"

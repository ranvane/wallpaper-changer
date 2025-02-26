#!/bin/bash

# 设置版本号变量
VERSION="1.0.0"

# 设置包名变量
PACKAGE_NAME="wallpaper-changer"

# 创建完整的包名
FULL_PACKAGE_NAME="${PACKAGE_NAME}_${VERSION}"

# build deb package
# 创建 Debian 包目录结构
mkdir -p ${FULL_PACKAGE_NAME}/DEBIAN
mkdir -p ${FULL_PACKAGE_NAME}/usr/local/bin
mkdir -p ${FULL_PACKAGE_NAME}/usr/share/applications
mkdir -p ${FULL_PACKAGE_NAME}/usr/share/${PACKAGE_NAME}

# 复制文件到相应目录
cp main_app.py ${FULL_PACKAGE_NAME}/usr/local/bin/wallpaper-changer.py
cp Bing_Wallpaper_changer_UI.py ${FULL_PACKAGE_NAME}/usr/local/bin/Bing_Wallpaper_changer_UI.py
cp icon.png ${FULL_PACKAGE_NAME}/usr/share/${PACKAGE_NAME}/
cp -r resources ${FULL_PACKAGE_NAME}/usr/share/${PACKAGE_NAME}/

# 创建 DEBIAN/control 文件
cat > ${FULL_PACKAGE_NAME}/DEBIAN/control << EOL
Package: ${PACKAGE_NAME}
Version: ${VERSION}
Section: graphics
Priority: optional
Architecture: all
Depends: python3 (>= 3.6), python3-wxgtk4.0
Maintainer: ranvane <ranvane@gmail.com>
Description: Wallpaper Changer
 A simple application to change wallpapers automatically
 using images from Bing.
EOL

# 创建桌面启动文件
cat > ${FULL_PACKAGE_NAME}/usr/share/applications/${PACKAGE_NAME}.desktop << EOL
[Desktop Entry]
Name=Wallpaper Changer
Exec=python /usr/local/bin/wallpaper-changer.py
Icon=/usr/share/${PACKAGE_NAME}/icon.png
Type=Application
Categories=Graphics;Utility;
EOL

# 创建 postinst 脚本（安装后执行）：
cat > ${FULL_PACKAGE_NAME}/DEBIAN/postinst << EOL
#!/bin/sh
chmod +x /usr/local/bin/wallpaper-changer.py
update-desktop-database
EOL

chmod +x ${FULL_PACKAGE_NAME}/DEBIAN/postinst

# 创建 prerm 脚本（卸载前执行）：
cat > ${FULL_PACKAGE_NAME}/DEBIAN/prerm << EOL
#!/bin/sh
update-desktop-database
EOL
chmod +x ${FULL_PACKAGE_NAME}/DEBIAN/prerm

# 创建 postrm 脚本（卸载后执行）：
cat > ${FULL_PACKAGE_NAME}/DEBIAN/postrm << EOL
#!/bin/sh
update-desktop-database
EOL
chmod +x ${FULL_PACKAGE_NAME}/DEBIAN/postrm

# 构建 Debian 包
dpkg-deb --build ${FULL_PACKAGE_NAME}

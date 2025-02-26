#!/bin/bash
#
# build deb package
#创建 Debian 包目录结构
mkdir -p wallpaper-changer_1.0-1/DEBIAN
mkdir -p wallpaper-changer_1.0-1/usr/local/bin
mkdir -p wallpaper-changer_1.0-1/usr/share/applications
mkdir -p wallpaper-changer_1.0-1/usr/share/wallpaper-changer

# 复制文件到相应目录
cp main_app.py wallpaper-changer_1.0-1/usr/local/bin/wallpaper-changer.py
cp Bing_Wallpaper_changer_UI.py wallpaper-changer_1.0-1/usr/local/bin/Bing_Wallpaper_changer_UI.py
cp icon.png wallpaper-changer_1.0-1/usr/share/wallpaper-changer/
cp -r resources wallpaper-changer_1.0-1/usr/share/wallpaper-changer/

# 创建 DEBIAN/control 文件
cat > wallpaper-changer_1.0-1/DEBIAN/control << EOL
Package: wallpaper-changer
Version: 1.0-1
Section: graphics
Priority: optional
Architecture: all
Depends: python3 (>= 3.6), python3-wxgtk4.0
Maintainer: ranvane <ranvane@gmail.com>
Description: Wallpaper Changer
 A simple application to change wallpapers automatically
 using images from Bing.
EOL

#创建桌面启动文件
cat > wallpaper-changer_1.0-1/usr/share/applications/wallpaper-changer.desktop << EOL
[Desktop Entry]
Name=Wallpaper Changer
Exec=python /usr/local/bin/wallpaper-changer.py
Icon=/usr/share/wallpaper-changer/icon.png
Type=Application
Categories=Graphics;Utility;
EOL

# 创建 postinst 脚本（安装后执行）：

cat > wallpaper-changer_1.0-1/DEBIAN/postinst << EOL
#!/bin/sh
chmod +x /usr/local/bin/wallpaper-changer.py
update-desktop-database
EOL

chmod +x wallpaper-changer_1.0-1/DEBIAN/postinst

# 创建 prerm 脚本（卸载前执行）：
cat > wallpaper-changer_1.0-1/DEBIAN/prerm << EOL
#!/bin/sh
update-desktop-database
EOL
chmod +x wallpaper-changer_1.0-1/DEBIAN/prerm

# 创建 postrm 脚本（卸载后执行）：
cat > wallpaper-changer_1.0-1/DEBIAN/postrm << EOL
#!/bin/sh
update-desktop-database
EOL
chmod +x wallpaper-changer_1.0-1/DEBIAN/postrm
# 构建 Debian 包
dpkg-deb --build wallpaper-changer_1.0-1
#!/bin/bash

# 设置版本号变量
VERSION="2.0.0"

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
cp main_app.py                    ${FULL_PACKAGE_NAME}/usr/local/bin/wallpaper-changer.py
cp Wallpaper_changer_UI.py        ${FULL_PACKAGE_NAME}/usr/local/bin/Wallpaper_changer_UI.py
cp ConfigMixin.py                 ${FULL_PACKAGE_NAME}/usr/local/bin/ConfigMixin.py
cp WallpaperChangerTaskBarIcon.py ${FULL_PACKAGE_NAME}/usr/local/bin/WallpaperChangerTaskBarIcon.py
cp my_logger.py                   ${FULL_PACKAGE_NAME}/usr/local/bin/my_logger.py
cp WallpaperProcessor.py          ${FULL_PACKAGE_NAME}/usr/local/bin/WallpaperProcessor.py
cp DownloadProcessor.py           ${FULL_PACKAGE_NAME}/usr/local/bin/DownloadProcessor.py
cp YearMonthPicker.py             ${FULL_PACKAGE_NAME}/usr/local/bin/YearMonthPicker.py
cp icon.png                       ${FULL_PACKAGE_NAME}/usr/share/${PACKAGE_NAME}/
cp -r resources                   ${FULL_PACKAGE_NAME}/usr/share/${PACKAGE_NAME}/

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
# cat > ${FULL_PACKAGE_NAME}/DEBIAN/prerm << EOL
# #!/bin/sh
# update-desktop-database
# EOL
# chmod +x ${FULL_PACKAGE_NAME}/DEBIAN/prerm

# 创建 postrm 脚本（卸载后执行）：
cat > ${FULL_PACKAGE_NAME}/DEBIAN/postrm << EOL
#!/bin/sh
set -e

remove_user_files() {
    user="\$1"
    home_dir=\$(getent passwd "\$user" | cut -d: -f6)
    
    if [ -d "\$home_dir" ]; then
        # 删除配置目录
        config_dir="\$home_dir/.config/${PACKAGE_NAME}"
        if [ -d "\$config_dir" ]; then
            rm -rf "\$config_dir"
            echo "Removed config directory: \$config_dir"
        fi

        # 删除自启动文件
        autostart_file="\$home_dir/.config/autostart/${PACKAGE_NAME}.desktop"
        if [ -f "\$autostart_file" ]; then
            rm -f "\$autostart_file"
            echo "Removed autostart file: \$autostart_file"
        fi
    fi
}

case "\$1" in
    purge|remove|abort-install|abort-upgrade|disappear)
        # 对所有用户执行清理操作
        for user in \$(getent passwd | cut -d: -f1); do
            if [ "\$user" != "root" ] && [ -d "/home/\$user" ]; then
                remove_user_files "\$user"
            fi
        done

        # 删除系统级目录
        if [ -d "/usr/share/${PACKAGE_NAME}" ]; then
            rm -rf /usr/share/${PACKAGE_NAME}
            echo "Removed system-wide directory: /usr/share/${PACKAGE_NAME}"
        fi
        ;;

    upgrade|failed-upgrade|abort-remove)
        # 升级时不执行清理操作
        ;;

    *)
        echo "postrm called with unknown argument \\\`\$1'" >&2
        exit 1
        ;;
esac

# 更新桌面数据库
update-desktop-database

exit 0
EOL
chmod +x ${FULL_PACKAGE_NAME}/DEBIAN/postrm

# 构建 Debian 包
dpkg-deb --build ${FULL_PACKAGE_NAME}

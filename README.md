# Wallpaper Changer

Wallpaper Changer 是一个用于 Debian 系统的桌面壁纸自动更换工具。

## 功能特点

- 自动更换桌面壁纸
- 可自定义壁纸目录
- 可设置壁纸更换时间间隔
- 支持开机自启动
- 系统托盘图标，方便操作
- 支持自选年月范围下载bing壁纸

## 安装

1. 下载最新的 .deb 安装包
2. 使用以下命令安装：

```bash
sudo apt-get install python3-pip libwxbase3.2-1t64 libwxgtk-gl3.2-1t64 libwxgtk3.2-1t64 python3-wxgtk4.0
pip install wxPython requests lxml
sudo dpkg -i wallpaper-changer.deb
```

## 使用方法

### 一. 自动更换壁纸

1. 从应用程序菜单启动 Wallpaper Changer
2. 选择壁纸所在目录
3. 设置壁纸更换时间间隔
4. 点击"开始"按钮开始自动更换壁纸
5. 点击程序右上角的"X"按钮关闭程序会最小化到托盘
6. 退出程序时，点击托盘图标，选择"退出"或着点击"退出程序"按钮关闭程序

### 二. 下载壁纸

1. 打开 Wallpaper Changer 程序
2. 使用默认的壁纸下载web api网址或者自定义api网址
3. 点击"下载壁纸"按钮
4. 在弹出的对话框中选择壁纸保存目录
5. 选择开始时间和结束时间
6. 点击"下载"按钮开始下载壁纸

### 三. 自定义下载api网址

[Bing-Month-Wallpaper](https://github.com/ranvane/Bing-Month-Wallpaper)是本项目的api配套项目。

fork [Bing-Month-Wallpaper]到自己的仓库，如果你自己的仓库的名字为`Bing-Month-Wallpaper`，则`Wallpaper Changer`的`壁纸下载`页的接口网址`字段为：

    `https://你的github用户名.github.io/Bing-Month-Wallpaper/`
点击加号按钮，添加一个新的接口网址。

#### 注意：
    选择的下载时间范围比较长时，可能会导致下载时长过长和下载失败。
## 系统要求

- Debian 或基于 Debian 的 Linux 发行版
- Python 3.6 或更高版本
- wxPython 4.0 或更高版本


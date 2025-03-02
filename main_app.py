import wx
import os
import random
import subprocess
from pathlib import Path
import time
import threading
import json
from loguru import logger
import shutil
import sys
from wx.adv import TaskBarIcon
from Wallpaper_changer_UI import Main_Ui_Frame
from WallpaperChangerTaskBarIcon import WallpaperChangerTaskBarIcon
from my_logger import logger, RESOURCE_PATH, IS_PRODUCTION
from WallpaperProcessor import WallpaperProcessor
from ConfigMixin import ConfigMixin


class Main_Frame(Main_Ui_Frame, ConfigMixin):

    def __init__(self):
        super().__init__(parent=None)
        self.processor = WallpaperProcessor(self)

        self.running = False
        self.thread = None
        self.wallpapers = []
        self.current_index = -1

        try:
            # 修改配置文件路径
            self.config_file = os.path.expanduser(
                '~/.config/wallpaper-changer/config.json')

            # 修改图标路径
            self.SetIcon(wx.Icon(os.path.join(RESOURCE_PATH, "icon.png")))
            # self.SetIcon(wx.Icon("icon.png"), "壁纸更换器")

            # 修改模板文件路径
            self.template_file = os.path.join(
                RESOURCE_PATH, 'resources',
                'wallpaper_changer_template.desktop')

            self.home_dir = Path.home()  # 获取用户主目录路径
            self.autostart_dir = self.home_dir / '.config' / 'autostart'  # 设置自动启动目录路径
            self.desktop_file = self.autostart_dir / 'wallpaper_changer.desktop'  # 设置桌面文件路径
            # 加载配置
            self.load_config()

            # 检查是否设置了开机启动
            self.check_autostart()

            # 绑定事件
            self.Bind(wx.EVT_CLOSE, self.on_close)
            # 初始化系统托盘图标
            try:
                taskbar_icon = WallpaperChangerTaskBarIcon(self)

                logger.debug("托盘图标初始化完成")
            except Exception as e:
                logger.exception(f"创建托盘图标时发生异常: {e}")

        except Exception as e:
            logger.error(f"初始化时出错: {e}")

    def hide_window(self):
        """
        隐藏主窗口到系统托盘的方法。
        使用wx.CallAfter确保在主事件循环中执行隐藏操作。
        """

        self.processor.hide_window()

    def check_autostart(self):

        self.processor.check_autostart()

    def on_m_dirPicker_changed(self, event):
        self.processor.on_m_dirPicker_changed(event)

    def on_exit(self, event):
        """
        程序退出时的处理方法。

        此方法负责停止所有正在运行的进程，保存配置，
        销毁系统托盘图标和主窗口，最后退出应用程序。

        Args:
            event: 触发退出的事件对象（未使用）
        """
        self.processor.on_exit(event)

    def on_close(self, event):
        """
        处理窗口关闭事件的方法。
        
        当用户尝试关闭窗口时，此方法会被调用。
        它会隐藏窗口而不是真正关闭程序，使程序继续在后台运行。

        Args:
            event (wx.CloseEvent): 关闭窗口的事件对象
        """
        self.processor.on_close(event)

    def on_start(self, event):
        self.processor.on_start(event)

    def on_stop(self, event):
        """
        停止壁纸更换的方法。

        当用户点击停止按钮时调用此方法。它会停止壁纸更换进程，
        更新UI状态，并启动非阻塞的线程清理过程。

        Args:
            event: 触发此方法的事件对象（未使用）
        """
        self.processor.on_stop(event)

    def on_prev(self, event):
        """
        切换到上一张壁纸的方法。

        当用户点击"上一张"按钮时调用此方法。它会将当前壁纸索引减1（循环到列表末尾），
        然后设置新的壁纸。

        Args:
            event: 触发此方法的事件对象（未使用）
        """
        WallpaperProcessor.on_prev(self)

    def on_next(self, event):
        """
        切换到下一张壁纸的方法。

        当用户点击"下一张"按钮时调用此方法。它会将当前壁纸索引加1（循环到列表开头），
        然后设置新的壁纸。

        Args:
            event: 触发此方法的事件对象（未使用）
        """
        WallpaperProcessor.on_next(self)

    def on_auto_start_changed(event):
        """
        处理自动启动选项变更的方法。

        当用户切换自动启动复选框时调用此方法。它会根据用户的选择
        创建或删除开机自启动文件。

        Args:
            event: 触发此方法的事件对象（未使用）
        """

        WallpaperProcessor.on_auto_start_changed(event)

    def on_select_Save_Folder(self, event):
        """
        选择保存图片的文件夹,并将选择的路径显示到文本控件中。

        Args:
            event: 触发此方法的事件对象
        """
        dlg = wx.DirDialog(self, "选择保存图片的文件夹", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            selected_path = dlg.GetPath()
            self.m_textCtrl_save_folder.SetValue(selected_path)
            logger.info(f"选择的保存路径: {selected_path}")
        dlg.Destroy()


if __name__ == '__main__':
    app = wx.App()
    # 设置应用程序名称和图标、取消，会影响托盘图标加载
    # app.SetAppName("壁纸更换器")
    # app.SetAppDisplayName("壁纸更换器")

    frame = Main_Frame()
    frame.Show()
    app.MainLoop()

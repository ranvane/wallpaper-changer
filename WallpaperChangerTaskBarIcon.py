import wx
import os
import random
import subprocess
from pathlib import Path
import time
import threading
import json
import shutil
import sys
from wx.adv import TaskBarIcon
from Wallpaper_changer_UI import Main_Ui_Frame
from my_logger import logging,RESOURCE_PATH,IS_PRODUCTION

    
class WallpaperChangerTaskBarIcon(TaskBarIcon):

    def __init__(self, frame):
        """
        初始化 WallpaperChangerTaskBarIcon 类的实例。

        Args:
            frame (wx.Frame): 主应用程序窗口的引用
        """
        # 调用父类 TaskBarIcon 的初始化方法
        super().__init__()
        # 保存对主窗口的引用
        self.frame = frame
        self.icon = None
        self.load_icon()

        # 绑定左键点击事件到 on_left_down 方法
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

    def load_icon(self):
        icon_path = os.path.join(RESOURCE_PATH, "icon.png")

        if not os.path.exists(icon_path):
            logging.error(f"图标文件不存在: {icon_path}")
            return

        try:
            self.icon = wx.Icon(icon_path)
            if not self.icon.IsOk():
                logging.error("图标加载失败：无效的图标数据")
                return

            if self.SetIcon(self.icon, "壁纸更换器"):
                logging.debug("成功设置托盘图标")

            else:
                logging.error("设置托盘图标失败")

        except Exception as e:
            logging.exception(f"加载托盘图标时发生异常: {e}")

    def on_left_down(self, event):
        """
        处理任务栏图标左键点击事件的方法。

        当用户左键点击任务栏图标时，此方法会被调用，用于显示主窗口。

        Args:
            event: 鼠标事件对象（在此方法中未被使用）
        """
        logging.debug("托盘图标被点击")

        if self.frame:
            self.frame.Show()
            self.frame.Raise()
        else:
            logging.warning("主窗口引用无效")
        event.Skip()  # 确保事件能够继续传递

    def CreatePopupMenu(self):
        """
        创建任务栏图标的弹出菜单。

        Returns:
            wx.Menu: 包含各种操作选项的弹出菜单
        """
        menu = wx.Menu()

        # 添加"显示主窗口"菜单项
        show_item = menu.Append(wx.ID_ANY, "显示主窗口")

        # 添加"上一张"菜单项
        pre_item = menu.Append(wx.ID_ANY, "上一张")

        # 添加"下一张"菜单项
        next_item = menu.Append(wx.ID_ANY, "下一张")

        # 添加"退出"菜单项
        exit_item = menu.Append(wx.ID_ANY, "退出")

        # 绑定事件处理器
        # 注意：绑定事件的顺序与菜单项的添加顺序相同
        self.Bind(wx.EVT_MENU, self.on_show, show_item)
        self.Bind(wx.EVT_MENU, self.on_pre, pre_item)
        self.Bind(wx.EVT_MENU, self.on_next, next_item)
        self.Bind(wx.EVT_MENU, self.on_exit, exit_item)

        return menu

    def on_pre(self, event):
        """切换到上一张壁纸"""
        if self.frame:
            wx.CallAfter(self.frame.on_prev, event)
        else:
            logging.warning("无法切换到上一张壁纸：主窗口引用无效")

    def on_next(self, event):
        """切换到下一张壁纸"""
        if self.frame:
            wx.CallAfter(self.frame.on_next, event)
        else:
            logging.warning("无法切换到下一张壁纸：主窗口引用无效")

    def on_show(self, event):
        """显示主窗口"""
        if self.frame:
            self.frame.Show()
            self.frame.Raise()
        else:
            logging.warning("无法显示主窗口：主窗口引用无效")

    def on_exit(self, event):
        """退出应用程序"""
        if self.frame:
            wx.CallAfter(self.frame.on_exit, event)
        else:
            logging.warning("无法正常退出：主窗口引用无效")
            wx.CallAfter(wx.GetApp().ExitMainLoop)

    def Destroy(self):
        """
        销毁托盘图标并释放资源。
        """
        try:
            self.RemoveIcon()
            if self.icon:
                del self.icon
            logging.debug("托盘图标已成功销毁")
        except Exception as e:
            logging.error(f"销毁托盘图标时出错: {e}")
        finally:
            super().Destroy()


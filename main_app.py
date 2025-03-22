import wx
import os
import sys
from pathlib import Path

from wx.adv import TaskBarIcon
from Wallpaper_changer_UI import Main_Ui_Frame
from WallpaperChangerTaskBarIcon import WallpaperChangerTaskBarIcon
from app_logger import logging, RESOURCE_PATH, IS_PRODUCTION
from WallpaperProcessor import WallpaperProcessor
from DownloadProcessor import DownloadProcessor
from ConfigMixin import ConfigMixin
from YearMonthPicker import YearMonthPicker


class Main_Frame(Main_Ui_Frame, ConfigMixin):

    def __init__(self):
        super().__init__(parent=None)

        # 从 VERSION 文件读取版本号
        version_file_path = os.path.join(RESOURCE_PATH,  'VERSION')
        if os.path.exists(version_file_path):
            with open(version_file_path, 'r') as f:
                version = f.read().strip()
        else:
            version = ""

        # 设置程序标题
        self.SetTitle(f"壁纸更换器 - V{version}")

        self.running = False
        self.thread = None
        self.wallpapers = []
        self.current_index = -1
        self.config_file = None

        try:
            # 修改配置文件路径
            self.config_file = os.path.expanduser(
                '~/.config/wallpaper-changer/config.json')
            # logging.DEBUG(self.config_file)

            # 修复wxformbuilder设置的图标、图片路径在打包运行后找不到的问题
            try:
                self.SetIcon(wx.Icon(os.path.join(RESOURCE_PATH, 'resources', "icon.png")))
                self.m_bpButton_add_Api.SetBitmap(wx.Bitmap(os.path.join(RESOURCE_PATH, 'resources', "plus.png")))
                self.m_bpButton_minus_Api.SetBitmap(wx.Bitmap(os.path.join(RESOURCE_PATH, 'resources', "minus.png")))
            except Exception as e:
                logging.exception(f"加载应用图标时发生异常: {e}")

            # 修改模板文件路径
            self.template_file = os.path.join(
                RESOURCE_PATH, 'resources',
                'wallpaper_changer_template.desktop')

            self.home_dir = Path.home()  # 获取用户主目录路径
            self.autostart_dir = self.home_dir / '.config' / 'autostart'  # 设置自动启动目录路径
            self.desktop_file = self.autostart_dir / 'wallpaper_changer.desktop'  # 设置桌面文件路径

            # 加载配置
            self.load_config()

            self.init_processors()  # 初始化处理器
            self.bind_events()  # 绑定事件

            # 检查是否设置了开机启动
            self.check_autostart()

            # 初始化系统托盘图标
            try:
                taskbar_icon = WallpaperChangerTaskBarIcon(self)

                logging.debug("托盘图标初始化完成")
            except Exception as e:
                logging.exception(f"创建托盘图标时发生异常: {e}")

        except Exception as e:
            logging.error(f"初始化时出错: {e}")

    def init_processors(self):
        # 初始化处理器实例
        self.wallpaper_processor = WallpaperProcessor(self)
        self.download_processor = DownloadProcessor(self)

    def bind_events(self):
        # 将 Main_Ui_Frame 中的事件绑定到处理器的方法
        # 绑定事件
        self.Bind(wx.EVT_CLOSE, self.on_close)
        # 更换壁纸按钮事件
        self.m_dirPicker.Bind(wx.EVT_DIRPICKER_CHANGED,
                              self.wallpaper_processor.on_m_dirPicker_changed)
        self.m_button_start.Bind(wx.EVT_BUTTON,
                                 self.wallpaper_processor.on_start)
        self.m_button_stop.Bind(wx.EVT_BUTTON,
                                self.wallpaper_processor.on_stop)
        self.m_button_prev.Bind(wx.EVT_BUTTON,
                                self.wallpaper_processor.on_prev)
        self.m_button_next.Bind(wx.EVT_BUTTON,
                                self.wallpaper_processor.on_next)
        self.m_checkBox_autoStart.Bind(
            wx.EVT_CHECKBOX, self.wallpaper_processor.on_auto_start_changed)
        self.m_button_exit.Bind(wx.EVT_BUTTON, self.on_exit)

        # 下载壁纸按钮事件
        self.m_button_select_Save_Folder.Bind(
            wx.EVT_BUTTON, self.download_processor.on_select_Save_Folder)
        self.m_button_start_Download.Bind(
            wx.EVT_BUTTON, self.download_processor.on_start_Download)
        self.m_checkBox_use_Wallpapers_Folder.Bind(
            wx.EVT_CHECKBOX, self.download_processor.on_checkBox_use_Wallpapers_Folder)
        self.m_bpButton_add_Api.Bind(wx.EVT_BUTTON, self.download_processor.on_bpButton_add_Api)
        self.m_bpButton_minus_Api.Bind(wx.EVT_BUTTON, self.download_processor.on_bpButton_minus_Api)

    def check_autostart(self):
        '''检查是否设置了开机启动'''

        self.wallpaper_processor.check_autostart()

    def on_exit(self, event):
        """
        程序退出时的处理方法。

        此方法负责停止所有正在运行的进程，保存配置，
        销毁系统托盘图标和主窗口，最后退出应用程序。

        Args:
            event: 触发退出的事件对象（未使用）
        """
        logging.debug("开始执行退出操作")

        # 停止壁纸更换进程
        self.wallpaper_processor.on_stop(event)

        # 保存配置
        self.save_config()

        # 销毁系统托盘图标
        if hasattr(self, 'taskbar_icon') and self.main_frame.taskbar_icon:
            logging.debug("正在销毁系统托盘图标")
            wx.CallAfter(self.main_frame.taskbar_icon.Destroy)

        # 销毁主窗口
        logging.debug("正在销毁主窗口")
        self.Destroy()

        # 使用 wx.CallAfter 确保在主事件循环中退出应用
        logging.debug("准备退出应用程序")
        wx.CallAfter(wx.GetApp().ExitMainLoop)

    def on_close(self, event):
        """
        处理窗口关闭事件的方法。
        
        当用户尝试关闭窗口时，此方法会被调用。
        它会隐藏窗口而不是真正关闭程序，使程序继续在后台运行。

        Args:
            event (wx.CloseEvent): 关闭窗口的事件对象
        """
        self.Hide()
        event.Veto()  # 阻止默认的关闭行为


if __name__ == '__main__':
    app = wx.App()


    frame = Main_Frame()

    frame.Show()

    app.MainLoop()

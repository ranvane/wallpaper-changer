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

# 定义环境标志
IS_PRODUCTION = os.path.dirname(os.path.abspath(
    sys.argv[0])) == '/usr/local/bin'
logger.info(f"IS_PRODUCTION: {IS_PRODUCTION}")
# 定义资源路径
if IS_PRODUCTION:
    # 生产环境：使用 /usr/share/wallpaper-changer
    RESOURCE_PATH = "/usr/share/wallpaper-changer"
    
    logger.remove()  # 移除默认的处理器
    
    logger.add(sys.stderr, level="INFO")  # 这里设置为 INFO 级别

else:
    # 开发环境：使用当前文件所在目录
    RESOURCE_PATH = os.path.dirname(os.path.abspath(__file__))
    logger.remove()  # 移除默认的处理器
    logger.add(sys.stderr, level="DEBUG")  # 这里设置为 DEBUG 级别
    

# 确保资源路径存在
if not os.path.exists(RESOURCE_PATH):
    logger.debug(f"警告: 资源路径 {RESOURCE_PATH} 不存在，将使用当前目录作为资源路径")
    RESOURCE_PATH = os.path.dirname(os.path.abspath(__file__))

logger.info(f"环境: {'生产' if IS_PRODUCTION else '开发'}")
logger.info(f"使用资源路径: {RESOURCE_PATH}")


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
        logger.debug(f"尝试加载图标: {icon_path} 是否存在：{os.path.exists(icon_path)}")

        if not os.path.exists(icon_path):
            logger.error(f"图标文件不存在: {icon_path}")
            return

        try:
            self.icon = wx.Icon(icon_path)
            if not self.icon.IsOk():
                logger.error("图标加载失败：无效的图标数据")
                return

            if self.SetIcon(self.icon, "壁纸更换器"):
                logger.debug("成功设置托盘图标")

            else:
                logger.error("设置托盘图标失败")
            logger.debug(f"Icon successfully set: {self.icon.IsOk()}")
            logger.debug(f"Icon set to taskbar: {self.IsAvailable()}")
        except Exception as e:
            logger.exception(f"加载托盘图标时发生异常: {e}")

    def on_left_down(self, event):
        """
        处理任务栏图标左键点击事件的方法。

        当用户左键点击任务栏图标时，此方法会被调用，用于显示主窗口。

        Args:
            event: 鼠标事件对象（在此方法中未被使用）
        """
        logger.debug("托盘图标被点击")

        if self.frame:
            self.frame.Show()
            self.frame.Raise()
        else:
            logger.warning("主窗口引用无效")
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
            logger.warning("无法切换到上一张壁纸：主窗口引用无效")

    def on_next(self, event):
        """切换到下一张壁纸"""
        if self.frame:
            wx.CallAfter(self.frame.on_next, event)
        else:
            logger.warning("无法切换到下一张壁纸：主窗口引用无效")

    def on_show(self, event):
        """显示主窗口"""
        if self.frame:
            self.frame.Show()
            self.frame.Raise()
        else:
            logger.warning("无法显示主窗口：主窗口引用无效")

    def on_exit(self, event):
        """退出应用程序"""
        if self.frame:
            wx.CallAfter(self.frame.on_exit, event)
        else:
            logger.warning("无法正常退出：主窗口引用无效")
            wx.CallAfter(wx.GetApp().ExitMainLoop)

    def Destroy(self):
        """
        销毁托盘图标并释放资源。
        """
        try:
            self.RemoveIcon()
            if self.icon:
                del self.icon
            logger.debug("托盘图标已成功销毁")
        except Exception as e:
            logger.error(f"销毁托盘图标时出错: {e}")
        finally:
            super().Destroy()


class Main_Frame(Main_Ui_Frame):

    def __init__(self):
        super().__init__(parent=None)

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

        def do_hide():
            self.Hide()
            if hasattr(self, 'taskbar_icon'):
                self.taskbar_icon.show_balloon("壁纸更换器", "程序已最小化到系统托盘")

        wx.CallAfter(do_hide)

    def load_config(self):
        """
        加载配置文件的方法。

        此方法尝试从配置文件中读取设置，并将其应用到UI控件上。
        如果配置文件存在，它会加载目录路径和时间间隔设置。
        """
        logger.debug("Loading configuration...")

        if os.path.exists(self.config_file):
            # 如果配置文件存在，则打开并读取内容
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                # 设置目录选择器的路径
                self.m_dirPicker.SetPath(config.get('directory', ''))
                # 设置时间间隔控件的值
                self.m_spinCtrl_interval.SetValue(config.get('interval', 60))
                # 显示壁纸目录路径
                self.m_staticText_dirpath.SetLabel(
                    f"壁纸目录: {self.m_dirPicker.GetPath()}")
                # 选择是否开机启动隐藏窗口
                self.m_checkBox_startHideWin.SetValue(
                    config.get('hidewindown', True))

    def save_config(self):
        """
        保存配置到文件的方法。

        此方法将当前的设置（包括壁纸目录和更换间隔）保存到配置文件中。
        """
        logger.debug("Save configuration...")

        # 创建包含当前设置的配置字典
        config = {
            'directory': self.m_dirPicker.GetPath(),
            'interval': self.m_spinCtrl_interval.GetValue(),
            'hidewindown': self.m_checkBox_startHideWin.GetValue()
        }

        # 确保配置目录存在
        config_dir = os.path.dirname(self.config_file)
        Path(config_dir).mkdir(parents=True, exist_ok=True)

        try:
            # 尝试将配置写入文件
            with open(self.config_file, 'w') as f:
                json.dump(config, f)
            logger.debug(f"配置已保存到 {self.config_file}")
            self.m_staticText_status.SetLabel(f"配置已保存！")
        except Exception as e:
            # 如果保存过程中出现错误，记录错误并更新状态文本
            logger.error(f"保存配置时出错: {e}")
            self.m_staticText_status.SetLabel(f"保存配置失败: {e}")

    def check_autostart(self):

        if self.desktop_file.exists():
            logger.debug("检测到开机自启动设置")
            self.m_checkBox_autoStart.SetValue(True)

            # 开机启动开始更换壁纸
            self._start()
            # 隐藏窗口而不是关闭
            if self.m_checkBox_startHideWin.GetValue():
                self.hide_window()

        else:
            logger.debug("未检测到开机自启动设置")
            self.m_checkBox_autoStart.SetValue(False)

    def on_m_dirPicker_changed(self, event):
        logger.debug("Directory changed")
        self.m_staticText_dirpath.SetLabel(
            f"壁纸目录: {self.m_dirPicker.GetPath()}")
        self.save_config()

    def on_exit(self, event):
        """
        程序退出时的处理方法。

        此方法负责停止所有正在运行的进程，保存配置，
        销毁系统托盘图标和主窗口，最后退出应用程序。

        Args:
            event: 触发退出的事件对象（未使用）
        """
        logger.debug("开始执行退出操作")

        # 停止壁纸更换进程
        self.on_stop(None)

        # 保存配置
        self.save_config()

        # 销毁系统托盘图标
        if hasattr(self, 'taskbar_icon') and self.taskbar_icon:
            logger.debug("正在销毁系统托盘图标")
            wx.CallAfter(self.taskbar_icon.Destroy)

        # 销毁主窗口
        logger.debug("正在销毁主窗口")
        self.Destroy()

        # 使用 wx.CallAfter 确保在主事件循环中退出应用
        logger.debug("准备退出应用程序")
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

    def on_start(self, event):
        self._start()
        logger.debug("启动更换壁纸")

    def _start(self):
        """
        启动壁纸更换进程的内部方法。

        此方法负责初始化壁纸更换过程，包括获取设置、验证壁纸文件、
        更新UI状态，以及启动壁纸更换线程。
        """
        if hasattr(self, 'running') and self.running:
            logger.warning("壁纸更换进程已在运行中")
            return
        try:
            # 获取用户选择的壁纸目录路径
            wallpaper_dir = self.m_dirPicker.GetPath()
            if wallpaper_dir=="":
                # wx.MessageBox('请选择壁纸目录', '错误', wx.OK | wx.ICON_ERROR)
                # 在主线程中更新 UI
                wx.CallAfter(self.m_staticText_status.SetLabel, "注意！请选择壁纸目录。")
                return
            # 获取用户设置的时间间隔（分钟），并转换为秒
            interval = self.m_spinCtrl_interval.GetValue() * 60  # 转换为秒

            # 获取指定目录中所有的jpg和png图片文件
            self.wallpapers = [
                f for f in os.listdir(wallpaper_dir)
                if f.endswith(('.jpg', '.png'))
            ]
            # 如果没有找到图片文件，显示错误消息并返回
            if not self.wallpapers:
                # wx.MessageBox('wallpapers文件夹中没有图片', '错误',wx.OK | wx.ICON_ERROR)
                # 在主线程中更新 UI
                wx.CallAfter(self.m_staticText_status.SetLabel, "注意！wallpapers目录中没有图片。")
                return

            # 设置运行标志为True
            self.running = True

            # 确保之前的线程已经结束
            if hasattr(self,
                       'thread') and self.thread and self.thread.is_alive():
                self.thread.join(timeout=0.5)  # 等待线程结束，最多等待0.5秒
                if self.thread.is_alive():
                    raise RuntimeError("无法停止之前的线程")

            # 创建并启动新的壁纸更换线程
            self.thread = threading.Thread(target=self.change_wallpaper,
                                           args=(wallpaper_dir, interval))
            self.thread.daemon = True
            self.thread.start()

            # 更新UI状态：禁用开始按钮，启用停止和切换按钮，CallAfter避免在非主线程中直接操作 UI
            wx.CallAfter(self.m_button_start.Disable)
            wx.CallAfter(self.m_button_stop.Enable)
            wx.CallAfter(self.m_button_prev.Enable)
            wx.CallAfter(self.m_button_next.Enable)

        except Exception as e:
            # 捕获并记录任何异常
            logger.error(f"on_start出错: {e}")
            wx.MessageBox(f'on_start出错：{str(e)}', '错误', wx.OK | wx.ICON_ERROR)
            self._cleanup()

    def on_stop(self, event):
        """
        停止壁纸更换的方法。

        当用户点击停止按钮时调用此方法。它会停止壁纸更换进程，
        更新UI状态，并启动非阻塞的线程清理过程。

        Args:
            event: 触发此方法的事件对象（未使用）
        """
        if not hasattr(self, 'running') or not self.running:
            return  # 如果已经停止，直接返回

        logger.debug("正在停止壁纸更换...")
        self.running = False

        if hasattr(self, 'thread') and self.thread and self.thread.is_alive():
            self.thread.join(timeout=0.5)  # 等待线程结束，最多等待0.5秒
            if self.thread.is_alive():
                logger.warning("线程未能在预期时间内结束")

        wx.CallAfter(self._cleanup)

    def _check_thread_status(self):
        """
        检查壁纸更换线程的状态。

        如果线程仍在运行，则延迟100毫秒后再次检查。
        如果线程已结束，则执行清理操作。
        """
        if self.thread and self.thread.is_alive():
            # 线程仍在运行，100毫秒后再次检查
            wx.CallLater(100, self._check_thread_status)
        else:
            # 线程已结束，执行清理操作
            self._cleanup()

    def _cleanup(self):
        """
        清理资源和重置状态的方法。
        """
        logger.debug("正在清理资源...")
        self.running = False
        if hasattr(self, 'thread'):
            del self.thread

        wx.CallAfter(self.m_button_start.Enable)
        wx.CallAfter(self.m_button_stop.Disable)
        wx.CallAfter(self.m_button_prev.Disable)
        wx.CallAfter(self.m_button_next.Disable)
        wx.CallAfter(self.m_staticText_status.SetLabel, "已停止更换壁纸")
        logger.debug("资源清理完成")

    def on_prev(self, event):
        """
        切换到上一张壁纸的方法。

        当用户点击"上一张"按钮时调用此方法。它会将当前壁纸索引减1（循环到列表末尾），
        然后设置新的壁纸。

        Args:
            event: 触发此方法的事件对象（未使用）
        """
        try:
            if self.wallpapers:
                # 计算新的壁纸索引，如果到达列表开头则循环到末尾
                self.current_index = (self.current_index - 1) % len(
                    self.wallpapers)
                # 设置新的壁纸
                self.set_wallpaper(self.m_dirPicker.GetPath())
        except Exception as e:
            # 捕获并记录任何异常
            logger.error(f"on_prev出错: {e}")

    def on_next(self, event):
        """
        切换到下一张壁纸的方法。

        当用户点击"下一张"按钮时调用此方法。它会将当前壁纸索引加1（循环到列表开头），
        然后设置新的壁纸。

        Args:
            event: 触发此方法的事件对象（未使用）
        """
        try:
            if self.wallpapers:
                # 计算新的壁纸索引，如果到达列表末尾则循环到开头
                self.current_index = (self.current_index + 1) % len(
                    self.wallpapers)
                # 设置新的壁纸
                self.set_wallpaper(self.m_dirPicker.GetPath())
        except Exception as e:
            # 捕获并记录任何异常
            logger.error(f"on_next出错: {e}")

    def on_auto_start_changed(self, event):
        """
        处理自动启动选项变更的方法。

        当用户切换自动启动复选框时调用此方法。它会根据用户的选择
        创建或删除开机自启动文件。

        Args:
            event: 触发此方法的事件对象（未使用）
        """

        if self.m_checkBox_autoStart.IsChecked():
            logger.debug("用户选择了开机自动启动")
            try:
                # 确保 autostart 目录存在
                self.autostart_dir.mkdir(parents=True, exist_ok=True)
                # 复制模板文件到 autostart 目录
                shutil.copy2(self.template_file, self.desktop_file)

                # 替换模板中的占位符
                with open(self.desktop_file, 'r') as f:
                    content = f.read()

                content = content.replace('{PYTHON_EXECUTABLE}',
                                          sys.executable)
                if IS_PRODUCTION:
                    content = content.replace(
                        '{SCRIPT_PATH}',
                        '/usr/local/bin/wallpaper-changer.py')  # 生产环境路径、deb打包后
                    content = content.replace(
                        '{ICON_PATH}', '/usr/share/wallpaper-changer/icon.png'
                    )  # 生产环境路径、deb打包后

                else:
                    content = content.replace(
                        '{SCRIPT_PATH}', os.path.abspath(__file__))  # 开发环境路径
                    # 生产环境路径、deb打包后
                    content = content.replace(
                        '{ICON_PATH}', os.path.join(RESOURCE_PATH, 'icon.png'))

                with open(self.desktop_file, 'w') as f:
                    f.write(content)

                logger.debug(f"已创建开机自启动文件: {self.desktop_file}")
                # wx.MessageBox("已设置开机自动启动", "成功", wx.OK | wx.ICON_INFORMATION)
                self.m_staticText_status.SetLabel(f"已创建开机自启动!")
            except Exception as e:
                logger.error(f"设置开机自启动失败: {e}")
                # wx.MessageBox(f"设置开机自启动失败: {e}", "错误", wx.OK | wx.ICON_ERROR)
                self.m_staticText_status.SetLabel(f"设置开机自启动失败!")
        else:
            logger.debug("用户取消了开机自动启动")
            try:
                # 如果文件存在，则删除它
                if self.desktop_file.exists():
                    self.desktop_file.unlink()
                    logger.debug(f"已删除开机自启动文件: {self.desktop_file}")
                    # wx.MessageBox("已取消开机自动启动", "成功", wx.OK | wx.ICON_INFORMATION)
                    self.m_staticText_status.SetLabel(f"已取消开机自动启动!")
                else:
                    logger.debug("开机自启动文件不存在，无需删除")
            except Exception as e:
                logger.error(f"取消开机自启动失败: {e}")
                # wx.MessageBox(f"取消开机自启动失败: {e}", "错误", wx.OK | wx.ICON_ERROR)
                self.m_staticText_status.SetLabel(f"取消开机自启动失败!")

    def change_wallpaper(self, directory, interval):
        """
        持续更换壁纸的方法。

        此方法在一个单独的线程中运行，根据指定的时间间隔随机选择并设置壁纸。

        Args:
            directory (str): 壁纸文件所在的目录路径
            interval (int): 更换壁纸的时间间隔（秒）
        """
        try:
            while self.running:
                if self.wallpapers:
                    # 随机选择一个壁纸索引
                    self.current_index = random.randint(
                        0,
                        len(self.wallpapers) - 1)
                    # 设置选中的壁纸
                    self.set_wallpaper(directory)
                # 等待指定的时间间隔
                time.sleep(interval)
        except Exception as e:
            # 捕获并记录任何异常
            logger.error(f"change_wallpaper出错: {e}")

    def set_wallpaper(self, wallpaper_dir):
        """
        设置壁纸

        Args:
            directory (str): 壁纸所在的目录路径
        """
        try:
            # 检查壁纸目录是否存在
            if not os.path.exists(wallpaper_dir):
                raise FileNotFoundError(f"壁纸目录不存在: {wallpaper_dir}")

            # 获取当前索引对应的壁纸文件名
            wallpaper = self.wallpapers[self.current_index]

            # 构建完整的壁纸文件路径
            wallpaper_path = os.path.join(wallpaper_dir, wallpaper)

            # 检查文件是否存在
            if not os.path.exists(wallpaper_path):
                raise FileNotFoundError(f"壁纸文件不存在: {wallpaper_path}")

            # 使用 gsettings 命令设置 GNOME 桌面背景
            result = subprocess.run([
                'gsettings', 'set', 'org.gnome.desktop.background',
                'picture-uri', f'file://{wallpaper_path}'
            ],
                                    capture_output=True,
                                    text=True,
                                    check=True)

            # 在主线程中更新 UI，显示当前壁纸信息
            wx.CallAfter(self.update_current_wallpaper, wallpaper)

            logger.debug(f"成功设置壁纸: {wallpaper}")

        except FileNotFoundError as e:
            logger.error(f"文件错误: {e}")
            # wx.CallAfter(wx.MessageBox, f"壁纸文件不存在: {wallpaper}", "错误", wx.OK | wx.ICON_ERROR)
            self.m_staticText_status.SetLabel(f"壁纸文件不存在: {wallpaper}")

        except subprocess.CalledProcessError as e:
            logger.error(f"设置壁纸时出错: {e}")
            # wx.CallAfter(wx.MessageBox, f"设置壁纸失败: {e}", "错误", wx.OK | wx.ICON_ERROR)
            self.m_staticText_status.SetLabel(f"设置壁纸时出错")

        except Exception as e:
            logger.error(f"未知错误: {e}")
            wx.CallAfter(wx.MessageBox, f"发生未知错误: {e}", "错误",
                         wx.OK | wx.ICON_ERROR)

    def update_current_wallpaper(self, wallpaper):
        """
        更新当前壁纸信息的方法。

        Args:
            wallpaper (str): 当前壁纸的文件名
        """
        logger.debug('update_current_wallpaper')
        if not self:
            return  # 如果对象已经被销毁，直接返回
        try:
            self.m_staticText_status.SetLabel(f"当前壁纸: {wallpaper}")

        except Exception as e:
            logger.error(f"更新当前壁纸信息时出错: {e}")


if __name__ == '__main__':
    app = wx.App()
    # 设置应用程序名称和图标、取消，会影响托盘图标加载
    # app.SetAppName("壁纸更换器")
    # app.SetAppDisplayName("壁纸更换器")

    frame = Main_Frame()
    frame.Show()
    app.MainLoop()

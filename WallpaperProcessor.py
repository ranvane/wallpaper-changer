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
from my_logger import logger,RESOURCE_PATH,IS_PRODUCTION

class Proxy:
    def __init__(self, obj):
        """
        初始化 Proxy 类的实例。

        Args:
            obj: 被代理的对象，所有的属性访问和方法调用将转发给这个对象。
        """
        self.obj = obj  # 将被代理的对象存储为实例变量

    def __getattr__(self, name):
        """
        处理对不存在属性的访问。

        当尝试访问 Proxy 实例中不存在的属性时，这个方法会被调用。
        它会尝试从被代理的对象 (self.obj) 中获取该属性。

        Args:
            name (str): 被请求的属性名

        Returns:
            被代理对象上对应的属性值

        Raises:
            AttributeError: 如果被代理对象也没有这个属性
        """
        return getattr(self.obj, name)

    def __getattribute__(self, name):
        """
        处理所有属性的访问。

        这个方法会拦截对 Proxy 实例的所有属性访问，包括存在和不存在的属性。
        它可以用来实现更复杂的属性访问控制逻辑。

        Args:
            name (str): 被请求的属性名

        Returns:
            属性值或一个包装后的值

        注意:
            这个方法需要谨慎使用，因为它会拦截所有属性访问，包括对 __getattr__ 的调用。
            不当的实现可能导致无限递归。
        """
        if name == 'obj':  #explicitly return obj to prevent infinite recursion
            return super().__getattribute__('obj')
        return getattr(self.obj, name)

    def __setattr__(self, name, value):
        """
        处理属性的设置。

        这个方法会拦截对属性的设置，确保正确地设置被代理对象的属性。

        Args:
            name (str): 被设置的属性名
            value: 属性值

        Raises:
            AttributeError: 如果被代理对象不允许设置该属性
        """
        if name == 'obj':
            super().__setattr__(name, value)  # 直接设置 'obj' 属性
        else:
            setattr(self.obj, name, value)  # 将属性设置在被代理的对象上
class WallpaperProcessor(Proxy):
    def __init__(self, main_frame):
        """
        初始化 WallpaperProcessor 的实例。

        Args:
            main_frame: 由 wxFormBuilder 生成的 UI 主框架实例
        """
        super().__init__(main_frame)  # 调用 Proxy 的初始化方法
            
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
            logger.debug(f"_start：当前壁纸列表长度: {len(self.wallpapers)}")
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
    def on_prev(self):
        """
        切换到上一张壁纸的方法。

        当用户点击"上一张"按钮时调用此方法。它会将当前壁纸索引减1（循环到列表末尾），
        然后设置新的壁纸。

        Args:
            event: 触发此方法的事件对象（未使用）
        """
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

    def on_next(self):
        """
        切换到下一张壁纸的方法。

        当用户点击"下一张"按钮时调用此方法。它会将当前壁纸索引加1（循环到列表开头），
        然后设置新的壁纸。

        Args:
            event: 触发此方法的事件对象（未使用）
        """
        try:
            logger.debug("切换到下一张壁纸...")
            logger.debug(f"当前壁纸列表长度: {len(self.wallpapers)}")
            logger.debug(f"当前壁纸目录: {self.m_dirPicker.GetPath()}")
            if self.wallpapers:
                # 计算新的壁纸索引，如果到达列表末尾则循环到开头
                self.current_index = (self.current_index + 1) % len(
                    self.wallpapers)
                # 设置新的壁纸
                self.set_wallpaper(self.m_dirPicker.GetPath())
        except Exception as e:
            # 捕获并记录任何异常
            logger.error(f"on_next出错: {e}")
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

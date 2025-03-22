import os
import sys
from app_logger import logging, RESOURCE_PATH, IS_PRODUCTION
import json
from pathlib import Path


class ConfigMixin:
    """
    配置管理类。
    此类提供了加载和保存配置的方法，以及获取配置值的方法。
    """

    # def __init__(self, main_frame):
    #     self.main_frame = main_frame
    def load_config(self):
        """
        加载配置文件的方法。

        此方法尝试从配置文件中读取设置，并将其应用到UI控件上。
        如果配置文件存在，它会加载目录路径和时间间隔设置。
        """
        logging.debug("Loading configuration...")
        config = {
            'bing-sites': ["https://bing.wdbyte.com/"],
            'site-default': 0
        }
        if os.path.exists(self.config_file):
            # 如果配置文件存在，则打开并读取内容
            with open(self.config_file, 'r') as f:
                config.update(json.load(f))
        # 尝试加载bing-sites值，如果bing-sites不存在或为空，则创建bing-sites
        if 'bing-sites' not in config or not config['bing-sites']:
            config['bing-sites'] = ["https://ranvane.github.io/Bing-Month-Wallpaper/"]
            logging.info("未找到 'bing-sites' 或其值为空，已创建新的 'bing-sites' 项。")
        # 尝试加载bing-site-default值，如果bing-site-default不存在，则创建bing-site-default
        if 'site-default' not in config or config['site-default'] < 0:
            config['site-default'] = 0
            logging.info("设置 'site-default'=0")
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
        # 选择是否使用壁纸文件夹
        self.m_checkBox_use_Wallpapers_Folder.SetValue(
            config.get('use_wallpapers_folder', True))
        # 显示bing-sites值
        self.m_comboBox_webSite.Clear()
        for site in config['bing-sites']:
            self.m_comboBox_webSite.Append(site)
        if self.m_comboBox_webSite.GetCount() > 0 and config['site-default'] < self.m_comboBox_webSite.GetCount():
            self.m_comboBox_webSite.SetSelection(config['site-default'])
        else:
            self.m_comboBox_webSite.SetSelection(0)

        logging.debug(f"配置已加载: {config}")

        # 如果使用壁纸文件夹，则设置壁纸下载保存目录为壁纸文件夹
        if self.m_checkBox_use_Wallpapers_Folder.GetValue():
            self.m_textCtrl_save_folder.SetValue(
                self.m_dirPicker.GetPath())
        else:
            self.m_textCtrl_save_folder.SetValue(
                config.get('wallpapers_save_folder', ''))

        self.m_statusBar.SetLabel(f"配置已加载！")

        # 将更新后的配置写回文件
        with open(self.config_file, 'w') as f:
            json.dump(config, f)

    def save_config(self):
        """
        保存配置到文件的方法。

        此方法将当前的设置（包括壁纸目录和更换间隔）保存到配置文件中。
        """
        logging.debug("Save configuration...")
        # 创建包含当前设置的配置字典
        bing_sites = list(set(self.m_comboBox_webSite.GetItems()))
        site_default = self.m_comboBox_webSite.GetSelection()
        if site_default >= len(bing_sites):
            site_default = 0
            logging.info("'site-default' 值大于等于 'bing-sites' 的长度，已将其设置为 0。")

        # 创建包含当前设置的配置字典
        config = {
            'directory':
                self.m_dirPicker.GetPath(),
            'interval':
                self.m_spinCtrl_interval.GetValue(),
            'hidewindown':
                self.m_checkBox_startHideWin.GetValue(),
            'use_wallpapers_folder':
                self.m_checkBox_use_Wallpapers_Folder.GetValue(),
            'wallpapers_save_folder': self.m_textCtrl_save_folder.GetValue(),
            'bing-sites': bing_sites,
            'site-default': site_default
        }

        # 确保配置目录存在
        config_dir = os.path.dirname(self.config_file)
        Path(config_dir).mkdir(parents=True, exist_ok=True)

        try:
            # 尝试将配置写入文件
            with open(self.config_file, 'w') as f:
                json.dump(config, f)
            logging.debug(f"配置已保存到 {self.config_file}")
            self.m_statusBar.SetLabel(f"配置已保存！")
        except Exception as e:
            # 如果保存过程中出现错误，记录错误并更新状态文本
            logging.error(f"保存配置时出错: {e}")
            self.m_statusBar.SetLabel(f"保存配置失败: {e}")

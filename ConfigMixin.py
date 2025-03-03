import os
import sys
from my_logger import logger,RESOURCE_PATH,IS_PRODUCTION
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
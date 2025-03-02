from loguru import logger   
import os
import sys
from pathlib import Path
import json
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
import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger():
    # 确保日志目录存在
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 配置根日志记录器
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # 创建一个 RotatingFileHandler
    log_file = os.path.join(log_dir, 'app.log')
    file_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
    
    # 设置日志格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # 添加处理器到根日志记录器
    logger.addHandler(file_handler)

    # 可选：如果您也想在控制台看到日志
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

# 初始化日志配置
logger = setup_logger()
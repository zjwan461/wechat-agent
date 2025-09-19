import logging
import os
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path


def get_logger(name=__name__, log_level=logging.INFO):
    """
    配置日志系统

    参数:
        name: 日志器名称
        log_level: 日志级别，默认为 INFO
    返回:
        配置好的日志器实例
    """
    # 创建日志器
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # 避免重复添加处理器
    if logger.handlers:
        return logger

    # 日志格式
    # 包含时间、日志级别、模块名、行号和日志消息
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 1. 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    # 2. 文件处理器 - 按天分割日志文件，保留30天
    # 创建日志目录
    log_dir = str(Path(__file__).parent.parent.parent / "logs")
    os.makedirs(log_dir, exist_ok=True)

    # 日志文件名格式
    log_filename = os.path.join(log_dir, 'app.log')

    # 每天凌晨轮转日志，保留30个备份
    file_handler = TimedRotatingFileHandler(
        log_filename,
        when='midnight',
        interval=1,
        backupCount=30,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)  # 文件输出所有级别日志
    file_handler.setFormatter(formatter)

    # 添加处理器到日志器
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

import logging
from logging import handlers
from datetime import datetime
import os
from .common import get_path

os.system('')

# level = logging.DEBUG
level = logging.INFO


class Logger():
    """
    打印日志+字体颜色+生成日志文件
    """

    def __init__(self):

        self.filename = get_path('logs/{}.log'.format(datetime.now().strftime('%Y%m%d')))  # 日志文件名，项目名字+日期
        self.logger = logging.getLogger(self.filename)
        self.logger.setLevel(level)  # 设置报错等级
        self.log_file = handlers.TimedRotatingFileHandler(filename=self.filename,
                                                          encoding='utf-8',
                                                          backupCount=3,  # 备份数量
                                                          when='D')  # 日期
        self.log_file.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s: %(message)s'))  # 格式化日志格式
        self.logger.addHandler(self.log_file)
        self.log_print = logging.StreamHandler()  # 打印到屏幕

    def font_color(self, color):
        # 给文字加上颜色
        self.log_print.setFormatter(logging.Formatter(color % '%(asctime)s - %(levelname)s: %(message)s'))
        self.logger.addHandler(self.log_print)

    def error(self, message):
        # 错误类型红色
        self.font_color('\033[31m%s\033[0m')
        self.logger.error(message)

    def info(self, message):
        # 成功类型绿色
        self.font_color('\033[32m%s\033[0m')
        self.logger.info(message)

    def debug(self, message):
        # 成功类型绿色
        self.font_color('\033[33m%s\033[0m')
        self.logger.debug(message)
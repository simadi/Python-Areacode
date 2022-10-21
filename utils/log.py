# _*_ coding: utf-8 _*_
import logging
import os.path
import time

#logging.basicConfig(level=logging.DEBUG)  # 配置全局root logger

class Logger(object):

    def __init__(self, logger):
        """
        指定保存日志的文件路径，日志级别，以及调用文件
            将日志存入到指定的文件中
        :param logger:
        """
        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)

        # 创建日志名称。
        rq = time.strftime('%Y%m%d', time.localtime(time.time()))

        # os.getcwd()获取当前文件的路径，os.path.dirname()获取指定文件路径的上级路径
        path_dir = os.path.dirname(__file__)
        log_path = os.path.abspath(os.path.dirname(path_dir)) + '/logs'
        if not os.path.exists(log_path):
            os.makedirs(log_path, 0o777)
        log_name = os.path.join(log_path, rq + '.txt')
        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(log_name, mode='a', encoding='utf-8')
        fh.setLevel(logging.INFO)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def get_logger(self):
        return self.logger

    '''
    logging.debug('调试级别的日志')
    logging.info('信息级别的日志')
    logging.warning('警告级别的日志')    # 或logging.warn('警告级别的日志')
    logging.error('错误级别的日志')
    logging.critical('严重错误级别的日志')
    logging.exception(ex)   # 错误级别的日志，显示多行回溯信息
    '''
import logging
import os
import time
from conf import setting
from logging.handlers import RotatingFileHandler       #按文件大小滚动备份

log_path=setting.FILE_PATH['LOG']
if not os.path.exists(log_path):
    os.mkdir(log_path)

logfile_name=log_path+r'\test.{}.log'.format(time.strftime('%Y-%m-%d'))
print(logfile_name)

class RecordLog:
    """
    封装日志
    """

    def output_logging(self):
        """
        获取logger对象
        :return:
        """
        logger =logging.getLogger(__name__)
        # 防止打印重复的log日志
        if not logger.handlers:
            logger.setLevel(setting.LOG_LEVEL)
            log_format=logging.Formatter(
                '%(levelname)s - %(asctime)s - %(filename)s:%(lineno)d -[%(module)s:%(funcName)s] - %(message)s'
            )

            # 日志输出到指定文件
            # maxByte控制单个日志文件的大小，单位是字节，backupCount:用于控制日志文件的数量
            fh=RotatingFileHandler(filename=logfile_name,mode='a',maxBytes=5242880,backupCount=7,encoding='utf-8')
            fh.setLevel(setting.LOG_LEVEL)
            fh.setFormatter(log_format)
            logger.addHandler(fh)

            # 将相应的handler添加到logger
            logger.addHandler(fh)

            # 日志输出到控制台
            sh=logging.StreamHandler()
            sh.setLevel(setting.STREAM_LOG_LEVEL)
            sh.setFormatter(log_format)
            logger.addHandler(sh)
        return logger




apilog=RecordLog()
logs=apilog.output_logging()
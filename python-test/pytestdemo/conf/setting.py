import os
import sys
import logging


DIR_PATH=os.path.dirname(os.path.dirname(__file__))

sys.path.append(DIR_PATH)



# log日志的输出基本
LOG_LEVEL=logging.DEBUG
STREAM_LOG_LEVEL=logging.DEBUG

# 文件路径
FILE_PATH={
    'extract': os.path.join(DIR_PATH, 'extract.yaml'),
    'conf':os.path.join(DIR_PATH, 'conf','config.ini'),
    'LOG':os.path.join(DIR_PATH,'log')
}

if __name__ == '__main__':
    print(DIR_PATH)
    print(FILE_PATH['conf'])
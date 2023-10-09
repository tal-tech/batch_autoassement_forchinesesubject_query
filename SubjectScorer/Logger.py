
import logging

class Logger():
    def Init(self, print_level):
        if print_level == "info":
            level = logging.INFO
        elif print_level == "debug":
            level = logging.DEBUG
        elif print_level == "warning":
            level = logging.WARNING
        elif print_level == "error":
            level = logging.ERROR
        # logging.basicConfig(level=level, filemode="a", format='[%(levelname)s] - %(asctime)s - %(message)s')
        logging.basicConfig(level=level, filename='subject_scorer.log', filemode="a", format='[%(levelname)s]%(asctime)s - %(filename)s:%(lineno)d - %(message)s')
        self.m_cLogger = logging.getLogger(__name__)
        self.m_cLogger.info("Init Logger Success!")
        return 0


#filemode：这个是指定日志文件的写入方式，有两种形式，一种是 w，一种是 a，分别代表清除后写入和追加写入。

"""
CRITICAL	50
ERROR	40
WARNING	30
INFO	20
DEBUG	10
NOTSET	0
"""

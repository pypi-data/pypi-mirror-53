# -*- coding:utf-8 -*-
''' 
统一日志记录
'''

import logging 
import time
import os
import threading
import sys
flag = False
global fh
global ch
class ILog(object):
    ''' 
    发送日志 写入统一的日志中 \n
    '''

    def __init__(self, fname):
        global flag
        global fh
        global ch
        if flag==False:
            date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
            application_path = ''
            if getattr(sys, 'frozen', False):
                application_path = os.path.dirname(sys.executable)
            elif __file__:
                application_path = os.path.dirname(fname)
                print(application_path)
            log_path = application_path +r"/logs/"
            pid = os.getpid()
            filename = 'py_' + str(pid) + '_'+ date + '.log'

            if(not os.path.exists(log_path)):
                os.makedirs(log_path)
            fh = logging.FileHandler(log_path + filename)
            ch = logging.StreamHandler()
        flag = True
        self.name = os.path.basename(fname)[:-3]
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        self.formatter = logging.Formatter('%(asctime)s - %(message)s')
        fh.setLevel(logging.INFO)
        fh.setFormatter(self.formatter)
        ch.setLevel(logging.INFO)
        ch.setFormatter(self.formatter)
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def info(self, msg):
        ''' 
        @功能 输出info类型的日志  \n
        @参数 msg 需要输出的信息 \n
        '''
        msg = self.name+' - '+'INFO - '+msg
        self.logger.info(msg)
    def warning(self, msg):
        ''' 
        @功能 输出warning类型的日志  \n
        @参数 msg 需要输出的信息 \n
        '''
        msg = self.name+' - '+'WARNING - '+msg
        self.logger.warning(msg)

    def error(self, msg):
        ''' 
        @功能 输出error类型的日志  \n
        @参数 msg 需要输出的信息 \n
        '''
        msg = self.name+' - '+'ERROR - '+msg
        self.logger.error(msg)

    def debug(self, msg):
        '''
        @功能 输出debug类型的日志  \n
        @参数 msg 需要输出的信息 \n
        '''
        msg = self.name+' - '+'DEBUG - '+msg
        self.logger.debug(msg)

    def INFO(self, msg):
        ''' 
        @功能 输出info类型的日志  \n
        @参数 msg 需要输出的信息 \n
        '''
        msg = self.name+' - '+'INFO - '+msg
        self.logger.info(msg)

    def exception(self, msg):
        ''' 
        @功能 输出exception类型的日志  \n
        @参数 msg 需要输出的信息 \n
        '''
        msg = self.name+' - '+'EXCEPTION - '+msg
        self.logger.exception(msg)

    def getLogFileName(self):
        '''
        @功能 获取日志文件名
        :return:
        '''
        date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        filename = 'py_' + date + '.log'
        return filename

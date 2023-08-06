import os
import sys
import time
import json
import logging
import inspect
import traceback
from pprint import pprint as lc


class Message(object):
    def __init__(self, fmt, *args, **kwargs):
        self.fmt = fmt
        self.args = args
        self.kwargs = kwargs
        
    # def __repr__(self):
    #     print(self.__class__, self.__dict__)
    #     return self.fmt.format(self.args, self.__dict__)

    def __str__(self):
        
        return self.fmt


class StyleAdapter(logging.LoggerAdapter):
    def __init__(self, logger, extra=None):
        self.print_output = extra.get("print_output",True)
        super(StyleAdapter, self).__init__(logger, extra or {})
        self.color = {  'Red'           : '\033[1;31m',
                        'Black'         : '\033[0;30m',   
                        'Dark Gray'     : '\033[1;30m',
                        'Light_Red'     : '\033[1;31m',
                        'Green'         : '\033[0;32m',     
                        'Light Green'   : '\033[1;32m',
                        'Brown_Orange'  : '\033[0;33m',     
                        'Yellow'        : '\033[1;33m',
                        'Blue'          : '\033[0;34m',     
                        'Light Blue'    : '\033[1;34m',
                        'Purple'        : '\033[0;35m',     
                        'Light Purple'  : '\033[1;35m',
                        'Cyan'          : '\033[0;36m',     
                        'Light Cyan'    : '\033[1;36m',
                        'Light Gray'    : '\033[0;37m',     
                        'White'         : '\033[1;37m',  
                        'No_Color'      : '\033[0;0m'
                    }

        """ TODO: finish the rest of this
        Black        0;30     Dark Gray     1;30
        Red          0;31     Light Red     1;31
        Green        0;32     Light Green   1;32
        Brown/Orange 0;33     Yellow        1;33
        Blue         0;34     Light Blue    1;34
        Purple       0;35     Light Purple  1;35
        Cyan         0;36     Light Cyan    1;36
        Light Gray   0;37     White         1;37
        """

    def error(self, level, msg, *args, **kwargs):
        if self.isEnabledFor(level):
            msg, kwargs = self.process(msg, kwargs)

            self.logger._log(level, Message(msg, args), (), **kwargs)
            # if self.print_output:
            errorMsg = "{}{}{}".format( self.color['Red'], msg, self.color['No_Color'])

            print(errorMsg)

    def warning(self, level, msg, *args, **kwargs):
        if self.isEnabledFor(level):
            msg, kwargs = self.process(msg, kwargs)
            self.logger._log(level, Message(msg, args, kwargs), (), **kwargs)
            # if self.print_output:
            errorMsg = "{}{}{}".format(self.color['Yellow'], msg, self.color['No_Color'])

            print(errorMsg)

    def color_log(self, level, msg, color, *args, **kwargs):
        logColor = self.color['White']
        if self.isEnabledFor(level):
            msg, kwargs = self.process(msg, kwargs)
        

            self.logger._log(level, Message(msg, args), (), **kwargs)
            # if self.print_output:
            
            logColor = self.color[color]

            colorMsg = "{}{}{}".format(logColor, msg, self.color['No_Color'])

            print(colorMsg)

    def log(self, level, msg, *args, **kwargs):
        if self.isEnabledFor(level):
            msg, kwargs = self.process(msg, kwargs)

          
            self.logger._log(level, Message(msg, args), (), **kwargs)
            # if self.print_output:


class lcdk:

    def __init__(self,**kwargs):
        self.print_output = kwargs.get("print_output", True)
        self.logsPath = kwargs.get("logsPath", 'logs.log')
        level = kwargs.get("logLevel", "INFO")
        logLevel = self.getLogLevel(level)
        logging.basicConfig(filename=self.logsPath,level=logLevel, filemode='w')
        self.logger = StyleAdapter(logging.getLogger(__name__), extra={"print_output":self.print_output})


    def _getCaller(self,frame):
        """
        Stack Index - 0: _getCaller
                      |-->1: call from getFormat()
                          |-->2: call from function calling getFormat()
                              |-->3: external function calling into lcdk
                                  |--> ....
        within each stack: 
            0: frame
            1: filename
            2: lineno
            3: fuction module
            4: code_context
            5: Index
                
        """
        stack = inspect.stack()
        caller_frame = stack[3][0]
        file_name = stack[3][1].split('/')[-1]
        class_name = ""
        if "self" in caller_frame.f_locals: 
            class_name = caller_frame.f_locals["self"].__class__.__name__
        elif '__name__' in caller_frame.f_locals:  
            class_name = caller_frame.f_locals['__name__']
        else: 
            pass
        function_name = inspect.getframeinfo(caller_frame).function
        lineno = caller_frame.f_lineno
        caller = "{} | {} | {}:{}".format(file_name, class_name, function_name, lineno)
        return caller

    def trace(self, frame, event, arg=""):
        try: 
            info = inspect.getframeinfo(frame.f_back)
            function_name = info.function
            if function_name == self.function_name:
                if event == "call":
                    msg =  ">>>__ENTER__  {} args {}".format(function_name,arg)

                elif event == "return":
                    msg =  "<<<__EXIT__ {} ".format(function_name)

                FORMAT = self.getFormat(msg)
                if self.print_output:
                    print("{}".format(FORMAT))
        except:
            pass
    def getLogLevel(self, level):
        getLevel = {"CRITICAL":logging.CRITICAL,
                    "ERROR":logging.ERROR, 
                    "WARNING":logging.WARNING,
                    "INFO":logging.INFO, 
                    "DEBUG":logging.DEBUG, 
                    "NOTSET":logging.NOTSET
                    } 
        return getLevel[level]


    def getFormat(self, msg="",level="INFO"):
        caller_frame = inspect.currentframe().f_back.f_back
        caller = self._getCaller(caller_frame)
        msg = str(msg)
    
        FORMAT = "[{} - {}] \n{}\n".format(caller,time.asctime(), msg)
        return FORMAT

    def error(self, errorMsg):
        if not self.print_output:
            return
        tb = traceback.format_exc()
        errorMsg+= "\n TRACEBACK {}".format(tb)
        logLevel = self.getLogLevel("ERROR")
        FORMATED_MSG = self.getFormat(errorMsg)
        self.logger.error(logLevel, FORMATED_MSG)


    def warning(self, msg, level="WARNING"):
        if not self.print_output:
            return
        logLevel = self.getLogLevel(level)
        FORMATED_MSG = self.getFormat(msg)
        self.logger.warning(logLevel, FORMATED_MSG)

    def lt_green(self, msg, level="WARNING"):
        if not self.print_output:
            return
        logLevel = self.getLogLevel(level)
        FORMATED_MSG = self.getFormat(msg)
        self.logger.color_log(logLevel, FORMATED_MSG, 'Light Green')

    def red(self, msg, level="WARNING"):
        if not self.print_output:
            return
        logLevel = self.getLogLevel(level)
        FORMATED_MSG = self.getFormat(msg)
        self.logger.color_log(logLevel, FORMATED_MSG, 'Red')
    
    def lt_cyan(self, msg, level="WARNING"):
        if not self.print_output:
            return
        logLevel = self.getLogLevel(level)
        FORMATED_MSG = self.getFormat(msg)
        self.logger.color_log(logLevel, FORMATED_MSG, 'Light Cyan')
    
    def purple(self, msg, level="WARNING"):
        if not self.print_output:
            return
        logLevel = self.getLogLevel(level)
        FORMATED_MSG = self.getFormat(msg)
        self.logger.color_log(logLevel, FORMATED_MSG, 'Purple')

    def lt_purple(self, msg, level="WARNING"):
        if not self.print_output:
            return
        logLevel = self.getLogLevel(level)
        FORMATED_MSG = self.getFormat(msg)
        self.logger.color_log(logLevel, FORMATED_MSG, 'Light Purple')
        
    def log(self, msg, level="INFO"):
        if not self.print_output:
            return
        logLevel = self.getLogLevel(level)
        FORMATED_MSG = self.getFormat(msg)
        self.logger.log(logLevel, FORMATED_MSG)

        

    


if __name__ == "__main__":
    pass
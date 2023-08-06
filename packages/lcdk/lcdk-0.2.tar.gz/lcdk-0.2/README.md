# Leslie Chow Debug Kit

## Installation
`pip install lcdk`


## Usage
`from lcdk.lcdk import lcdk as LeslieChow`

`DBG=LeslieChow.lcdk()`

`DBG.log("{}".format("MESSAGE FROM DEBUG"))`

`DBG.lt_green("{}".format("MESSAGE FROM DEBUG"))`

## Further Help

Help on module lcdk.lcdk in lcdk:

NAME
    lcdk.lcdk

FILE
   lcdk/lcdk/lcdk.py

CLASSES
    __builtin__.object
        Message
    lcdk
    logging.LoggerAdapter(__builtin__.object)
        StyleAdapter
    
    class Message(__builtin__.object)
     |  Methods defined here:
     |  
     |  __init__(self, fmt, *args, **kwargs)
     |  
     |  __str__(self)
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class StyleAdapter(logging.LoggerAdapter)
     |  Method resolution order:
     |      StyleAdapter
     |      logging.LoggerAdapter
     |      __builtin__.object
     |  
     |  Methods defined here:
     |  
     |  __init__(self, logger, extra=None)
     |  
     |  color_log(self, level, msg, color, *args, **kwargs)
     |  
     |  error(self, level, msg, *args, **kwargs)
     |  
     |  log(self, level, msg, *args, **kwargs)
     |  
     |  warning(self, level, msg, *args, **kwargs)
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from logging.LoggerAdapter:
     |  
     |  critical(self, msg, *args, **kwargs)
     |      Delegate a critical call to the underlying logger, after adding
     |      contextual information from this adapter instance.
     |  
     |  debug(self, msg, *args, **kwargs)
     |      Delegate a debug call to the underlying logger, after adding
     |      contextual information from this adapter instance.
     |  
     |  exception(self, msg, *args, **kwargs)
     |      Delegate an exception call to the underlying logger, after adding
     |      contextual information from this adapter instance.
     |  
     |  info(self, msg, *args, **kwargs)
     |      Delegate an info call to the underlying logger, after adding
     |      contextual information from this adapter instance.
     |  
     |  isEnabledFor(self, level)
     |      See if the underlying logger is enabled for the specified level.
     |  
     |  process(self, msg, kwargs)
     |      Process the logging message and keyword arguments passed in to
     |      a logging call to insert contextual information. You can either
     |      manipulate the message itself, the keyword args or both. Return
     |      the message and kwargs modified (or not) to suit your needs.
     |      
     |      Normally, you'll only need to override this one method in a
     |      LoggerAdapter subclass for your specific needs.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from logging.LoggerAdapter:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class lcdk
     |  Methods defined here:
     |  
     |  __init__(self, **kwargs)
     |  
     |  error(self, errorMsg)
     |  
     |  getFormat(self, msg='', level='INFO')
     |  
     |  getLogLevel(self, level)
     |  
     |  log(self, msg, level='INFO')
     |  
     |  lt_cyan(self, msg, level='WARNING')
     |  
     |  lt_green(self, msg, level='WARNING')
     |  
     |  lt_purple(self, msg, level='WARNING')
     |  
     |  purple(self, msg, level='WARNING')
     |  
     |  red(self, msg, level='WARNING')
     |  
     |  trace(self, frame, event, arg='')
     |  
     |  warning(self, msg, level='WARNING')





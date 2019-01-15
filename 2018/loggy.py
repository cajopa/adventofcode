from contextlib import contextmanager
from functools import wraps

from structlog import DropEvent, PrintLogger, BoundLogger

from myenum import AutoOrderedEnum



class TaggedWrapper(BoundLogger):
    tagged_methods = set()
    
    def __getattr__(self, method_name):
        method = getattr(self._logger, method_name)
        
        if getattr(method, '__func__', None) in self.tagged_methods:
            return super().__getattr__(method_name)
        else:
            return method
    
    @classmethod
    def tag(cls, f):
        cls.tagged_methods.add(f)
        
        return f


class IndentLogger(PrintLogger):
    def __init__(self, *args, indent_token='  ', **kwargs):
        super().__init__(*args, **kwargs)
        
        self.indent_level = 0
        self.indent_token = indent_token
    
    @classmethod
    def factory(cls, *args, **kwargs):
        return cls(*args, **kwargs)
    
    @property
    def indent_string(self):
        return self.indent_token * self.indent_level
    
    @contextmanager
    def indent(self):
        self.indent_level += 1
        
        try:
            yield self
        finally:
            self.indent_level -= 1
    
    @TaggedWrapper.tag
    def msg(self, message):
        return super().msg(self.indent_string + message)
    
    log = debug = info = warn = warning = msg
    fatal = failure = err = error = critical = exception = msg


class LogLevel:
    class LEVELS(AutoOrderedEnum):
        DEBUG = ()
        INFO = ()
        WARNING = ()
        ERROR = ()
        FATAL = ()
    
    def __init__(self, level=LEVELS.WARNING):
        ### TODO: figure out how to change this after the fact
        self.level = level
    
    def __call__(self, logger, method_name, event_dict):
        level_from_method = getattr(self.LEVELS, method_name.upper(), None)
        
        effective_level = event_dict.get('level', self.level)
        
        if level_from_method and level_from_method < effective_level:
            raise DropEvent
        else:
            return event_dict

def Format(format_str):
    def Format(logger, method_name, event_dict):
        return format_str.format(**event_dict)
    
    return Format

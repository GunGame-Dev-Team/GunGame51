# ../addons/eventscripts/gungame/core/debug/__init__.py
'''
$Rev$
$LastChangedBy$
$LastChangedBy$
'''
"""
This module provides a unified logging and debugging interface for gungame51.

There are four levels of debugging:

    warn:
        Something went bad or doesn't seem right, but it's not necessary to
        raise an Exception.
          
        Default output channels: es.dbgmsg (0) and logfile
          
    debug:
        Information which might be useful for debugging purposes.
    
        Default output channels: es.dbgmsg (1)
        
    notify:
        Information to be printed to server console but not logged
        
        Default output channels: es.dbgmsg (0)
        
    log:
        Information to be logged but not printed to server console
        
        Default output channels: logfile
        
        
There is also a decorator for methods to log the environment should a method fail. 
WARNING: This does not seem to work with cmdlib command functions due to CMDArgs
failing to coerce to string! Therefore the logging is done with try...except.

This decorator is called 'trace' and can be used like this:

from gungame51.core.debug import trace

@trace
def myfunction(...):
    ...
    
Now should your function be called and fail, the error and the environment under
which the error happened (arguments to the method, global variables, platform...)
will be logged.
"""
import es
from hashlib import md5
from sys import exc_info
from traceback import format_exception
from inspect import getargspec, ismethod, isclass, isfunction
from gungame51.core import get_game_dir, platform

def _write_to_log(message):
    #TODO: add a file to write to! Awaiting decision on using path over get_game_dir
    pass

def _write_to_console(message, level=0):
    #TODO: Do we want a nice prefix?
    es.dbgmsg(level, message)

def warn(message):
    #TODO: make settings to fine tune output channels
    _write_to_console(message)
    _write_to_log(message)

def debug(message):
    #TODO: make settings to fine tune output channels
    _write_to_console(message, 1)
    

def notify(message):
    #TODO: make settings to fine tune output channels
    _write_to_console(message)

def log(message):
    #TODO: make settings to fine tune output channels
    _write_to_log(message)


class MethodTracer(object):
    """
    A proxy to trace a method if it fails.
    """
    def __init__(self, method):
        self.method = method
        
    def _handle_exception(self, arguments, kwargs, extype, exvalue, extraceback):
        """
        Get the hashsum of the traceback. This will become the filename to prevent
        one error to fill the folder in seconds (in the worst case). Having hashed
        filenames means that every (unique) traceback will only be logged once!
        """
        traceback_lines = format_exception(extype, exvalue, extraceback)
        filename = md5(''.join(traceback_lines)).hexdigest() + '.txt'
        self._write_dump(arguments, kwargs, traceback_lines, filename)
        
    def _write_dump(self, arguments, kwargs, traceback_lines, filename):
        lines = []
        # Affected method and module
        lines.append("An error occured in %s.%s" % (self.method.__module__, self.method.__name__))
        # Original traceback
        lines.append("Traceback:")
        for line in traceback_lines:
            lines.append(line[:-1])
        lines.append('')
        # Get argument specifications for this method
        arg_names, varags, varkw, defaults = getargspec(self.method)
        argdict = {}
        for name, default in zip(arg_names, defaults):
            argdict[name] = {'value': default, 'default': default}
        for name, value in zip(arg_names, arguments):
            if not name in argdict:
                argdict[name] = {'value': value, 'default': 'NO_DEFAULT_PROVIDED'}
            else:
                argdict[name]['value'] = value
        for key, value in kwargs.iteritems():
            if not name in argdict:
                argdict[key] = {'value': value, 'default': 'NO_DEFAULT_PROVIDED'}
            else:
                argdict[key]['value'] = value
        arglist = []
        for name in arg_names:
            value = argdict[name]['value']
            default = argdict[name]['default']
            # Try...Except here because of things like CMDArgs messing up the logging.
            things = [name, value, type(value), default, type(default)]
            stringed = []
            for thing in things:
                try:
                    stringed.append(str(thing))
                except:
                    stringed.append('???')
            arglist.append(tuple(stringed))
        # Add the arguments to the 
        lines.append('The function was called with following arguments:')
        for arg in arglist:
            lines.append('  %s: %s (%s) [Default: %s (%s)]' % arg)
        lines.append('')
        # The server environment.
        #TODO: Does this need more information?
        lines.append('Server environment:')
        lines.append('  platform: %s' % platform)
        lines.append('  gg version: %s' % '5.1') # TODO: Detect real version
        lines.append('  es version: %s' % str(es.ServerVar('eventscripts_ver')))
        lines.append('')
        # The global variables
        lines.append('Global variables:')
        for key, value in dict(globals()).iteritems():
            lines.append('  %s: %s (%s)' % (key, value, type(value)))
        #TODO: What other information do we need? Time? Players?
        
        #TODO: real path! Should be a standalone file (timestamped)
        #logdir.joinpath(filename).write_lines(lines)
        
    def __call__(self, *arguments, **kwargs):
        """
        When the decorated method gets called try to call the method.
        
        If it fails, handle the exception and re-raise the initial exception.
        """
        try:
            return self.method(*arguments, **kwargs)
        except:
            self._handle_exception(arguments, kwargs, *exc_info())
            # Re-raise the excepted exception.
            raise
        
        
class NoTracer(object):
    def __init__(self, method):
        self.method = method
        
    def __call__(self, *args, **kwargs):
        return self.method(*args, **kwargs)
        
        
def trace(method):
    """
    Decorates a method to be traced by a MethodTracer
    """
    return MethodTracer(method)

def notrace(method):
    """
    Decorate a method not to be traced by autotrace
    """
    return NoTracer(method)

def autotrace(obj):
    """
    Autotraces a object.
    """
    for name in dir(obj):
        attr = getattr(obj, name)
        if isfunction(attr) or ismethod(attr):
            setattr(obj, name, trace(attr))
        elif isclass(attr):
            autotrace(attr)
        elif type(attr).__name__ == 'instance':
            if isinstance(attr, MethodTracer):
                continue
            if isinstance(attr, NoTracer):
                continue
            autotrace(attr) 
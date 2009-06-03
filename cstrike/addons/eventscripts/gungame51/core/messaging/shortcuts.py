# ../addons/eventscripts/gungame/core/messaging/shortcuts.py

'''
$Rev: 84 $
$LastChangedBy: WarrenAlpert $
$LastChangedDate: 2009-06-03 13:08:04 -0400 (Wed, 3 Jun 2009) $
'''

from gungame51.core.messaging import __messages__

def msg(filter, string, tokens={}, prefix=False):
    __messages__.msg(filter, string, tokens, prefix)
    
def saytext2(filter, index, string, tokens={}, prefix=False):
    __messages__.saytext2(filter, index, string, tokens, prefix)
    
def centermsg(filter, string, tokens={}):
    __messages__.centermsg(filter, string, tokens)
    
def hudhint(filter, string, tokens={}):
    __messages__.hudhint(filter, string, tokens)
    
def toptext(filter, duration, color, string, tokens={}):
    __messages__.toptext(filter, duration, color, string, tokens)
    
def echo(filter, level, string, tokens={}, prefix=False):
    __messages__.echo(filter, level, string, tokens, prefix)
    
def loadTranslation(name, addon):
    __messages__.load(name, addon)

def unloadTranslation(name, addon):
    __messages__.unload(name, addon)
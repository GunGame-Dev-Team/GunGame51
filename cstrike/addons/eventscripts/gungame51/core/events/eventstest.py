import es

def getEventList():
    '''
    Function that returns a list of events contained within various .res files
    used in Counter-Strike: Source.
    '''
    from keyvalues import KeyValues
    
    # Declare a list of ".res" paths to read the events
    list_resPaths = ['%s/resource/modevents.res' %
                    str(es.ServerVar('eventscripts_gamedir')),
                  '%s/resource/gameevents.res' %
                    str(es.ServerVar('eventscripts_gamedir')).replace('cstrike', 'hl2'),
                  '%s/resource/serverevents.res' %
                    str(es.ServerVar('eventscripts_gamedir')).replace('cstrike', 'hl2'),
                  '%s/events/es_gungame_events.res' %
                    es.getAddonPath('eventstest')]
    
    # Create a blank list to store the event names
    list_events = []
    
    # Loop through the list of .res file paths
    for path in list_resPaths:
        # Load the .res file using KeyValues
        res = KeyValues(filename=path)
        
        # Loop through each key (event name) in the .res file
        for key in res:
            # Append each event name to list_events
            list_events.append(key.getName())
    
    # Return the list of event names
    return list_events
    
# Test code
list_addons = ['findme']
def load():
    list_events = getEventList()
        
    import types
    from scripts import findme
    
    all =  findme.__dict__
    
    # run through the items and check whether they are classes are functions
    for i in all.keys():
        if type(all[i]) == types.FunctionType:
            if i in list_events:
                es.dbgmsg(0, i, 'is a valid function')
                
def player_death(event_var):
    list_events = getEventList()
    es.dbgmsg(0, '-------------------------Player Death: eventstest')
    for addon in list_addons:
        __import__('eventstest.scripts.%s' %addon, fromlist=['eventstest.scripts.%s' %addon]).player_death(event_var)
                
class EventHandler():
    def __init__(self, addon):
        self.name = str(addon)
        #__import__(name[, globals[, locals[, fromlist[, level]]]])
        __import__("myapp.commands.%s" % command, fromlist=["myapp.commands"])
        
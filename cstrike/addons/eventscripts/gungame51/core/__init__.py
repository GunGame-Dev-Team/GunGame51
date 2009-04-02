# ============================================================================
# >> IMPORTS
# ============================================================================
# Eventscripts Imports
import es

# ============================================================================
# >> GLOBALS
# ============================================================================
gamePath = str(es.ServerVar('eventscripts_gamedir')).replace('\\', '/')

# ============================================================================
# >> FUNCTIONS
# ============================================================================
def getGameDir(dir):
    '''!Gets an absolute path to a game directory.
    
    @remark Implicitly replaces \\ with / (linux support)
    
    @param dir Directory to append to the game directory.
    
    @return An absolute path to the game directory plus \p dir.'''
    # Linux path seperators
    dir = dir.replace('\\', '/')
    
    # Return
    return '%s/%s' % (gamePath, dir)
# ../addons/eventscripts/gungame/core/menus/shortcuts.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

def get_index_page(index, optionsPerPage=10):
    '''
    Returns the page number that item with the index specified is on.
    '''
    return (index / optionsPerPage) + (1 if index % optionsPerPage  > 0 else 0)
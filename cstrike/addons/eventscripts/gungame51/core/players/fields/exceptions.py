# ../core/players/fields/exceptions.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''


# =============================================================================
# >> Exception Classes
# =============================================================================
class ValidationError(Exception):
    def __init__(self, msg):
        if isinstance(msg, list):
            self.messages = msg
        else:
            self.messages = [msg]

    def __str__(self):
        return repr(self.messages)

    def __repr__(self):
        return 'ValidationError(%s)' % repr(self.messages)

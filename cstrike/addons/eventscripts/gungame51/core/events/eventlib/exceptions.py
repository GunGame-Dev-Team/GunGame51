# =============================================================================
# CLASSES
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


class ESEventError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)

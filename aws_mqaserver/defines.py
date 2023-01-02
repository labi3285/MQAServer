
        
class ValidateException(Exception):
    message = 'validate failed'
    info = None
    def __init__(self, message, info = None):
        super().__init__(self)
        self.message = message
        self.info = info
    def __str__(self):
        return self.message




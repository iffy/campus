"""
Actions
"""



class Action:
    """
    Abstract base class for actions.
    """
    
    name = None
    
    
    def __call__(self):
        """
        Do this action
        """



class Use(Action):
    """
    Action of an actor using an object.
    """
    
    def __init__(self, user, used):
        self.user = user
        self.used = used


    def __call__(self):
        self.used.use(self.user)




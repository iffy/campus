"""
Events
"""

from zope.interface import Interface, Attribute, implements



class IEvent(Interface):
    """
    I prescribe what event notifications should be like.
    """


    def describe(perspective):
        """
        Returns a string indicating what happened according to the perspective
        of who.
        """



class Entrance:
    """
    I am the event of something entering a location.
    """
    
    implements(IEvent)


    def __init__(self, who, where):
        self.who = who
        self.where = where


    def describe(self, perspective):
        """
        Return a description of the event from the given perspective.
        """
        msg = ''
        data = {}
        if perspective == self.who:
            msg = 'You entered %(location)s.'
            data = {'location': self.where.name}
        elif perspective == self.where:
            msg = '%(who)s entered you.'
            data = {'who': self.who.name}
        else:
            msg = '%(who)s entered %(location)s.'
            data = {'who': self.who.name, 'location': self.where.name}
        return msg,data
        




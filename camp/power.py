
from zope.interface import implements
from axiom.item import Item
from axiom import attributes

from camp.thing import Thing
from camp.interface import IContainer, IUseable



class Containment(Item):
    """
    I given L{Thing}s the power to contain other L{Thing}s.
    """

    implements(IContainer)
    powerupInterfaces = (IContainer,)

    thing = attributes.reference()


    def __init__(self, thing, *args, **kwargs):
        Item.__init__(self, *args, **kwargs)
        self.store = thing.store
        self.thing = thing
        thing.powerUp(self)


    def getContents(self):
        """
        Return the list of L{Thing}s located inside me.
        """
        return self.store.query(Thing, Thing.location == self.thing)



class Portal(Item):
    """
    I give L{Thing}s the power to be used as a portal to another place.
    """
    
    implements(IUseable)
    powerupInterfaces = (IUseable,)
    
    thing = attributes.reference()
    destination = attributes.reference()

    
    def __init__(self, thing, *args, **kwargs):
        Item.__init__(self, *args, **kwargs)
        self.store = thing.store
        self.thing = thing
        thing.powerUp(self)


    def use(self, who):
        """
        Use this portal.
        
        @param who: The L{Thing} using me.
        """
        try:
            dst = IContainer(self.destination)
            who.location = self.destination
        except:
            raise Exception('No destination')

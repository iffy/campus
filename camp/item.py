"""
Things go in here.
"""

from zope.interface import implements

from axiom import item, attributes as A


from camp.interface import IContainment



class Thing(item.Item):
    """
    I am a thing in the universe.
    """
    typeName = 'thing'
    schemaVersion = 1
    
    name = A.text()
    location = A.reference()



class Container(item.Item):
    """
    I am a container.
    """
    typeName = 'container'
    schemaVersion = 1
    
    implements(IContainment)
    
    thing = A.reference('foo')


    def getContents(self):
        """
        Return all the L{Things<Thing>} with C{location} set to me.
        """
        return self.store.query(Thing, Thing.location == self)




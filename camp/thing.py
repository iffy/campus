"""
"""


from axiom.item import Item
from axiom import attributes



class Thing(Item):
    """
    I am something in the World.
    """
    
    name = attributes.text()
    location = attributes.reference()
    owner = attributes.reference()



class User(Item):
    """
    I am a user of the system, but have no "physical" representation myself.
    """
    
    name = attributes.text()


    def createAvatar(self):
        """
        XXX
        """
        from camp.power import UserActor
        avatar = Thing(store=self.store, name=self.name)
        UserActor(avatar, self)
        return avatar

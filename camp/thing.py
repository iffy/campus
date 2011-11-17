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
        Create a L{Thing} to be used as an avatar for me.
        """
        from camp.power import UserActor
        avatar = Thing(store=self.store, name=self.name, owner=self)
        UserActor(avatar, self)
        return avatar


    def avatars(self):
        """
        Get a list of current avatar L{Thing}s representing me.
        """
        from camp.power import UserActor
        for ua in self.store.query(UserActor, UserActor.user == self):
            if ua.thing:
                yield ua.thing
            else:
                ua.deleteFromStore()



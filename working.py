from axiom import attributes
from axiom.item import Item
from axiom.store import Store
from zope.interface import Interface, Attribute, implements
import random


#------------------------------------------------------------------------------
# Interfaces
#------------------------------------------------------------------------------

class IContainer(Interface):

    def getContents():
        """
        Return the contents of this thing
        """

class IMortal(Interface):

    health = Attribute('hitpoints')

class IActor(Interface):

    def do(name, *args, **kwargs):
        """
        Perform an action (or attempt to)
        """

class IPortal(Interface):

    destination = Attribute('where to?')

class IUseable(Interface):

    def use(who):
        """
        Use this thing
        """

class IActionExecutor(Interface):

    def executeAction(action):
        pass



#------------------------------------------------------------------------------
# Thing
#------------------------------------------------------------------------------

class Thing(Item):

    name = attributes.text()
    owner = attributes.reference()
    location = attributes.reference()

    def __str__(self):
        parts = [str(self.name)]
        try:
            mortal = IMortal(self)
            parts.append('health: %s' % mortal.health)
        except:
            pass

        return ' '.join(parts)

    def find(self, name):
        # is it in my current location?
        if self.location:
            for obj in IContainer(self.location).getContents():
                if obj.name == name:
                    return obj
            
            # is it my location?
            if self.location.thing.name == name:
                return self.location
        
        # is it an unlocatable thing?
        return self.store.findFirst(Thing, attributes.AND(Thing.name == name,
            Thing.location == None))
        


#------------------------------------------------------------------------------
# Powers
#------------------------------------------------------------------------------

class Mortality(Item):
    
    implements(IMortal)
    powerupInterfaces = (IMortal,)
    
    thing = attributes.reference()
    health = attributes.integer(default=100)
    
    def __init__(self, thing, *args, **kwargs):
        Item.__init__(self, *args, **kwargs)
        self.store = thing.store
        self.thing = thing
        self.thing.powerUp(self)
    

class ContainmentPower(Item):

    implements(IContainer)
    powerupInterfaces = (IContainer,)
    
    thing = attributes.reference()
    
    def __init__(self, thing, *args, **kwargs):
        Item.__init__(self, *args, **kwargs)
        self.store = thing.store
        self.thing = thing
        self.thing.powerUp(self)

    def getContents(self):
        return self.store.query(Thing, Thing.location == self)


class PortalPower(Item):

    implements(IPortal, IUseable)
    powerupInterfaces = (IPortal, IUseable)
    
    thing = attributes.reference()
    destination = attributes.reference()
    
    def __init__(self, thing, destination=None, *args, **kwargs):
        Item.__init__(self, *args, **kwargs)
        self.store = thing.store
        self.thing = thing
        self.thing.powerUp(self)
        self.destination = destination

    def use(self, user):
        user.location = IContainer(self.destination)


class ActorPower(Item):
    
    implements(IActor)
    powerupInterfaces = (IActor,)
    
    thing = attributes.reference()
    
    def __init__(self, thing, *args, **kwargs):
        Item.__init__(self, *args, **kwargs)
        self.store = thing.store
        self.thing = thing
        self.thing.powerUp(self)

    def do(self, name, *args, **kwargs):
        cls = {
            'create': Create,
            'empower': Empower,
            'move': Move,
            'punch': Punch,
            'use': Use,
            'go': Go,
        }[name]
        action = cls(self.thing, *args, **kwargs)
        IActionExecutor(self.store).executeAction(action)


class ActionExecutor(Item):

    implements(IActionExecutor)
    powerupInterfaces = (IActionExecutor,)
    
    name = attributes.text()
    
    def __init__(self, store, *args, **kwargs):
        Item.__init__(self, *args, **kwargs)
        self.store = store
        store.powerUp(self)
    
    def actionAllowed(self, action):
        return True
    
    def executeAction(self, action):
        if self.actionAllowed(action):
            action()



#------------------------------------------------------------------------------
# Actions
#------------------------------------------------------------------------------

class Action:
    name = None

class Punch(Action):
    name = 'punch'
    
    def __init__(self, actor, target):
        self.actor = actor
        self.target = actor.find(target)
    def __call__(self):
        mortal = None
        try:
            mortal = IMortal(self.target)
        except TypeError, e:
            pass
        if mortal:
            mortal.health -= random.randint(1, 20)
            w = random.choice(['POW', 'KACHOW', 'BAM', 'SMACK'])
            print '* %s! %s punched %s' % (w, self.actor.name, self.target)
        else:
            print '* %s tried to punch %s' % (self.actor.name, self.target)

class Move(Action):
    name = 'move'
    
    def __init__(self, actor, what, where):
        self.actor = actor
        self.what = actor.find(what)
        self.where = IContainer(actor.find(where))
    def __call__(self):
        self.what.location = self.where
        print '* %s moved %s ' % (self.actor.name, self.what.name)

class Go(Action):
    name = 'go'
    
    def __init__(self, actor, where):
        self.actor = actor
        self.where = IContainer(actor.find(where))
    def __call__(self):
        self.actor.location = self.where
        print '* %s moved %s ' % (self.actor.name, self.where.name)

class Create(Action):
    name = 'create'
    
    def __init__(self, actor, name=None, location=None):
        self.actor = actor
        self.name = name
        if location:
            self.location = self.actor.find(location)
        else:
            self.location = self.actor.location

    def __call__(self):
        thing = Thing(store=self.actor.store)
        thing.name = self.name
        thing.owner = self.actor
        thing.location = self.location
        print '* %s created %s' % (self.actor.name, thing.name)

class Empower(Action):
    name = 'empower'
        
    def __init__(self, actor, thing, power, *args):
        self.actor = actor
        self.thing = self.actor.find(thing)
        self.power = {
            'containment': ContainmentPower,
            'mortality': Mortality,
            'portal': PortalPower,
        }[power]
        self.args = map(actor.find, args)

    def __call__(self):
        self.power(self.thing, *self.args)
        print '* %s empowered %s with %s' % (self.actor.name, self.thing.name, self.power.__name__)

class Use(Action):
    name = 'use'
    
    def __init__(self, actor, thing):
        self.actor = actor
        self.thing = actor.find(thing)
    def __call__(self):
        IUseable(self.thing).use(self.actor)
        print '%s used %s' % (self.actor, self.thing)


def main():
    import time
    
    store = Store()
    ActionExecutor(store)
    
    world = Thing(name=u'world', store=store)
    ContainmentPower(world)
    
    lobby = Thing(name=u'lobby', store=store)
    lobbyc = ContainmentPower(lobby)
    
    bob = Thing(name=u'Bob', store=store, location=lobbyc)
    Mortality(bob)
    ActorPower(bob)
    
    # later
    actor = IActor(bob)
    import shlex
    print 'you are %s' % bob
    while True:
        loc = actor.thing.location.thing
        command = map(unicode, shlex.split(raw_input('%s > ' % loc)))
        if command[0] == 'look':
            for thing in IContainer(bob.location).getContents():
                print thing
            continue
        try:
            actor.do(*command)
        except Exception, e:
            print repr(e)
            print dir(e)
            print e


if __name__ == '__main__':
    main()
    
    
    

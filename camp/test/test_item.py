from twisted.trial.unittest import TestCase

from zope.interface.verify import verifyClass


from axiom import item
from axiom.store import Store
from camp.item import Thing, Container



class ThingTest(TestCase):


    def setUp(self):
        self.store = Store()


    def test_attributes(self):
        """
        Should have name
        """
        t = Thing()
        self.assertEqual(t.name, None)
        self.assertEqual(t.location, None)


    def test_persist(self):
        """
        Should persist with axiom.
        """
        t = Thing(store=self.store)
        things = list(self.store.query(Thing))
        self.assertEqual(things, [t])
        


class ContainerTest(TestCase):


    def setUp(self):
        self.store = Store()


    def test_getContents(self):
        """
        Can return any Thing with location = contents.
        """
        c = Container(store=self.store)
        self.assertEqual(list(c.getContents()), [])
        
        t = Thing(store=self.store)
        t.location = c
        self.assertEqual(list(c.getContents()), [t])
        
        t2 = Thing(store=self.store)
        t2.location = c
        self.assertEqual(set(c.getContents()), set([t, t2]))


    def test_thing(self):
        """
        Should be attached to a thing.
        """
        c = Container(store=self.store)
        self.assertEqual(c.thing, None)
        
        t = Thing(store=self.store)
        c.thing = t
        self.assertEqual(list(c.store.query(Container, Container.thing == t)),
                         [c])
        
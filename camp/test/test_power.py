from twisted.trial.unittest import TestCase

from zope.interface.verify import verifyClass

from axiom.store import Store

from camp.interface import IContainer
from camp.power import Containment
from camp.thing import Thing



class ContainmentTest(TestCase):


    def setUp(self):
        self.store = Store()


    def test_IContainer(self):
        verifyClass(IContainer, Containment)


    def test_thing(self):
        """
        Should know what thing it empowers and take its store.
        """
        t = Thing(store=self.store)
        c = Containment(t)
        self.assertEqual(c.store, t.store)
        self.assertEqual(c.thing, t)
        self.assertEqual(IContainer(t), c)


    def test_getContents(self):
        """
        Should get everything that is located inside it.
        """
        container = Thing(store=self.store)
        Containment(container)
        
        c = IContainer(container)
        self.assertEqual(list(c.getContents()), [])
        
        a = Thing(store=self.store)
        a.location = container
        b = Thing(store=self.store)
        b.location = container
        
        self.assertEqual(set(c.getContents()), set([a,b]))
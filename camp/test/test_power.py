from twisted.trial.unittest import TestCase

from zope.interface.verify import verifyClass

from axiom.store import Store

from camp.interface import IContainer, IUseable
from camp.power import Containment, Portal
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



class PortalTest(TestCase):


    def setUp(self):
        self.store = Store()


    def test_IUseable(self):
        verifyClass(IUseable, Portal)


    def test_init(self):
        """
        It should know what thing it empowers and be attached to the store.
        """
        t = Thing(store=self.store)
        p = Portal(t)
        self.assertEqual(p.store, t.store)
        self.assertEqual(p.thing, t)
        self.assertEqual(p.destination, None)
        self.assertEqual(IUseable(t), p)


    def test_use_nodestination(self):
        """
        It should change their location to destination if there is one.
        """
        p = Portal(Thing(store=self.store))
        
        guy = Thing(store=self.store)
        self.assertRaises(Exception, p.use, guy)
    
        
    def test_use(self):
        """
        Using should change location
        """
        p = Portal(Thing(store=self.store))
        p.destination = Thing(store=self.store)
        
        guy = Thing(store=self.store)
        # destination is not a Container
        self.assertRaises(Exception, p.use, guy)

        Containment(p.destination)
        p.use(guy)
        self.assertEqual(guy.location, p.destination)




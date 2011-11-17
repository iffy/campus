from twisted.trial.unittest import TestCase


from axiom.store import Store

from camp.interface import IActor
from camp.thing import Thing, User



class ThingTest(TestCase):


    def setUp(self):
        self.store = Store()


    def test_basic(self):
        """
        A basic Thing should have these attributes
        """
        t = Thing(store=self.store)
        self.assertEqual(t.name, None)
        self.assertEqual(t.location, None)
        self.assertEqual(t.owner, None)



class UserTest(TestCase):


    def setUp(self):
        self.store = Store()


    def test_attrs(self):
        """
        Should have these attributes
        """
        u = User(store=self.store)
        self.assertEqual(u.store, self.store)
        self.assertEqual(u.name, None)


    def test_createAvatar(self):
        """
        Creates a Thing that can act on my behalf in the World
        """
        u = User(store=self.store, name=u'bojimbo')
        a = u.createAvatar()
        
        self.assertIsInstance(a, Thing)
        self.assertEqual(a.store, self.store)
        self.assertEqual(a.name, 'bojimbo')
        actor = IActor(a)
        self.assertEqual(actor.user, u)
        self.assertEqual(actor.thing, a)








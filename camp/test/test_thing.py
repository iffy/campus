from twisted.trial.unittest import TestCase


from axiom.store import Store
from camp.thing import Thing



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



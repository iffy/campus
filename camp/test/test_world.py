from twisted.trial.unittest import TestCase

from axiom import item
from axiom.store import Store
from camp.world import World


class WorldTest(TestCase):


    def setUp(self):
        self.store = Store()


    def test_init(self):
        """
        You can init with a store
        """
        w = World()

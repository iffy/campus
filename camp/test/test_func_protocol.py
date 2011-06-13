from twisted.trial.unittest import TestCase
from twisted.internet import reactor


from camp.protocol import CampFactory



class CampFactoryTest(TestCase):


    def test_runs(self):
        """
        It should start without error
        """
        f = CampFactory()
        p = reactor.listenTCP(9999, f)
        r = p.stopListening()
        return r



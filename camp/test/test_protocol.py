from twisted.trial.unittest import TestCase
from twisted.conch.telnet import TelnetTransport, TelnetBootstrapProtocol
from twisted.conch.insults import insults


from camp.protocol import CampProtocol, bootStrap



class CampProtocolTest(TestCase):


    def test_attrs(self):
        """
        CampProto should know his avatar.
        """
        c = CampProtocol()
        self.assertEqual(c.avatar, None)



class bootStrapTest(TestCase):


    def test_return(self):
        """
        It should return a CampProtocol instance wrapped in Telnet
        """
        o = object()
        f = bootStrap(o)
        self.assertTrue(callable(f))
        
        r = f()
        self.assertTrue(isinstance(r, TelnetTransport))
        self.assertEqual(r.protocolFactory, TelnetBootstrapProtocol)
        self.assertEqual(r.protocolArgs, (insults.ServerProtocol, o))



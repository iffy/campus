from twisted.trial.unittest import TestCase
from twisted.protocols import basic
from twisted.test.proto_helpers import StringTransport

import os

from camp.ui.line import LineProtocol, LineFactory



class LineFactoryTest(TestCase):


    def test_protocol(self):
        """
        Should be LineProtocol by default
        """
        self.assertEqual(LineFactory.protocol, LineProtocol)



class LineProtocolTest(TestCase):


    def test_LineReceiver(self):
        self.assertTrue(issubclass(LineProtocol, basic.LineReceiver))
        self.assertTrue(issubclass(LineProtocol, basic.StatefulStringProtocol))


    def test_attrs(self):
        """
        Should have these attributes
        """
        p = LineProtocol()
        self.assertEqual(p.user, None)
        self.assertEqual(p.avatar, None)
        self.assertEqual(p.state, 'username')
        self.assertEqual(p.delimiter, os.linesep)


    def test_lineReceived(self):
        """
        Should call stringReceived 
        """
        p = LineProtocol()
        called = []
        p.stringReceived = called.append
        
        p.lineReceived('foo')
        self.assertEqual(called, ['foo'])


    def test_init(self):
        """
        should get the username, then try for password
        """
        p = LineProtocol()
        t = StringTransport()
        p.transport = t
        
        r = p.proto_username('foo')
        self.assertEqual(p.username, 'foo')
        self.assertEqual(r, 'password')
        






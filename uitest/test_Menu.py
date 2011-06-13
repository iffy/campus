from twisted.trial.unittest import TestCase
from twisted.conch.insults import insults, window
from twisted.internet import reactor, defer, stdio
from twisted.internet.protocol import Factory
from twisted.python.failure import Failure
from twisted.conch.telnet import TelnetTransport, TelnetBootstrapProtocol
from twisted.protocols import basic


from camp.widget import Menu
from camp.protocol import bootStrap



class TellyProtocol(insults.TerminalProtocol):

    width = 80
    height = 24
    
    def __init__(self, widget):
        insults.TerminalProtocol.__init__(self)
        self.widget = widget


    def _draw(self):
        self.window.draw(self.width, self.height, self.terminal)
    
    
    def _schedule(self, f):
        reactor.callLater(0, f)
    
    
    def _redraw(self):
        self.window.filthy()
        self._draw()


    def connectionMade(self):
        self.window = window.TopWindow(self._draw, self._schedule)
        self.window.addChild(self.widget)
        self.terminalSize(self.width, self.height)
    
    
    def keystrokeReceived(self, keyID, modifier):
        self.window.keystrokeReceived(keyID, modifier)
    
    
    def terminalSize(self, width, height):
        self.width = width
        self.height = height
        self.terminal.eraseDisplay()
        self._redraw()



class InputProtocol(basic.LineReceiver):
    from os import linesep as delimiter
    
    
    def connectionMade(self):
        self.question = None


    def lineReceived(self, line):
        if self.question:
            if line.lower().startswith('n'):
                self.question.errback('User said it failed')
            else:
                self.question.callback(line)
    
    
    def assertYes(self, question):
        self.sendLine(question)
        self.question = defer.Deferred()
        return self.question
        



class MenuTest(TestCase):

    timeout = 60

    port = 9999


    def setUp(self):
        self.factory = Factory()
        self.factory.protocol = None
        self.server = reactor.listenTCP(self.port, self.factory)
        print ''
        print '-' * 30
        print 'telnet to port %s' % self.port
        self.stdio = stdio.StandardIO(InputProtocol())
        self.useri = self.stdio.protocol
    
    
    def tearDown(self):
        self.useri.transport.loseConnection()
        return self.server.stopListening()


    def test_visible(self):
        """
        The menu should be display.
        """
        opts = ['foo', 'bar', 'baz']
        m = Menu(opts, lambda x:None)
        self.factory.protocol = bootStrap(lambda: TellyProtocol(m))
        return self.useri.assertYes('Did a menu appear with options %s?' % ', '.join(opts))
    
    
    def test_selecting(self):
        """
        You should be able to choose an item.
        """
        d = defer.Deferred()
        def cb(what):
            self.assertEqual(what, 'foo')
            proto.terminal.loseConnection()
            d.callback(True)
        opts = ['foo', 'bar', 'baz']
        m = Menu(opts, cb)
        proto = TellyProtocol(m)
        self.factory.protocol = bootStrap(lambda: proto)
        self.useri.sendLine('Press 1')
        return d






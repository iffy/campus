from twisted.internet import reactor
from twisted.python import log
from axiom.store import Store
from camp.ui.line import LineFactory

import sys
log.startLogging(sys.stdout)

store = Store()

f = LineFactory()

reactor.listenTCP(9002, f)
reactor.run()
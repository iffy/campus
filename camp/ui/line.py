"""
Line-by-line protocols.
"""

import os

from twisted.internet.protocol import Factory
from twisted.protocols import basic
from twisted.python import log



class LineProtocol(basic.LineReceiver, basic.StatefulStringProtocol):
    
    user = None
    avatar = None
    delimiter = os.linesep
    state = 'username'
    
    def connectionMade(self):
        self.transport.write('username: ')


    def lineReceived(self, line):
        self.stringReceived(line)


    def proto_username(self, username):
        self.username = username
        self.setRawMode()
        self.transport.write('password: ')
        return 'password'


    def proto_password(self, password):
        self.password = password
        self.setLineMode()
        return 'foo'



class LineFactory(Factory):
    
    protocol = LineProtocol

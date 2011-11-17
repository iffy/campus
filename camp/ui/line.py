"""
Line-by-line protocols.
"""

import os

from twisted.protocols import basic



class LineProtocol(basic.LineReceiver, basic.StatefulStringProtocol):
    
    user = None
    avatar = None
    delimiter = os.linesep
    state = 'username'
    

    def lineReceived(self, line):
        self.stringReceived(line)


    def proto_username(self, username):
        self.username = username
        return 'password'



class LineFactory:
    
    protocol = LineProtocol

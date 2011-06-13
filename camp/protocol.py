from twisted.internet.protocol import Factory
from twisted.conch.telnet import TelnetTransport, TelnetBootstrapProtocol
from twisted.conch.insults import insults



def bootStrap(protocol):
    """
    I return a telnet-bootstrapped version of the given protocol.
    """
    def f():
        return TelnetTransport(TelnetBootstrapProtocol,
            insults.ServerProtocol,
            protocol)
    return f



class CampProtocol:
    """
    I am the main Camp protocol
    """
    
    avatar = None



class CampFactory(Factory):
    """
    I am a factory.
    """
    
    protocol = bootStrap(CampProtocol)



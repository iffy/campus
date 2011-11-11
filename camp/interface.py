from zope.interface import Interface, Attribute


class IContainment(Interface):
    """
    For powering up things to have containment.
    """
    
    thing = Attribute('''The thing with the powerup''')
    
    def getContents():
        """
        Get the contents of the container.
        """
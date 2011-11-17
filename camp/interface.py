"""
Interfaces for powering up Things
"""

from zope.interface import Interface, Attribute



class IContainer(Interface):
    """
    For things that support containment.
    """


    def getContents():
        """
        Returns an iterable of my contents.
        """



class IUseable(Interface):
    """
    For things that support the Use action.
    """
    
    def use(who):
        """
        Use the thing.
        """


class IActor(Interface):
    """
    For things that can act.
    """




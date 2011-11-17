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
"""
"""


from axiom.item import Item
from axiom import attributes



class Thing(Item):
    """
    I am something.
    """
    
    name = attributes.text()
    location = attributes.reference()
    owner = attributes.reference()
from twisted.trial.unittest import TestCase
from zope.interface.verify import verifyClass


from camp.event import IEvent, Entrance


class Fake:
    
    
    def __init__(self, name):
        self.name = name



class EntranceTest(TestCase):


    def test_IEvent(self):
        verifyClass(IEvent, Entrance)


    def test_init(self):
        """
        Entrance involves a who and a where
        """
        who = object()
        where = object()
        e = Entrance(who, where)
        self.assertEqual(e.who, who)
        self.assertEqual(e.where, where)

    
    def test_describe(self):
        """
        From the perspective of the two parties or another observer.
        """
        actor = Fake('actor')
        room = Fake('room')
        e = Entrance(actor, room)
        
        self.assertEqual(e.describe(actor), ("You entered %(location)s.",
                                            {'location': 'room'}))
        self.assertEqual(e.describe(room), ("%(who)s entered you.",
                                           {'who': 'actor'}))
        self.assertEqual(e.describe('foo'), ('%(who)s entered %(location)s.',
                                            {'who': 'actor',
                                             'location': 'room'}))



        


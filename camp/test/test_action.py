from twisted.trial.unittest import TestCase


from camp.action import Action, Use


class Fake:
    pass


class UseTest(TestCase):


    def test_init(self):
        """
        Should take the actor and the thing being used.
        """
        user = object()
        used = object()
        a = Use(user, used)
        self.assertEqual(a.user, user)
        self.assertEqual(a.used, used)


    def test_call(self):
        """
        Should call the .use method on used with user as the argument.
        """
        user = object()
        used = Fake()
        
        called = []
        used.use = lambda u: called.append(u)
        
        a = Use(user, used)
        a()
        self.assertEqual(called, [user], "Should have called used.use(user)")





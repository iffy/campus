from twisted.trial.unittest import TestCase
from twisted.conch.insults import window

from camp.widget import MainWindow



class MainWindowTest(TestCase):


    def test_TopWindow(self):
        self.assertTrue(issubclass(MainWindow, window.TopWindow))


    def test_setBody(self):
        """
        You can set the body of the window
        """
        w = MainWindow(lambda:None, lambda x:None)
        o = window.Widget()
        w.setBody(o)
        self.assertEqual(w.body, o)
        self.assertIn(o, w.vbox.children)
    
    
    def test_setBody_displaces(self):
        """
        Setting the body should displace the other body
        """
        w = MainWindow(lambda:None, lambda x:None)
        a = window.Widget()
        w.setBody(a)
        
        b = window.Widget()
        w.setBody(b)
        self.assertEqual(w.body, b)
        self.assertIn(b, w.vbox.children)
        self.assertNotIn(a, w.vbox.children)



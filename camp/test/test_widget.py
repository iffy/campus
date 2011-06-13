from twisted.trial.unittest import TestCase
from twisted.conch.insults import window

from camp.widget import MainWindow, Menu



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



class MenuTest(TestCase):

    
    def test_Widget(self):
        self.assertTrue(issubclass(Menu, window.Widget))


    def test_inputs(self):
        """
        Pressing inputs calls the passed in function.
        """
        called = []
        m = Menu(['foo', 'bar', 'baz'], called.append)
        m.characterReceived('2', None)
        self.assertEqual(called, ['bar'])
        
        called.pop()
        m.characterReceived('0', None)
        self.assertEqual(called, [])
        
        m.characterReceived('4', None)
        self.assertEqual(called, [])


    def test_moreThan10(self):
        """
        Menus are paged if there are more than 9 items
        """
        called = []
        m = Menu(range(1, 16), called.append)
        m.func_RIGHT_ARROW(None)
        m.characterReceived('1', None)
        self.assertEqual(called, [10])
        called.pop()
        
        m.func_RIGHT_ARROW(None)
        m.characterReceived('1', None)
        self.assertEqual(called, [10],
            "You shouldn't allow paging beyond the last element")
        called.pop()
        
        m.func_LEFT_ARROW(None)
        m.characterReceived('1', None)
        self.assertEqual(called, [1])
        called.pop()
        
        m.func_LEFT_ARROW(None)
        m.characterReceived('1', None)
        self.assertEqual(called, [1])






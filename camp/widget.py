from twisted.conch.insults import window


class MainWindow(window.TopWindow):
    """
    I am the main window that is displayed to connected users.
    
    +------------+
    | status_bar |
    +------------+
    | body       |
    |            |
    |            |
    +------------+
    """
    
    body = None
    
    
    def __init__(self, *args, **kwargs):
        window.TopWindow.__init__(self, *args, **kwargs)
        
        self.vbox = window.VBox()
        self.addChild(self.vbox)
    
    
    def setBody(self, body):
        """
        Sets the main body to the given widget.
        """
        if self.body:
            self.vbox.remChild(self.body)
        self.body = body
        self.vbox.addChild(self.body)


class Menu(window.Widget):
    """
    I am a menu for choosing between options.
    """

    size = 9


    def __init__(self, sequence, callback):
        """
        @param sequence: A finite list of strings to display as options
        @type sequence: iterable
        
        @param callback: The function that will be called with a menu item
            is chosen
        @type callback: C{callable}
        """
        window.Widget.__init__(self)
        self.pages = []
        for i in xrange(0, len(sequence), self.size):
            self.pages.append(tuple(sequence[i:i+self.size]))
        self.callback = callback
        self.page = 0
    
    
    def characterReceived(self, keyID, modifier):
        """
        Respond to a character being pressed.
        """
        page = self.pages[self.page]        
        index = int(keyID) - 1
        if index >= 0 and index < len(page):
            self.callback(page[index])


    def func_RIGHT_ARROW(self, modifier):
        """
        Respond to right arrow
        """
        self.page += 1
        if self.page >= len(self.pages):
            self.page -= 1
    
    
    def func_LEFT_ARROW(self, modifier):
        """
        Respond to left arrow
        """
        self.page -= 1
        if self.page < 0:
            self.page = 0
    
    
    def render(self, width, height, terminal):
        """
        Show the current page
        """
        page = self.pages[self.page]
        
        for i, item in enumerate(page):
            terminal.cursorPosition(0, i)
            terminal.write(item)



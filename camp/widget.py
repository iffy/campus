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

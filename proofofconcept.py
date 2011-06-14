from twisted.internet import reactor, defer, task
from twisted.internet.protocol import Factory
from twisted.conch.telnet import TelnetTransport, TelnetBootstrapProtocol
from twisted.conch.insults import insults, window
from twisted.conch.insults.text import flatten, attributes as A
from twisted.conch.insults.helper import CharacterAttribute
from twisted.python import text as tptext
from twisted.internet.protocol import ProcessProtocol
import random





def bootStrap(protocol):
    """
    I return a telnet-bootstrapped version of the given protocol.
    """
    def f():
        return TelnetTransport(TelnetBootstrapProtocol,
            insults.ServerProtocol,
            protocol)
    return f


def timestables():
    r = random.Random()
    a = r.randint(99,9999)
    b = r.randint(99,9999)
    p = '''\
%19d
%19d  *
--------
''' % (a, b)
    s = a*b
    return p, s


def goodjob(a):
    return 'swell'


class CampProtocol(insults.TerminalProtocol):

    avatar = None

    width = 80
    height = 24


    def _draw(self):
        self.window.draw(self.width, self.height, self.terminal)


    def _schedule(self, f):
        reactor.callLater(0, f)


    def _redraw(self):
        self.window.filthy()
        self._draw()


    def terminalSize(self, width, height):
        self.width = width
        self.height = height
        self.terminal.eraseDisplay()
        self._redraw()


    def connectionMade(self):
        self.terminal.eraseDisplay()
        self.terminal.resetPrivateModes([insults.privateModes.CURSOR_MODE])
        self.window = MainWindow(self._draw, self._schedule)

        self.avatar = User()
        self.avatar.protocol = self

        self.avatar.moveTo(lobby)

        self.terminalSize(self.width, self.height)


    def keystrokeReceived(self, keyID, modifier):
        self.window.keystrokeReceived(keyID, modifier)



class CampFactory(Factory):

    protocol = bootStrap(CampProtocol)



class StatusBar(window.HBox):
    """
    I am a one-line status bar
    """

    def __init__(self):
        window.HBox.__init__(self)

        self.location = window.TextOutput()
        self.message = window.TextOutput()
        self.annoy = window.TextOutput()

        self.addChild(self.location)
        self.addChild(self.message)
        self.addChild(self.annoy)


    def sizeHint(self):
        return None, 1


    def setLocation(self, location):
        if type(location) in [str, unicode]:
            self.location.setText(location)
        else:
            self.location.setText(location.name)


    def setMessage(self, msg):
        self.message.setText(msg)


    def startAnnoying(self):
        self.annoy.setText('\x1b[5;1m***\x1b[0m')


    def stopAnnoying(self):
        self.annoy.setText('')


    def focusReceived(self):
        raise window.YieldFocus()




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

        self.status_bar = StatusBar()
        self.status_bar.setLocation('???')
        self.status_bar.stopAnnoying()
        self.vbox.addChild(window.Border(self.status_bar))


    def keystrokeReceived(self, keyID, modifier):
        window.TopWindow.keystrokeReceived(self, keyID, modifier)


    def setBody(self, body):
        """
        Sets the main body to the given widget.
        """
        for child in self.vbox.children[1:]:
            child.focusLost()
            self.vbox.remChild(child)
            if hasattr(child, 'discard'):
                child.discard()
        self.vbox.focusedChild = None

        self.body = body
        self.vbox.addChild(body)
        if not self.vbox.focusedChild:
            self.vbox.focusedChild = self.vbox.children[1]
        if not self.focusedChild:
            self.focusedChild = self.vbox



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
        self.sequence = list(sequence)
        self.callback = callback
        self.pages = []
        self.page = 0
        self.makePages()


    def makePages(self):
        self.pages = []
        for i in xrange(0, len(self.sequence), self.size):
            self.pages.append(tuple(self.sequence[i:i+self.size]))
        while self.page >= len(self.pages) and self.page != 0:
            self.page -= 1


    def characterReceived(self, keyID, modifier):
        """
        Respond to a character being pressed.
        """
        if keyID in 'nN':
            self.func_RIGHT_ARROW(modifier)
        elif keyID in 'pP':
            self.func_LEFT_ARROW(modifier)
        elif keyID in '123456789':
            page = self.pages[self.page]
            index = int(keyID) - 1
            if index >= 0 and index < len(page):
                self.callback(page[index])


    def addOption(self, option):
        self.sequence.append(option)
        self.makePages()
        self.repaint()


    def remOption(self, option):
        self.sequence.remove(option)
        self.makePages()
        self.repaint()


    def func_RIGHT_ARROW(self, modifier):
        """
        Respond to right arrow
        """
        self.page += 1
        if self.page >= len(self.pages):
            self.page -= 1
        self.repaint()


    def func_LEFT_ARROW(self, modifier):
        """
        Respond to left arrow
        """
        self.page -= 1
        if self.page < 0:
            self.page = 0
        self.repaint()


    def func_UP_ARROW(self, modifier):
        self.func_LEFT_ARROW(modifier)


    def func_DOWN_ARROW(self, modifier):
        self.func_RIGHT_ARROW(modifier)


    def render(self, width, height, terminal):
        """
        Show the current page
        """
        page = self.pages[self.page]

        for i, item in enumerate(page):
            terminal.cursorPosition(0, i)
            text = '(%s) %s' % (i+1, item.getName())
            text += ' ' * (width - len(text))
            terminal.write(text)

        n = len(page)
        terminal.cursorPosition(0, n)
        text = '    page %s/%s' % (self.page+1, len(self.pages))
        terminal.write(text + (' ' * (width - len(text))))

        for i in xrange(n+1, height):
            terminal.cursorPosition(0, i)
            terminal.write(' '*width)


    def __repr__(self):
        return 'Menu(%r)' % self.pages



class ClearingTextOutputArea(window.TextOutputArea):


    def render(self, width, height, terminal):
        n = 0
        inputLines = self.text.splitlines()
        outputLines = []
        while inputLines:
            if self.longLines == self.WRAP:
                wrappedLines = tptext.greedyWrap(inputLines.pop(0), width)
                outputLines.extend(wrappedLines or [''])
            else:
                outputLines.append(inputLines.pop(0)[:width])
            if len(outputLines) >= height:
                break
        for n, L in enumerate(outputLines[:height]):
            terminal.cursorPosition(0, n)
            terminal.write(L + (' ' * (width - len(L))))
        for n in xrange(len(outputLines), height):
            terminal.cursorPosition(0, n)
            terminal.write(' ' * width)


class Dialog(window.VBox):

    def __init__(self, text, okFunc):
        window.ContainerWidget.__init__(self)

        tout = ClearingTextOutputArea()
        tout.setText(text)

        ok = window.Button('OK', okFunc)

        self.addChild(window.Border(tout))
        self.addChild(window.Border(ok))
        self.changeFocus()



class Form(window.VBox):
    """
    I am a form you can fill out
    """

    def __init__(self, fieldnames, values=None):
        window.VBox.__init__(self)

        self.done = defer.Deferred()

        self.values = values or {}
        self.fieldnames = fieldnames

        for name in fieldnames:
            label = window.TextOutput((None, 1))
            label.setText('\x1b[1m' + name + ':\x1b[0m')
            field = window.TextInput(30, self.getInput)
            val = values.get(name, '')
            if val is None:
                val = ''
            elif type(val) not in [str, unicode]:
                val = str(val)
            field.setText(val)
            field.label = name
            self.addChild(label)
            self.addChild(field)

        self.addChild(window.Border(window.Button('OK', self.okFunc)))

    def getInput(self, value):
        key = self.focusedChild.label
        self.values[key] = value


    def okFunc(self):
        self.done.callback(self.values)



class Thing:

    location = None
    name = None
    description = None


    def __init__(self):
        self.views = []


    def moveTo(self, location):
        oldLocation = self.location
        if oldLocation:
            oldLocation.removeThing(self)
        location.addThing(self)
        assert self.location == location


    def getView(self, user):
        def okFunc():
            user.lookAt(user.location)
        text = self.getName() + '\n\n' + self.getDescription()
        w = Dialog(text, okFunc)
        w.discard = self.getDiscard(w)
        self.views.append(w)
        return w


    def setName(self, name):
        self.name = name
        for view in self.views:
            view.setText(self.name)


    def getName(self):
        if self.name:
            return self.name
        return '%s %x' % (self.__class__.__name__, id(self))


    def getDescription(self):
        if self.description:
            return self.description
        return 'No description :('


    def getDiscard(self, view):
        def f():
            self.views.remove(view)
        return f


    def __repr__(self):
        return self.getName()



class Room(Thing):

    def __init__(self, name=None):
        Thing.__init__(self)
        self.contents = []
        self.name = name


    def moveTo(self, location):
        pass


    def addThing(self, thing):
        if thing not in self.contents:
            self.contents.append(thing)
            for view in self.views:
                view.addOption(thing)
        thing.location = self


    def removeThing(self, thing):
        if thing in self.contents:
            self.contents.remove(thing)
            for view in self.views:
                view.remOption(thing)


    def getView(self, viewer):
        m = Menu(self.contents, viewer.actOn)
        m.discard = self.getDiscard(m)
        self.views.append(m)
        return m



class Exit(Thing):

    def __init__(self, destination):
        Thing.__init__(self)
        self.destination = destination


    def getName(self):
        return self.destination.getName()


class ResolveDispute(Thing):
    solution = lambda *a:defer.succeed(None)
    getproblem = lambda *a:defer.succeed(('''1+1 = ?''', 2))
    name = 'Resolve Dispute'

    def __init__(self, getproblem=None, solution=None):
        if getproblem is not None:
            self.getproblem = getproblem
        if solution is not None:
            self.solution = solution


    def getView(self, viewer):
        self.viewer = viewer
        log.msg('viewer for ResolveDispute %r' % viewer)
        v = window.VBox()
        c = self.c = ClearingTextOutputArea()
        field = window.TextInput(30, self.getInput)
        d = defer.maybeDeferred(self.getproblem)
        def cb(a):
            self.answer = a[1]
            self.question = a[0]
            return self.question
        d.addCallback(cb)
        d.addCallback(c.setText)
        v.addChild(c)
        v.addChild(field)
        v.changeFocus()
        return v

    def getInput(self, msg):
        if str(msg).strip() == str(self.answer).strip():
            self.solution(self)
            self.c.setText(self.c.text + '   ........... CORRECT')
            task.deferLater(reactor, 1.0, self.viewer.lookAt, self.viewer.location)





class User(Thing):

    protocol = None

    def moveTo(self, location):
        Thing.moveTo(self, location)
        self.protocol.window.status_bar.setLocation(self.location)
        self.lookAt(self.location)


    def lookAt(self, thing):
        w = thing.getView(self)
        if w:
            self.protocol.window.setBody(w)


    def actOn(self, thing):
        if isinstance(thing, Exit):
            self.moveTo(thing.destination)
        else:
            self.lookAt(thing)


    def getView(self, user):
        if user is not self:
            return Thing.getView(self, user)

        f = Form(['name', 'description'],
            {'name': self.name,
            'description': self.description})
        def cb(values):
            self.setName(values['name'])
            self.description = values['description']
            self.lookAt(self.location)
        f.done.addCallback(cb)
        return f



lobby = Room('The Lobby')
hr = Room('Human Resource')
furnace = Room('Furnace Room')
maze = Room('Maze')
tt = Room('Times Tables')

firepit = Thing()
firepit.name = 'fire pit'
firepit.description = 'This is a raging fire pit.  Don\'t touch it.'

r = ResolveDispute(timestables, goodjob)
r.name = 'Turning back times tables'

lobby.addThing(Exit(hr))
lobby.addThing(Exit(tt))

hr.addThing(Exit(lobby))
hr.addThing(Exit(furnace))

furnace.addThing(Exit(lobby))
furnace.addThing(firepit)
furnace.addThing(Exit(maze))

maze.addThing(Exit(maze))

tt.addThing(r)
tt.addThing(Exit(lobby))



if __name__ == '__main__':
    import sys
    from twisted.python import log
    log.startLogging(sys.stdout)
    f = Factory()
    f.protocol = bootStrap(CampProtocol)
    reactor.listenTCP(9099, f)
    reactor.run()

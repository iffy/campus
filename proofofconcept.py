from twisted.internet import reactor, defer, task, stdio
from twisted.internet.protocol import Factory
from twisted.conch.telnet import TelnetTransport, TelnetBootstrapProtocol
from twisted.conch.insults import insults, window
from twisted.conch.insults.text import flatten, attributes as A
from twisted.conch.insults.helper import CharacterAttribute
from twisted.python import text as tptext
from twisted.internet.protocol import ProcessProtocol
import random, sys, termios, tty, os
from twisted.python.usage import Options, UsageError
from twisted.python import log


def runWithProtocol(klass):
    fd = sys.__stdin__.fileno()
    oldSettings = termios.tcgetattr(fd)
    tty.setraw(fd)
    try:
        p = insults.ServerProtocol(klass)
        stdio.StandardIO(p)
        reactor.run()
    finally:
        termios.tcsetattr(fd, termios.TCSANOW, oldSettings)
        os.write(fd, "\r\x1bc\r")


def bootStrap(protocol):
    """
    I return a telnet-bootstrapped version of the given protocol.
    """
    def f():
        return TelnetTransport(TelnetBootstrapProtocol,
            insults.ServerProtocol,
            protocol)
    return f

def ndigitrandom(digits=2, num=2):
    r = random.Random()
    h = (10 ** digits) -1
    l = 10 ** (digits-1)
    res = []
    for i in xrange(num):
        res.append(r.randint(l, h))
    if len(res) == 1:
        return res[0]
    return res

def boxyproblem(a, b, operation='*'):
    p = '''\
%19d
%19d  %s
--------
''' % (a, b, operation)
    s = eval(str(a) + ' ' + operation + ' ' + str(b))
    return p, s


def elevens(digits=2):
    a = ndigitrandom(digits=digits, num=1)
    b = 11
    return boxyproblem(a, b)


def addition(digits=2):
    a, b = ndigitrandom(digits=digits)
    return boxyproblem(a, b, '+')


def subtraction(digits=2):
    a, b = ndigitrandom(digits=digits)
    if b > a:
        return boxyproblem(b, a, '-')
    return boxyproblem(a, b, '-')


def complements(n=100):
    a = ndigitrandom(digits=2, num=1)
    p = 'x + %d = %d' % (a, n)
    s = n - a
    return p, s

def mult2x1():
    b = ndigitrandom(digits=2, num=1)
    a = ndigitrandom(digits=1, num=1)
    return boxyproblem(a, b)

def mult3x1():
    b = ndigitrandom(digits=3, num=1)
    a = ndigitrandom(digits=1, num=1)
    return boxyproblem(a, b)


def mult2x2_same_sum10():
    a = ndigitrandom(digits=2, num=1)
    tens = (a/10) * 10
    ones = a - tens
    b = tens + ones
    return boxyproblem(a, b)


def squared(digits=2):
    b = ndigitrandom(digits=2, num=1)
    return '%d^2' % b, b**2


def squared2x2_endswith_5():
    r = random.Random()
    a = r.choice(range(15, 95, 10))
    return '%d^2' % a, a**2


class Magic:
    def __init__(self):
        self.finished = set()
        
    def __call__(self):
        return self.magic()
        
    def magic(self):
        r = random.Random()
        a = [elevens, addition, subtraction, complements, mult2x1,
             mult3x1, mult2x2_same_sum10, squared, squared2x2_endswith_5]
        m = r.choice(a)
        res = m()
        while res in self.finished:
            log.msg('Already did that one')
            res = m()
        self.finished.add(res)
        return res
         

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


def nameThatAnimal():
    animals = ['duck', 'cat', 'dog', 'cow', 'chicken', 'gorilla',
        'asdf', 'eggplant', 'kitchen']
    animal = random.choice(animals)
    return "It looks like a %s.  What is it?" % animal, animal


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


class LastLinesViewer(window.TextOutputArea):

    def __init__(self):
        window.TextOutputArea.__init__(self)
        self.lines = []

    def setLines(self, lines):
        self.lines = lines


    def render(self, width, height, terminal):
        n = 0
        inputLines = self.lines[-height:]
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

    def __init__(self, fieldnames, values=None, otherinfo=None):
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
        
        if otherinfo:
            o = ClearingTextOutputArea()
            o.setText(otherinfo)
            self.addChild(window.Border(o))

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



class Chat(Thing):

    def __init__(self):
        Thing.__init__(self)
        self.sharedoutput = []
        self.history = []


    def getView(self, viewer):
        vbox = window.VBox()
        c = LastLinesViewer()
        self.sharedoutput.append(c)
        self.displayLine(viewer.getName() + ' joined')
        inputline = window.TextInput(40, self.makeListener(vbox,
                                                         viewer))
        vbox.addChild(c)
        vbox.addChild(inputline)
        return vbox
    
    
    def displayLine(self, line):
        self.history.append(line)
        if len(self.history) > 10000:
            self.history = self.history[-10000:]
        for v in self.sharedoutput:
            v.setLines(self.history)
            v.repaint()


    def makeListener(self, vbox, viewer):
        def f(msg):
            if str(msg).strip() == 'q':
                viewer.lookAt(viewer.location)
                self.displayLine(viewer.getName() + ' has left')
            else:
                log.msg(msg)
                text = '<' + viewer.getName() + '> ' + msg
                inputline = vbox.children[1]
                inputline.setText('')
                self.displayLine(text)
        return f


class DisputationArena(Thing):

    getproblem = lambda *a:defer.succeed(('''1+1 = ?''', 2))
    question = None
    answer = None
    accepting_answers = False
    name = 'Resolve Dispute'

    def __init__(self, getproblem=None):
        Thing.__init__(self)
        if getproblem is not None:
            self.getproblem = getproblem
        self.getNewProblem()

    def getView(self, viewer):
        v = window.VBox()
        c = ClearingTextOutputArea()
        field = window.TextInput(30, self.makeListener(v, viewer))
        v.addChild(c)
        v.addChild(field)
        
        if self.question:
            c.setText(self.question)
        
        v.changeFocus()
        v.discard = self.getDiscard(v)
        self.views.append(v)
        return v

    def makeListener(self, view, viewer):
        def f(msg):
            self.gotAnswer(view, viewer, msg)
        return f

    def getNewProblem(self):
        d = defer.maybeDeferred(self.getproblem)
        d.addCallback(self.gotProblem)


    def gotProblem(self, problem):
        self.question = problem[0]
        self.answer = problem[1]
        for view in self.views:
            view.children[0].setText(self.question)
            view.children[1].setText('')
        self.accepting_answers = True

    def gotAnswer(self, view, user, answer):
        if str(answer).strip() == 'q':
            user.lookAt(user.location)
        elif str(answer).strip() == str(self.answer).strip():
            if not self.accepting_answers:
                return
            self.accepting_answers = False
            points = len(self.views) - 1
            for v in self.views:
                if v is view:
                    v.children[0].setText(self.question + '\nCORRECT: %s points' % points)
                    user.points += points
                else:
                    v.children[0].setText(self.question + '\nToo slow! %s got it first' % user.getName())
            reactor.callLater(2, self.getNewProblem)





class User(Thing):

    protocol = None
    points = 0

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
    
    
    def getDescription(self):
        return Thing.getDescription(self) + '\n%d points' % self.points


    def getView(self, user):
        if user is not self:
            return Thing.getView(self, user)

        f = Form(['name', 'description'],
            {'name': self.name,
            'description': self.description},
            'Points: %s' % self.points)
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
tt = Room('Arenas')
irc = Room('Talk to a representative')

firepit = Thing()
firepit.name = 'fire pit'
firepit.description = 'This is a raging fire pit.  Don\'t touch it.'

magic = Magic()
r = DisputationArena(magic)
r.name = 'No paper no pencil no problem Math Arena (http://goo.gl/krdAE)'

r2 = DisputationArena(nameThatAnimal)
r2.name = 'Name that Animal arena'

chatty = Chat()
chat2 = Chat()
chat2.name = 'other chat room'

lobby.addThing(Exit(hr))
lobby.addThing(Exit(tt))
lobby.addThing(Exit(irc))

hr.addThing(Exit(lobby))
hr.addThing(Exit(furnace))

furnace.addThing(Exit(lobby))
furnace.addThing(firepit)
furnace.addThing(Exit(maze))

maze.addThing(Exit(maze))

tt.addThing(Exit(lobby))
tt.addThing(r)
tt.addThing(r2)

irc.addThing(Exit(lobby))
irc.addThing(chatty)
irc.addThing(chat2)

class MainOptions(Options):
    def getSynopsis(self):
        return """%s [options] """ % __file__

    optFlags = [('foreground', 'f', 'Run in the foreground')]



def main(argv):
    opt = MainOptions()
    try:
        opt.parseOptions(argv[1:])
    except UsageError, e:
        raise SystemExit(str(e))
    if opt['foreground']:
        runWithProtocol(CampProtocol)
    else:
        log.startLogging(sys.stdout)
        f = Factory()
        f.protocol = bootStrap(CampProtocol)
        reactor.listenTCP(9099, f)
        reactor.run()


if __name__ == '__main__':
    main(sys.argv)

"""


+----------------+
| Lobby          |
+----------------+
| 1 Accounting   |
+----------------+
| I inventory    |
| R room         |
+----------------+


Press 1


+----------------------------+
| Accounting                 |
+----------------------------+
| 1 Lobby                    |
| 2 copy machine             |
| 3 Dungeon                  |
+----------------------------+
| I inventory                |
| R room                     |
+----------------------------+


Exit
    create
    destroy
    copy
    move
    close
    lock
    unlock


Room
    create <thing>
    destroy
    view
    rename


User
    view
    talk
    send to
    kick
    mute


Reimbursement form
    view
    edit
    move
    copy
    destroy


Box
    put
    destroy
    view
    lock
    unlock




A user's actions can:
    - Change the widget a protocol has loaded
    - Alter some information on a widget
    - Change an object
    - Create an object
    - Destroy an object
    - Spawn a process
    - Make an object do something


"""

from twisted.internet import reactor

from axiom.store import Store
from axiom import item, attributes


store = Store('tmpstore.db')

if __name__ == '__main__':
    reactor.run()


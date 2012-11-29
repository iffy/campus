======
campus
======

You are in your basement making yet another webapp

::
    
    look webapp

The webapp is a mess of spaghetti.  The Javascript has spilled and the style sheets are cascading off your desk.

::

    say web 2.0 buzzword

You die.  You are in heaven.

::

    look

You are surrounded by people using their keyboards -- there's no mouse in sight.



Features that would be cool
===========================

- Allow rooms to be distributed between processes (and servers).
- Allow for outside sources of data to easily provide data to the campus
- Allow for sending data from the campus to the outside world
- pastebin
- image/video/html pastebin
- chat
- programmable robots
- permissions


Design
======

It could look like this.  Each box is a process (running on the same machine or
not):

::

                                                                      +------------+
                             +----------------------------------------+ db         |
                             |                                        |            |
                             |                                        +------------+
                             |                                        | git repo   |
                             |api                                     |            |
                             v                                        +------------+
        +--------+  +-----------------+   +-----------------+         | irc channel|
        | web    |  |  world          |   |  workers        |         |            |
        | ui     +--+                 |   |                 |         +------------+
        |        |  |                 +---+                 |         | mailserver |
        |        |  |                 |   |                 +--------->            |
        +--------+  |                 |   |                 |         +------------+
        | ssh    |  |                 |   |                 |
        | ui     +--+                 |   |                 |
        +--------+  +-----------------+   +-----------------+


Or maybe the world/workers have an API that allows for sending and receiving
messages that even the UIs use.


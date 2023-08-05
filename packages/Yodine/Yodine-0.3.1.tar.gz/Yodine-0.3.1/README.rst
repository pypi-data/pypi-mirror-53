######
Yodine
######

Briefly put, Yodine is a special, flexible, fun, easily extensible game, written in Python, with advanced plugin support,
that uses pyglet and an involved Entity-Component-System infrastructure.

It is easy to write plugins for Yodine. And it is easy to *feel the structure*. (Just don't let the cows do so. They're evil
monsters.)

**Notice: the game is currently in a development stage. Expect bugs and a lack of features.**



How to play
***********

In order to install the game, simply run:

..  code:: bash

    pip install yodine


Running it is quite simple, too:

..  code:: bash

    python -m yodine.launcher



Writing Plugins
===============

In order to write a plugin for Yodine, you may run the following module:

..  code:: bash

    python -m yodine.utils.plugin_init

After answering a few questions, a generous, helpful filesystem structure will be generated. The files are
heavily commented, to aid you in your quest to add to the game. Let's build a castle?



Editing Maps
============

In order to create or edit a map for Yodine, simply run:

..  code:: bash

    python -m yodine.editor my_map.save.json



Hosting Servers
===============

In order to host a server for Yodine, run the following:

..  code:: bash

    YODINE_DEDICATED=y YODINE_LISTEN=8081 python -m yodine my_map.save.json

Of course, replace the :code:`8081` in :code:`YODINE_LISTEN=8081` by the desired listen port. The standard
*should* be 8081, but since the default is not listening at all, there is unfortunately no obvious
way to tell that.

License
*******

This project and its source code are available under [the MIT license](https://opensource.org/licenses/MIT),
under the autorship of Gustavo Ramos Rehermann (:code:`rehermann6046@gmail.com`).
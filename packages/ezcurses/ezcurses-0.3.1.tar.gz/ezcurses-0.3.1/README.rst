ezcurses
========

library to help with curses programming (Python 3.3+ compatible)

Installation
------------

From the project root directory::

    $ python setup.py install

Usage
-----

The easiest method is to just decorate your function, and use the injected ``scr`` argument::

    from time import sleep
    from ezcurses import curse

    @curse
    def main(scr, message_string):
        w, h = scr.max_size()
        scr.write(message_string, pos=(w // 2, h // 2))
        scr.refresh()
        sleep(1)

    if __name__ == '__main__':
        main('Hello world!')


You can also use the Cursed context manager.
Here's an example with windows with backgrounds and borders and colors::

    from ezcurses import Cursed

    with Cursed() as scr:
        w, h = scr.max_size()
        win1 = scr.new_win(orig=(0, 0), size=(20, 20))
        win2 = scr.new_win(orig=(20, 0), size=(20, 20))
        win1.border()
        win2.border()
        win1.background('+', color='red')
        win2.background('.', color=('green', 'blue'))
        win1.refresh()
        win2.refresh()
        s = win1.getstr((1, 1), echo=True)
        win2.write(s, (1, 1), color=('red', 'black'))
        win2.refresh()
        win1.write('Press q to quit', (1, 1), color=('black', 'red'))
        while win1.getkey() != 'q':
            pass

Release Notes
-------------

:0.2.12:
  - Add windows support with unicurses
:0.2.11:
  - Readme example was bad
:0.2.10:
  - Add multi_menu feature for selections spanning a screen
:0.2.9:
  - Rename _msgs to Menu.items
:0.2.8:
  - Much more intricate menu logic and new multi_menu.py example
:0.2.7:
  - Fix menu origin in windows bug
:0.2.6:
  - Make layout creatable with ``Screen.new_layout(border=True)``
:0.2.5:
  - Add Layout feature for bootstrap like rows and columns
:0.2.4:
  - Add Menu functionality and an example in examples/menu_example.py
:0.2.3:
  - make it much more tolerable for floats, if user does math stuff
:0.2.2:
  - add ``curse`` decorator
  - rename main context manager to ``Cursed``
:0.2.1:
  - fixed a few bugs in window without size
:0.2.0:
  - lots of clean up and testing, fix README
:0.1.2:
  - Make positional optional and a keyword ``pos`` for the ``getstr`` function
  - Add documentation to API
:0.1.1:
  - Make position optional for ``write`` and default (0, 0) like other funcs
:0.1.0:
  - New features for curses windows
  - get input, string and characters
  - add strings with colors to the window
  - add borders
  - draw lines
  - change background
  - very functional as is
:0.0.1:
  - Project created

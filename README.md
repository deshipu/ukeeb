A minimal USB keyboard library for CircuitPython
================================================

Copy the file ``ukeeb.py`` to your board. Then copy the ``boot.py`` from
``examples`` and adjust pins and desired HID devices, then create a ``code.py``
file using one of the example boards.

By default the keyboard will only come up as USB HID keyboard, but if you hold
down the key on the intersection of column and row specified in ``boot.py``,
while connecting it, the ``CIRCUITPY`` drive and serial ``REPL`` will become
available.

A minimal USB keyboard library for CircuitPython
================================================

Copy the files `ukeeb.py`, `boot.py` and `main.py` to the root of your
board, and then create a file `matrix.py` for your particular board based
on the examples.

By default the keyboard will only come up as USB HID keyboard, but if you hold
down the key on the first row and first column while connecting it, the
``CIRCUITPY`` drive and serial ``REPL`` will become available.

CircuitPython at least 7.1.0-beta2 is required.

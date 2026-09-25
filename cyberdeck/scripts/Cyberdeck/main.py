"""Power-on entry point.

MicroPython runs this after every reset, including unplug/replug.
In Thonny, press Run on app.py for the full program, or on a scene
file (aquarium.py, cat.py, ...) for that scene alone.
"""
import sys
import app

try:
    app.main()
except Exception as e:
    sys.print_exception(e)

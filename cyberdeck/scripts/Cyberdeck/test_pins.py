"""Raw GPIO pin test -- no driver, no SPI object, just machine.Pin.

Cycles each screen control pin HIGH for 2s, then LOW for 2s, one pin
at a time, printing what it's doing. While it runs, probe the far end
of each wire (at the SCREEN side, not the Pico side) with a multimeter
set to DC volts, or clip a 330ohm-resistor+LED between the wire and
GND -- it should light during the HIGH phase.

This isolates: "is the Pico driving this pin?" and "is this wire/
breadboard row actually carrying it to the screen?" from any question
about the display driver or main.py logic.

Edit the pin numbers below if you're not using the current pinout.

Run with:
    make test-pins        (or open it in Thonny and press F5)
"""
from machine import Pin
import time

PINS = [
    ("CS   (GP9)",  9),
    ("SCK  (GP10)", 10),
    ("MOSI (GP11)", 11),
    ("RST  (GP12)", 12),
    ("DC   (GP13)", 13),
    ("BLK  (GP14)", 14),
]

HOLD_S = 2

def main():
    print("[test_pins] Raw pin toggle test. No driver involved.")
    print("[test_pins] Probe each wire at the SCREEN end while it cycles.")
    print("[test_pins] Ctrl-C to stop.\n")

    outs = [(name, Pin(num, Pin.OUT, value=0)) for name, num in PINS]

    try:
        while True:
            for name, pin in outs:
                print("[test_pins] {} -> HIGH".format(name))
                pin.value(1)
                time.sleep(HOLD_S)
                print("[test_pins] {} -> LOW".format(name))
                pin.value(0)
                time.sleep(HOLD_S)
            print("[test_pins] --- cycle complete, repeating ---\n")
    except KeyboardInterrupt:
        print("[test_pins] Stopped.")
        for _, pin in outs:
            pin.value(0)


main()

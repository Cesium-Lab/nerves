"""Check that every part of the cyberdeck made it onto the Pico and runs.

Run with:
    make test-scenes      (or open it in Thonny and press F5)

Draws a few seconds of each mode in turn, then the sleep aurora. If one
of them is missing or has a typo in it, this stops there and tells you
which file to look at -- much easier than watching main.py crash.

Nothing here uses the buttons, so it also works before you've wired them.
"""
from machine import Pin, SPI
import time

import config
config.LOADING_APP = True
import st7789py as st7789
import vga1_8x8 as font


def build_display():
    spi = SPI(
        1, baudrate=config.SCREEN_SPI_BAUD,
        sck=Pin(config.PIN_SCREEN_SCK),
        mosi=Pin(config.PIN_SCREEN_MOSI),
    )
    bl = Pin(config.PIN_SCREEN_BL, Pin.OUT, value=1)
    display = st7789.ST7789(
        spi, config.SCREEN_PHYS_W, config.SCREEN_PHYS_H,
        reset=Pin(config.PIN_SCREEN_RST, Pin.OUT),
        cs=Pin(config.PIN_SCREEN_CS, Pin.OUT),
        dc=Pin(config.PIN_SCREEN_DC, Pin.OUT),
        backlight=bl,
        rotation=config.SCREEN_ROTATION,
    )
    return display, bl


def banner(display, text):
    display.fill_rect(0, 0, config.SCREEN_W, 12, 0)
    display.text(font, text, 4, 2, st7789.WHITE, 0)


def main():
    print("[scenes] Building display...")
    display, bl = build_display()

    print("[scenes] Importing every scene...")
    from cat import Cat
    from aquarium import Aquarium
    from reader import Reader
    from quiz import Quiz
    from flappy import Flappy
    from pomodoro import Pomodoro
    import sleepshow
    from galaxy import Galaxy

    scenes = [
        ("cat", Cat(display)),
        ("aquarium", Aquarium(display)),
        ("reader", Reader(display, config.READER_PATH)),
        ("quiz", Quiz(display)),
        ("flappy", Flappy(display)),
        ("pomodoro", Pomodoro(display)),
    ]
    print("[scenes] All six imported OK.")

    try:
        for name, scene in scenes:
            print("[scenes] ->", name)
            scene.reset()
            frame_ms = getattr(scene, "frame_ms", config.SCREEN_FRAME_MS)
            # Roughly three seconds of each.
            for i in range(3000 // frame_ms):
                scene.step()
                # Poke it a few times so the animations actually move.
                if i == 8:
                    scene.action()
                time.sleep_ms(frame_ms)

        for label, Scene in (("aurora", sleepshow.NorthernLights), ("galaxy", Galaxy)):
            print("[scenes] -> {} (sleep)".format(label))
            scene = Scene(display)
            scene.reset()
            for i in range(12):
                scene.step()
                time.sleep_ms(scene.frame_ms)
            print("[scenes]    {} stepped OK".format(label))

        display.fill(0)
        display.text(font, "ALL SCENES OK",
                     (config.SCREEN_W - 13 * 8) // 2, 110, st7789.GREEN, 0)
        print()
        print("[scenes] Everything imported, drew, and responded. You're good.")
    except KeyboardInterrupt:
        print("[scenes] Stopped.")
        display.fill(0)


main()


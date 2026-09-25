"""Run one scene as a standalone program.

Thonny's Run submits the editor text to the REPL instead of importing
the file, so `__name__ == "__main__"` is false and a file with only
class definitions does nothing. Scene modules call `run()` from the
bottom when `__name__` is not their own module name -- that fires
under Thonny, and stays quiet when app.py imports them.
"""
from machine import Pin, SPI
import time

import config
from hardware import DebouncedInput, StatusLED
import st7789py as st7789


def build_display():
    spi = SPI(
        1, baudrate=config.SCREEN_SPI_BAUD,
        sck=Pin(config.PIN_SCREEN_SCK),
        mosi=Pin(config.PIN_SCREEN_MOSI),
    )
    display = st7789.ST7789(
        spi, config.SCREEN_PHYS_W, config.SCREEN_PHYS_H,
        reset=Pin(config.PIN_SCREEN_RST, Pin.OUT),
        cs=Pin(config.PIN_SCREEN_CS, Pin.OUT),
        dc=Pin(config.PIN_SCREEN_DC, Pin.OUT),
        backlight=None,
        rotation=config.SCREEN_ROTATION,
    )
    bl = Pin(config.PIN_SCREEN_BL, Pin.OUT, value=0)
    return display, bl


def build_inputs():
    button_a = DebouncedInput(
        config.PIN_BUTTON_A, pull=Pin.PULL_UP,
        active_high=False, debounce_ms=config.DEBOUNCE_MS,
    )
    button_b = DebouncedInput(
        config.PIN_BUTTON_B, pull=Pin.PULL_UP,
        active_high=False, debounce_ms=config.DEBOUNCE_MS,
    )
    led = StatusLED(config.PIN_LED)
    return button_a, button_b, led


def with_display(fn):
    """Turn the screen on, call fn(display, bl), then optionally blank."""
    display, bl = build_display()
    bl.value(1)
    try:
        fn(display, bl)
    except KeyboardInterrupt:
        print("Interrupted.")
    finally:
        if config.BLANK_ON_EXIT:
            bl.value(0)


def run(cls, *args):
    """Show one scene. A tap = action, A hold = hold, Ctrl-C = stop."""
    print("Running {}. A tap=action  A hold=hold  Ctrl-C=stop".format(
        getattr(cls, "__name__", cls)))
    display, bl = build_display()
    button_a, button_b, led = build_inputs()
    bl.value(1)
    scene = cls(display, *args)
    scene.reset()

    a_press_start = None
    a_long_fired = False
    last_frame = time.ticks_ms()

    try:
        while True:
            a_rise, a_fall = button_a.update()
            button_b.update()
            now = time.ticks_ms()

            if a_rise:
                a_press_start = now
                a_long_fired = False

            if (a_press_start is not None and not a_long_fired
                    and button_a.pressed
                    and time.ticks_diff(now, a_press_start) >= config.LONG_PRESS_MS):
                scene.hold()
                a_long_fired = True
                print("A hold -> {}".format(getattr(scene, "status", "")))

            if a_fall:
                if not a_long_fired and a_press_start is not None:
                    scene.action()
                    print("A tap -> {}".format(getattr(scene, "status", "")))
                a_press_start = None
                a_long_fired = False

            frame_ms = getattr(scene, "frame_ms", config.SCREEN_FRAME_MS)
            if time.ticks_diff(now, last_frame) >= frame_ms:
                scene.step()
                last_frame = now

            led.set(button_a.pressed or button_b.pressed)
            time.sleep_ms(config.LOOP_INTERVAL_MS)
    except KeyboardInterrupt:
        print("Interrupted.")
    finally:
        led.off()
        if config.BLANK_ON_EXIT:
            bl.value(0)

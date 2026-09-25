"""Main entry point -- splash, then a six-mode state machine.

Hardware: one 240x320 ST7789 screen (landscape 320x240) and two buttons. Nothing else.

Controls:
  Button A tap    : the mode-specific action
                      cat      -> next animation
                      aquarium -> next color palette
                      reader   -> next page
                      quiz     -> next answer choice
                      flappy   -> flap
                      pomodoro -> start / pause / resume
  Button A hold   : the mode-specific "hold" action
                      quiz     -> lock in answer, next question
                      reader   -> jump back to page 1
                      flappy   -> restart the game
                      pomodoro -> reset the timer
                      cat/aquarium -> nothing
  Button B tap    : switch mode (cat -> aquarium -> reader -> quiz -> flappy
                    -> pomodoro)
  Button B hold   : go to sleep -- plays an ambient ASCII animation
                    (aurora or galaxy -- see config.SLEEP_SCENE)

  Either button also wakes it from sleep, and that first press only wakes --
  it doesn't also fire the action.

Every scene object implements the same four methods, which is what lets
this loop stay so short: reset(), step(), action(), hold().
"""
from machine import Pin, SPI
import sys
import time

import gc

import config
config.LOADING_APP = True
from hardware import DebouncedInput, StatusLED

import st7789py as st7789
from cat import Cat
from aquarium import Aquarium
from reader import Reader
from quiz import Quiz
from flappy import Flappy
from pomodoro import Pomodoro
from splash import splash
import sleepshow
from galaxy import Galaxy


MODE_NAMES = ["cat", "aquarium", "reader", "quiz", "flappy", "pomodoro"]

# What the device is doing right now.
AWAKE = 0
ASLEEP = 1        # sleep picture on screen, backlight still on
OFF = 2           # backlight off entirely


def log(msg):
    if config.DEBUG:
        print("[{:>8} ms] {}".format(time.ticks_ms(), msg))


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


def show_error(display, bl, err):
    """Print the traceback to the shell and draw a short message on the LCD."""
    sys.print_exception(err)
    try:
        import vga1_8x8 as font_small
        ERR = st7789.color565(255, 60, 60)
        bl.value(1)
        display.fill(0)
        display.text(font_small, str(err)[:config.SCREEN_W // 8 - 1], 4, 110, ERR, 0)
    except Exception:
        pass


def main():
    log("Boot OK. Initializing hardware...")
    button_a, button_b, led = build_inputs()
    display, bl = build_display()

    try:
        splash(display, bl)

        scenes = [
            Cat(display),
            Aquarium(display),
            Reader(display, config.READER_PATH),
            Quiz(display),
            Flappy(display),
            Pomodoro(display),
        ]

        mode = 0
        power = AWAKE
        last_activity = time.ticks_ms()
        last_frame    = time.ticks_ms()
        last_beat     = time.ticks_ms()

        # Long-press tracking. `swallow` means this press only woke the screen,
        # so it shouldn't also fire an action when released.
        a_press_start = None
        a_long_fired = False
        a_swallow = False
        b_press_start = None
        b_long_fired = False
        b_swallow = False

        # A live NorthernLights scene while asleep (so it animates), else None.
        sleep_scene = None

        def wake():
            """Back to the current mode."""
            nonlocal power, sleep_scene
            power = AWAKE
            bl.value(1)
            sleep_scene = None
            scenes[mode].reset()

        def go_to_sleep():
            nonlocal power, sleep_scene
            power = ASLEEP
            bl.value(1)
            gc.collect()
            if config.SLEEP_SCENE == "galaxy":
                sleep_scene = Galaxy(display)
            else:
                sleep_scene = sleepshow.NorthernLights(display)
            sleep_scene.reset()
            log("Sleep ({}).".format(sleep_scene.status))

        def screen_off():
            nonlocal power, sleep_scene
            power = OFF
            sleep_scene = None
            display.fill(0)
            bl.value(0)
            log("Backlight off.")

        wake()

        log("Ready.")
        log("A tap=action  A hold=mode action  B tap=switch mode  B hold=sleep")

        while True:
            a_rise, a_fall = button_a.update()
            b_rise, b_fall = button_b.update()

            now = time.ticks_ms()

            # --- Button A pressed ---
            if a_rise:
                last_activity = now
                a_press_start = now
                a_long_fired = False
                a_swallow = power != AWAKE
                if power != AWAKE:
                    wake()
                    log("Wake ({}).".format(MODE_NAMES[mode]))

            # --- Button A held ---
            if (a_press_start is not None and not a_long_fired
                    and not a_swallow and button_a.pressed
                    and time.ticks_diff(now, a_press_start) >= config.LONG_PRESS_MS):
                last_activity = now
                scenes[mode].hold()
                a_long_fired = True
                log("A hold -> {}".format(scenes[mode].status))

            # --- Button A released ---
            if a_fall:
                last_activity = now
                if (not a_long_fired and not a_swallow
                        and a_press_start is not None):
                    scenes[mode].action()
                    log("A tap -> {}".format(scenes[mode].status))
                a_press_start = None
                a_long_fired = False
                a_swallow = False

            # --- Button B pressed ---
            if b_rise:
                last_activity = now
                b_press_start = now
                b_long_fired = False
                b_swallow = power != AWAKE
                if power != AWAKE:
                    wake()
                    log("Wake ({}).".format(MODE_NAMES[mode]))

            # --- Button B held: go to sleep ---
            if (b_press_start is not None and not b_long_fired
                    and not b_swallow and button_b.pressed
                    and time.ticks_diff(now, b_press_start) >= config.LONG_PRESS_MS):
                last_activity = now
                go_to_sleep()
                b_long_fired = True

            # --- Button B released: switch mode ---
            if b_fall:
                last_activity = now
                if (not b_long_fired and not b_swallow
                        and b_press_start is not None):
                    mode = (mode + 1) % len(scenes)
                    scenes[mode].reset()
                    log("Mode -> {}".format(MODE_NAMES[mode]))
                b_press_start = None
                b_long_fired = False
                b_swallow = False

            # --- Idle: awake -> asleep -> backlight off ---
            idle = time.ticks_diff(now, last_activity)
            # A scene can refuse to let the screen sleep -- the pomodoro does
            # that while it's counting down, so a session isn't interrupted.
            keep_awake = getattr(scenes[mode], "keep_awake", False)
            if (power == AWAKE and config.AUTO_SLEEP_MS and not keep_awake
                    and idle > config.AUTO_SLEEP_MS):
                go_to_sleep()
            elif (power == ASLEEP and config.SCREEN_OFF_MS
                  and idle > config.AUTO_SLEEP_MS + config.SCREEN_OFF_MS):
                screen_off()

            # --- Render ---
            if power == AWAKE:
                # A scene can ask for a faster frame rate by setting frame_ms
                # (flappy does); everything else uses the config default.
                frame_ms = getattr(scenes[mode], "frame_ms", config.SCREEN_FRAME_MS)
                if time.ticks_diff(now, last_frame) >= frame_ms:
                    scenes[mode].step()
                    last_frame = now
            elif power == ASLEEP and sleep_scene is not None:
                # Keep the aurora shimmering while asleep.
                frame_ms = getattr(sleep_scene, "frame_ms", config.SCREEN_FRAME_MS)
                if time.ticks_diff(now, last_frame) >= frame_ms:
                    sleep_scene.step()
                    last_frame = now

            # --- Heartbeat ---
            if config.HEARTBEAT_MS and time.ticks_diff(now, last_beat) >= config.HEARTBEAT_MS:
                log("hb a={} b={} | mode={} power={}".format(
                    int(button_a.pressed), int(button_b.pressed),
                    MODE_NAMES[mode],
                    ("awake", "asleep", "off")[power],
                ))
                last_beat = now

            led.set(button_a.pressed or button_b.pressed)
            time.sleep_ms(config.LOOP_INTERVAL_MS)

    except KeyboardInterrupt:
        log("Interrupted.")
    except Exception as e:
        show_error(display, bl, e)
    finally:
        led.off()
        if config.BLANK_ON_EXIT:
            bl.value(0)
        log("Clean shutdown.")


if __name__ != "app":
    main()

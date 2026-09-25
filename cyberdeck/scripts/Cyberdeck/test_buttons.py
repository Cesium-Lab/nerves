"""Two-button test.

The onboard LED lights while either button is held. The terminal shows
each press and release, tells you when a long press fires, and prints a
heartbeat with the raw pin values so you can spot wiring issues.

Run with:
    make test-buttons
"""

from machine import Pin
import time



import config
from hardware import DebouncedInput, StatusLED


def main():
    button_a = DebouncedInput(
        config.PIN_BUTTON_A,
        pull=Pin.PULL_UP,
        active_high=False,
        debounce_ms=config.DEBOUNCE_MS,
    )

    button_b = DebouncedInput(
        config.PIN_BUTTON_B,
        pull=Pin.PULL_UP,
        active_high=False,
        debounce_ms=config.DEBOUNCE_MS,
    )

    led = StatusLED(config.PIN_LED)

    print("[test_buttons] Press either button. LED lights while held.")
    print("[test_buttons] Button A = GP{}   Button B = GP{}".format(
        config.PIN_BUTTON_A, config.PIN_BUTTON_B))
    print("[test_buttons] Raw goes 1 -> 0 when pressed (pull-up, active-low).")
    print("[test_buttons] Hold A or B for {}ms to see the long press fire.".format(
        config.LONG_PRESS_MS))
    print("[test_buttons] Ctrl-C to stop.")

    a_down_at = None
    a_long_fired = False

    b_down_at = None
    b_long_fired = False

    last_beat = time.ticks_ms()

    try:
        while True:
            # Update both debounced inputs
            a_rise, a_fall = button_a.update()
            b_rise, b_fall = button_b.update()

            now = time.ticks_ms()

            # Button A
            if a_rise:
                print("[test_buttons] A DOWN")
                a_down_at = now
                a_long_fired = False

            if a_fall:
                print("[test_buttons] A UP{}".format(
                    "" if a_long_fired else "  (short tap)"
                ))
                a_down_at = None
                a_long_fired = False

            # Button B
            if b_rise:
                print("[test_buttons] B DOWN")
                b_down_at = now
                b_long_fired = False

            if b_fall:
                print("[test_buttons] B UP{}".format(
                    "" if b_long_fired else "  (short tap)"
                ))
                b_down_at = None
                b_long_fired = False

            # A long press
            if (
                a_down_at is not None
                and not a_long_fired
                and time.ticks_diff(now, a_down_at) >= config.LONG_PRESS_MS
            ):
                print("[test_buttons] A LONG PRESS fired")
                a_long_fired = True

            # B long press
            if (
                b_down_at is not None
                and not b_long_fired
                and time.ticks_diff(now, b_down_at) >= config.LONG_PRESS_MS
            ):
                print("[test_buttons] B LONG PRESS fired")
                b_long_fired = True

            # LED on while either button is held
            led.set(button_a.pressed or button_b.pressed)

            # Heartbeat every second
            if time.ticks_diff(now, last_beat) >= 1000:
                print(
                    "[test_buttons]   hb  "
                    "A raw={} pressed={}  |  "
                    "B raw={} pressed={}".format(
                        int(button_a.raw),
                        int(button_a.pressed),
                        int(button_b.raw),
                        int(button_b.pressed),
                    )
                )
                last_beat = now

            time.sleep_ms(5)

    except KeyboardInterrupt:
        led.off()
        print("[test_buttons] Stopped.")


main()

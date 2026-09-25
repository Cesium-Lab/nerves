"""Pin assignments and runtime tunables.

Hardware for this build: one 240x320 ST7789 screen + two buttons.
No touch sensor, no motion sensor, no speaker.
"""
HEARTBEAT_MS = 1000

# --- Buttons ----------------------------------------------------------------
# Both buttons wire from the GPIO pin to GND. The Pico's internal pull-up
# holds the pin HIGH when the button is up, and pressing pulls it LOW --
# which is why the code below uses active_high=False.
PIN_BUTTON_A = 15   # ACTION  button: does the mode-specific thing
PIN_BUTTON_B = 16   # MODE    button: switches between modes
PIN_LED = "LED"

# --- Screen (ST7789 240x320, SPI1, landscape) --------------------------------
# Native panel is 240 wide x 320 tall. Rotation 1 (or 3) turns that on its
# side so drawing is 320 x 240. If the image is upside-down, use 3.
PIN_SCREEN_SCK  = 10   # SCL on the TFT
PIN_SCREEN_MOSI = 11   # SDA on the TFT
PIN_SCREEN_CS   = 9
PIN_SCREEN_DC   = 13
PIN_SCREEN_RST  = 12
PIN_SCREEN_BL   = 14
SCREEN_PHYS_W = 240
SCREEN_PHYS_H = 320
SCREEN_ROTATION = 1    # 1 = landscape, 3 = landscape flipped
SCREEN_W = 320         # after rotation
SCREEN_H = 240
SCREEN_SPI_BAUD = 32_000_000
SCREEN_FRAME_MS = 120  # ~8 FPS animation
READER_PATH   = "/content/reader.txt"  # where the kindle lives

# --- Sleep mode --------------------------------------------------------------
# Hold button B to go to sleep at any time: the screen plays a colored
# ASCII animation. Any button wakes it (and that first press only wakes --
# it doesn't also fire the action).
#
# It also falls asleep on its own after AUTO_SLEEP_MS with nothing pressed,
# then turns the backlight off completely SCREEN_OFF_MS after that, so it
# isn't lit up all night. Set either to 0 to switch that stage off.
AUTO_SLEEP_MS = 100_000    # idle -> show the sleep picture
SCREEN_OFF_MS = 300_000    # then -> backlight off entirely

# TODO) Which ambient ASCII animation plays while asleep. "aurora" is the
#   northern-lights curtains in sleepshow.py; "galaxy" is the drifting
#   Milky Way band in galaxy.py. Both follow the same reset()/step()/
#   action()/hold() shape, so this is the only line you need to change.
SLEEP_SCENE = "aurora"

# --- Timing (milliseconds) ---------------------------------------------------
DEBOUNCE_MS = 30
LOOP_INTERVAL_MS = 5

# --- Long press --------------------------------------------------------------
LONG_PRESS_MS = 700  # hold button A this long for its "hold" action

# --- Logging -----------------------------------------------------------------
DEBUG = True

# Leave the last frame on screen when the program is interrupted (Thonny
# sends Ctrl-C on connect). Set True to blank the backlight on exit.
BLANK_ON_EXIT = False

# Scene files start themselves when you press Run in Thonny. app.py and the
# tests set this True first so importing them does not also start a scene.
LOADING_APP = False


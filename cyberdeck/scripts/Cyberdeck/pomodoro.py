"""Pomodoro timer: work, short break, long break, repeat.

Button A tap  -> start / pause / resume. 
Button A hold -> reset

"""
import time

import config
import st7789py as st7789
import vga1_8x8 as font_small
import vga1_16x16 as font_big


# TODO) Set your own work/break lengths and number of rounds. 
WORK_MIN        = 25    # length of a work sesh (mins)
SHORT_BREAK_MIN = 5     # short break after each work sesh
LONG_BREAK_MIN  = 15    # longer break after a few work stretches
ROUNDS          = 4     # work stretches before the long break

# TODO) Change the pictures! The tomato is a classic, but you can make it anything you like.
# Each letter is one block of color; '.' is empty. Draw whatever you like --
# it just has to stay a rectangle, and every row the same length.
#   r/R/h = tomato dark red / red / shine      g/G = leaf dark / light
#   m/M/h = mug rim / drink / handle           s   = steam
TOMATO = [
    ".......gg.......",
    "..g....gg....g..",
    "..gg..gGGg..gg..",
    "...gggGGGGggg...",
    "....rrRRRRrr....",
    "..rrRRRRRRRRrr..",
    ".rRRhhRRRRRRRRr.",
    "rRRhhRRRRRRRRRRr",
    "rRRhRRRRRRRRRRRr",
    "rRRRRRRRRRRRRRRr",
    ".rRRRRRRRRRRRRr.",
    "..rrRRRRRRRRrr..",
    "....rrRRRRrr....",
    "......rrrr......",
]

MUG = [
    "................",
    "....s..s..s.....",
    "...s..s..s......",
    "................",
    ".mmmmmmmmmm.hh..",
    ".mMMMMMMMMm.h.h.",
    ".mMMMMMMMMmh...h",
    ".mMMMMMMMMmh...h",
    ".mMMMMMMMMmh...h",
    ".mMMMMMMMMm.h.h.",
    ".mMMMMMMMMm.hh..",
    ".mmmmmmmmmm.....",
    "..mmmmmmmm......",
    "................",
]

# ----- Palette --------------------------------------------------------------
BG        = st7789.color565( 20,  22,  34)
WORK_C    = st7789.color565(255, 120,  90)
BREAK_C   = st7789.color565( 90, 220, 170)
DIGIT_OFF = st7789.color565( 38,  42,  58) 
LABEL     = st7789.color565(230, 232, 245)
DIM       = st7789.color565(120, 130, 160)
DOT_OFF   = st7789.color565( 52,  56,  76)

# Colors for the pictures above, full strength...
FULL = {
    "r": st7789.color565(160,  36,  36),
    "R": st7789.color565(228,  62,  52),
    "h": st7789.color565(255, 150, 130),
    "g": st7789.color565( 42, 120,  52),
    "G": st7789.color565( 96, 194,  84),
    "m": st7789.color565(232, 238, 248),
    "M": st7789.color565(152,  98,  62),
    "s": st7789.color565(170, 200, 214),
}
# ...and drained, for the part of the picture that time has already eaten.
DRAINED = {
    "r": st7789.color565( 48,  50,  66),
    "R": st7789.color565( 60,  64,  82),
    "h": st7789.color565( 74,  78,  98),
    "g": st7789.color565( 46,  58,  64),
    "G": st7789.color565( 58,  74,  78),
    "m": st7789.color565( 66,  70,  88),
    "M": st7789.color565( 54,  56,  72),
    "s": st7789.color565( 48,  52,  68),
}

# ----- Seven-segment digits ------
DIGIT_W = 22
DIGIT_H = 38
SEG_T   = 6
HALF    = (DIGIT_H - SEG_T) // 2

#      a
#    f   b
#      g
#    e   c
#      d
SEGMENTS = {
    "0": "abcdef", "1": "bc",     "2": "abged",  "3": "abgcd", "4": "fgbc",
    "5": "afgcd",  "6": "afgecd", "7": "abc",    "8": "abcdefg", "9": "abcdfg",
}

# ----- Layout ---------------------------------------------------------------
LABEL_Y  = 14
SCALE    = 5
SPR_X    = (config.SCREEN_W - 16 * SCALE) // 2
SPR_Y    = 42
DIGITS_Y = 126
_DX = (config.SCREEN_W - 240) // 2   # original layout was designed for 240px
DIGIT_XS = (62 + _DX, 89 + _DX, 129 + _DX, 156 + _DX)
COLON_X  = 116 + _DX
DOTS_Y   = 182
DOT_SIZE = 10
DOT_GAP  = 10
FOOTER_Y = 214

WORK = 0
SHORT_BREAK = 1
LONG_BREAK = 2

IDLE = 0 
RUNNING = 1
PAUSED = 2
DONE = 3 

PHASE_MS = (WORK_MIN * 60000, SHORT_BREAK_MIN * 60000, LONG_BREAK_MIN * 60000)
PHASE_NAMES = ("WORK", "BREAK", "LONG BREAK")


class Pomodoro:
    frame_ms = 200          # a timer doesn't need redrawing any faster

    def __init__(self, display):
        self.display = display
        self.round = 0
        self._load(WORK)
        self._force_redraw = True
        self._prev_text = None
        self._prev_blink = False
        self._prev_drained = -1

    def reset(self):
        """Called when you switch into this mode, or wake the screen.
        """
        self._force_redraw = True

    def action(self):
        """Button A tap: start, pause or resume."""
        if self.state == DONE:
            self._advance()
            self._start()
        elif self.state == RUNNING:
            self.state = PAUSED
            self._force_redraw = True
        else:
            self._start()

    def hold(self):
        """Button A hold: restart."""
        self.round = 0
        self._load(WORK)
        self._force_redraw = True

    def step(self):
        if self.state == RUNNING:
            now = time.ticks_ms()
            elapsed = time.ticks_diff(now, self.last_tick)
            self.last_tick = now
            if elapsed > 0:
                self.remaining -= elapsed
                if self.remaining <= 0:
                    self.remaining = 0
                    self.state = DONE
                    self._force_redraw = True
        self._draw()

    @property
    def keep_awake(self):
        """main.py checks this: don't fall asleep mid-pomodoro."""
        return self.state == RUNNING

    @property
    def status(self):
        return "{} {} {}".format(
            PHASE_NAMES[self.phase], self._clock(),
            ("idle", "running", "paused", "done")[self.state])

    # internal
    def _load(self, phase):
        self.phase = phase
        self.total = PHASE_MS[phase]
        self.remaining = self.total
        self.state = IDLE
        self.last_tick = time.ticks_ms()

    def _start(self):
        self.state = RUNNING
        self.last_tick = time.ticks_ms()
        self._force_redraw = True

    def _advance(self):
        if self.phase == WORK:
            self.round += 1
            if self.round >= ROUNDS:
                self.round = 0
                self._load(LONG_BREAK)
            else:
                self._load(SHORT_BREAK)
        else:
            self._load(WORK)
        self._force_redraw = True

    def _clock(self):
        secs = (self.remaining + 999) // 1000
        return "{:02d}:{:02d}".format(secs // 60, secs % 60)

    @property
    def _accent(self):
        return WORK_C if self.phase == WORK else BREAK_C

    @property
    def _sprite(self):
        return TOMATO if self.phase == WORK else MUG

    def _drained_rows(self):
        """How many rows from the top time has already eaten."""
        rows = len(self._sprite)
        if self.total <= 0:
            return 0
        done = self.total - self.remaining
        n = (rows * done) // self.total
        if n > rows:
            n = rows
        return n

    # drawing
    def _draw(self):
        text = self._clock()
        blink = (time.ticks_ms() // 500) % 2 == 0
        drained = self._drained_rows()

        if self._force_redraw:
            self._draw_all(text, blink, drained)
            self._force_redraw = False
            self._prev_text = text
            self._prev_blink = blink
            self._prev_drained = drained
            return

        if drained != self._prev_drained:
            self._draw_sprite(drained)
            self._prev_drained = drained
        if text != self._prev_text:
            self._draw_digits(text)
            self._prev_text = text
        if self.state == DONE and blink != self._prev_blink:
            self._draw_footer(blink)
            self._prev_blink = blink

    def _draw_all(self, text, blink, drained):
        self.display.fill(BG)
        label = PHASE_NAMES[self.phase]
        x = (config.SCREEN_W - len(label) * 16) // 2
        self.display.text(font_big, label, x, LABEL_Y, self._accent, BG)
        self._draw_sprite(drained)
        self._prev_text = None
        self._draw_digits(text, full=True)
        self._draw_dots()
        self._draw_footer(blink)

    def _draw_sprite(self, drained):
        """Draw the picture, dimming the rows time has already used up.
        """
        sprite = self._sprite
        for ry in range(len(sprite)):
            line = sprite[ry]
            palette = DRAINED if ry < drained else FULL
            x = 0
            while x < len(line):
                ch = line[x]
                run = 1
                while x + run < len(line) and line[x + run] == ch:
                    run += 1
                color = palette.get(ch, BG)
                self.display.fill_rect(SPR_X + x * SCALE, SPR_Y + ry * SCALE,
                                       run * SCALE, SCALE, color)
                x += run

    def _draw_digits(self, text, full=False):
        """text is MM:SS."""
        color = self._accent
        chars = (text[0], text[1], text[3], text[4])
        prev = (None, None, None, None)
        if not full and self._prev_text:
            p = self._prev_text
            prev = (p[0], p[1], p[3], p[4])
        for i in range(4):
            if full or chars[i] != prev[i]:
                self._draw_digit(DIGIT_XS[i], DIGITS_Y, chars[i], color)
        if full:
            self.display.fill_rect(COLON_X, DIGITS_Y + 10, SEG_T, SEG_T, color)
            self.display.fill_rect(COLON_X, DIGITS_Y + 24, SEG_T, SEG_T, color)

    def _draw_digit(self, x, y, ch, color):
        lit = SEGMENTS.get(ch, "")
        # Unlit segments are drawn dim, like a real LCD -- it makes the digits
        # read as digits instead of floating bars.
        for name, rect in (
            ("a", (x + SEG_T, y, DIGIT_W - 2 * SEG_T, SEG_T)),
            ("f", (x, y + SEG_T, SEG_T, HALF - SEG_T)),
            ("b", (x + DIGIT_W - SEG_T, y + SEG_T, SEG_T, HALF - SEG_T)),
            ("g", (x + SEG_T, y + HALF, DIGIT_W - 2 * SEG_T, SEG_T)),
            ("e", (x, y + HALF + SEG_T, SEG_T, HALF - SEG_T)),
            ("c", (x + DIGIT_W - SEG_T, y + HALF + SEG_T, SEG_T, HALF - SEG_T)),
            ("d", (x + SEG_T, y + DIGIT_H - SEG_T, DIGIT_W - 2 * SEG_T, SEG_T)),
        ):
            c = color if name in lit else DIGIT_OFF
            self.display.fill_rect(rect[0], rect[1], rect[2], rect[3], c)

    def _draw_dots(self):
        """One dot per work stretch done so far in this cycle."""
        total_w = ROUNDS * DOT_SIZE + (ROUNDS - 1) * DOT_GAP
        x = (config.SCREEN_W - total_w) // 2
        for i in range(ROUNDS):
            color = self._accent if i < self.round else DOT_OFF
            self.display.fill_rect(x, DOTS_Y, DOT_SIZE, DOT_SIZE, color)
            x += DOT_SIZE + DOT_GAP

    def _draw_footer(self, blink):
        if self.state == DONE:
            if self.phase == WORK:
                msg = "nice! tap for a break"
            else:
                msg = "break over -- tap to work"
            color = self._accent if blink else DIM
        elif self.state == RUNNING:
            msg = "tap = pause   hold = reset"
            color = DIM
        elif self.state == PAUSED:
            msg = "paused -- tap to resume"
            color = LABEL
        else:
            msg = "tap to start"
            color = LABEL
        self.display.fill_rect(0, FOOTER_Y - 2, config.SCREEN_W, 14, BG)
        x = (config.SCREEN_W - len(msg) * 8) // 2
        if x < 0:
            x = 0
        self.display.text(font_small, msg, x, FOOTER_Y, color, BG)


def run():
    from runscene import run as _run
    _run(Pomodoro)


if not __import__("config").LOADING_APP:
    run()

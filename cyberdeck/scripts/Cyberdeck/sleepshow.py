"""Sleep screen: a colored ASCII northern lights animation.

Inspired by D. Rice's "Northern Lights" ASCII piece -- curtains of
green/cyan/violet over a star field and a jagged horizon.

Button A tap/hold do nothing; this is the sleep scene.
"""
import random

import config
import st7789py as st7789
import vga1_8x8 as font


CHAR = 8
COLS = config.SCREEN_W // CHAR
ROWS = config.SCREEN_H // CHAR
GROUND_TOP = ROWS - 3

# Cheap 16-step sine, range -8..8. Index with ``x & 15``.
SINE = (0, 3, 5, 7, 8, 7, 5, 3, 0, -3, -5, -7, -8, -7, -5, -3)

BG     = st7789.color565(  6,   8,  22)
STAR_D = st7789.color565( 90, 100, 140)
STAR_B = st7789.color565(255, 250, 220)
TITLE  = st7789.color565(170, 190, 230)
GROUND = st7789.color565( 48,  56,  72)
SNOW   = st7789.color565(160, 170, 190)
# top of a curtain -> core -> bottom
PINK   = st7789.color565(220, 110, 200)
VIOLET = st7789.color565(150,  80, 220)
GREEN  = st7789.color565( 50, 230, 120)
MINT   = st7789.color565( 90, 255, 180)
CYAN   = st7789.color565( 40, 200, 220)
DIM_G  = st7789.color565( 30, 110,  70)

CORE_CH  = ("|", ":", "|", "!")
EDGE_CH  = (".", "'", ":", ".")
STAR_CH  = (".", ".", "*", "+", ".")


def _sin(x):
    return SINE[x & 15]


class NorthernLights:
    frame_ms = 160

    def __init__(self, display):
        self.display = display
        n = COLS * ROWS
        self.cur_ch = [" "] * n
        self.cur_co = [0] * n
        self.prev_ch = ["\x00"] * n
        self.prev_co = [0] * n
        self.frame = 0
        self.stars = []
        self._seed_stars()

    def _seed_stars(self):
        random.seed(7)
        self.stars = []
        for _ in range(28):
            col = random.randint(0, COLS - 1)
            row = random.randint(1, GROUND_TOP - 2)
            self.stars.append((col, row, random.randint(0, 11)))

    def reset(self):
        n = COLS * ROWS
        self.prev_ch = ["\x00"] * n
        self.prev_co = [0] * n
        self.frame = 0
        self.display.fill(BG)
        self._compose()
        self._flush()

    def action(self):
        pass

    def hold(self):
        pass

    def step(self):
        self.frame += 1
        self._compose()
        self._flush()

    @property
    def status(self):
        return "northern lights"

    def _clear(self):
        n = COLS * ROWS
        ch, co = self.cur_ch, self.cur_co
        for i in range(n):
            ch[i] = " "
            co[i] = 0

    def _put(self, col, row, text, color):
        if row < 0 or row >= ROWS or not text:
            return
        base = row * COLS
        ch, co = self.cur_ch, self.cur_co
        for i in range(len(text)):
            c = col + i
            if 0 <= c < COLS:
                glyph = text[i]
                ch[base + c] = glyph
                co[base + c] = 0 if glyph == " " else color

    def _compose(self):
        self._clear()
        t = self.frame
        self._stars(t)
        self._curtains(t)
        self._ground()
        title = "Northern Lights"
        self._put((COLS - len(title)) // 2, 0, title, TITLE)

    def _stars(self, t):
        for col, row, phase in self.stars:
            twinkle = (t // 2 + phase) & 7
            if twinkle == 0:
                ch, color = "*", STAR_B
            elif twinkle < 3:
                ch, color = "+", STAR_B
            else:
                ch, color = ".", STAR_D
            self._put(col, row, ch, color)

    def _curtains(self, t):
        # Two drifting masses, shaped like the original W of curtains.
        groups = (
            (9 + _sin(t // 3), 11, 0),
            (24 + _sin(t // 3 + 8), 13, 6),
        )
        for center, half, drift in groups:
            for col in range(center - half, center + half + 1):
                if col < 0 or col >= COLS:
                    continue
                dist = abs(col - center)
                # Gaps between ribbons, like the original's separate streaks.
                if _sin(col * 5 + t // 2 + drift) < -5 and dist > 2:
                    continue
                mid = 10 + _sin(col + t // 2 + drift) + _sin(col * 2 + 4) // 2
                height = 5 + (8 + _sin(col * 3 + drift)) // 4
                # Taper the sides of each mass.
                height = height - dist // 3
                if height < 3:
                    continue
                self._ribbon(col, mid, height, t, drift)

    def _ribbon(self, col, mid, height, t, drift):
        for dy in range(-height, height + 1):
            row = mid + dy
            if row < 1 or row >= GROUND_TOP:
                continue
            dist = dy if dy >= 0 else -dy
            # Flicker the texture so the curtain shimmers.
            flick = _sin(col * 7 + t // 2 + dy + drift)
            if dist <= height // 3:
                ch = CORE_CH[(t // 2 + col + (1 if flick > 0 else 0)) & 3]
                if dy < -1:
                    color = PINK if flick > 2 else VIOLET
                elif dy > 2:
                    color = CYAN
                else:
                    color = GREEN if flick >= 0 else MINT
            elif dist <= (2 * height) // 3:
                ch = EDGE_CH[(t // 2 + col) & 3]
                color = MINT if dy > 0 else VIOLET
            else:
                if flick < -3:
                    continue
                ch = "." if flick < 2 else "'"
                color = DIM_G if dy > 0 else PINK
            self._put(col, row, ch, color)

    def _ground(self):
        for col in range(COLS):
            bump = (8 + _sin(col * 3) + _sin(col * 5 + 4)) // 6  # 0..2
            top = ROWS - 1 - bump
            if top < GROUND_TOP:
                top = GROUND_TOP
            for row in range(top, ROWS):
                if row == top:
                    if _sin(col * 7) > 3:
                        ch = "^"
                    elif col & 1:
                        ch = "/"
                    else:
                        ch = "\\"
                    color = SNOW
                else:
                    ch = "_" if (col + row) & 1 else "-"
                    color = GROUND
                self._put(col, row, ch, color)

    def _flush(self):
        cur_ch, cur_co = self.cur_ch, self.cur_co
        prev_ch, prev_co = self.prev_ch, self.prev_co
        for row in range(ROWS):
            base = row * COLS
            col = 0
            while col < COLS:
                i = base + col
                if cur_ch[i] == prev_ch[i] and cur_co[i] == prev_co[i]:
                    col += 1
                    continue
                color = cur_co[i]
                start = col
                run = []
                while col < COLS:
                    j = base + col
                    if cur_ch[j] == prev_ch[j] and cur_co[j] == prev_co[j]:
                        break
                    if cur_co[j] != color:
                        break
                    run.append(cur_ch[j])
                    col += 1
                self.display.text(font, "".join(run),
                                  start * CHAR, row * CHAR, color, BG)
        prev_ch[:] = cur_ch
        prev_co[:] = cur_co


def show(display, path=None):
    """Draw one frame. `path` is ignored; kept so older callers still work."""
    scene = NorthernLights(display)
    scene.reset()
    return True


def run():
    from runscene import run as _run
    _run(NorthernLights)


if not __import__("config").LOADING_APP:
    run()


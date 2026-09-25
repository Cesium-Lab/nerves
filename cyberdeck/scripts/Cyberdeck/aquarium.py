"""ASCII aquarium with a day/night palette.

The water, sand, seaweed, and fish colors all shift through four
phases: dawn, day, dusk, night.

Button A tap -> jump to the next phase (the colors change).
"""
import random

import config
import st7789py as st7789
import vga1_8x8 as font


CHAR_W = 8
CHAR_H = 8
COLS = config.SCREEN_W // CHAR_W
ROWS = config.SCREEN_H // CHAR_H

PHASES = [
    {
        'name':    'dawn',
        'water':   st7789.color565(140,  80, 100),
        'sand':    st7789.color565(240, 190, 120),
        'weed':    st7789.color565( 90, 150,  70),
        'surface': st7789.color565(255, 200, 130),
        'fish': [
            st7789.color565(255, 130,  80),
            st7789.color565(255, 200, 120),
            st7789.color565(255, 100, 160),
            st7789.color565(180, 200, 220),
        ],
    },
    {
        'name':    'day',
        'water':   st7789.color565( 15,  60, 130),
        'sand':    st7789.color565(220, 200,  90),
        'weed':    st7789.color565( 40, 180,  60),
        'surface': st7789.color565(180, 220, 255),
    
        # TODO) These are the fish colours for the 'day' phase.
        #   color565(r, g, b) takes red/green/blue, each 0-255.
        'fish': [
            st7789.color565(255, 140,   0),
            st7789.color565(255, 255, 100),
            st7789.color565(255, 100, 200),
            st7789.color565(100, 200, 255),
        ],
    },
    {
        'name':    'dusk',
        'water':   st7789.color565(110,  50, 110),
        'sand':    st7789.color565(180, 110,  80),
        'weed':    st7789.color565( 70, 110,  60),
        'surface': st7789.color565(255, 130,  80),
        'fish': [
            st7789.color565(255, 180, 100),
            st7789.color565(255, 130, 200),
            st7789.color565(200, 100, 250),
            st7789.color565(255, 220, 150),
        ],
    },
    {
        'name':    'night',
        'water':   st7789.color565(  5,  15,  45),
        'sand':    st7789.color565( 50,  50,  30),
        'weed':    st7789.color565( 25,  80,  40),
        'surface': st7789.color565(220, 220, 255),
        'fish': [
            st7789.color565(200, 230, 255),
            st7789.color565(150, 220, 255),
            st7789.color565(180, 200, 255),
            st7789.color565(150, 255, 200),  # bioluminescent
        ],
    },
]
BUBBLE = st7789.color565(220, 240, 255)


# TODO) Change the fish! Each string in quotes is one fish shape.
FISH_RIGHT = ["><(((*>", "><(*>",  "><>",  ">o>"]
FISH_LEFT  = ["<*)))><", "<*)><",  "<><",  "<o<"]


class Fish:
    def __init__(self, palette):
        self.direction = random.choice(["left", "right"])
        idx = random.randint(0, len(FISH_RIGHT) - 1)
        self.shape = FISH_RIGHT[idx] if self.direction == "right" else FISH_LEFT[idx]
        self.color = random.choice(palette['fish'])
        self.row = random.randint(2, ROWS - 6)
        if self.direction == "right":
            self.col = -len(self.shape)
            self.dx = 1
        else:
            self.col = COLS
            self.dx = -1
        self.last_col = self.col


class Bubble:
    def __init__(self):
        self.col = random.randint(0, COLS - 1)
        self.row = ROWS - 4
        self.last_row = self.row
        self.glyph = random.choice(["o", "O", "."])


# TODO) How many fish? Try a number between 1 and 12.
class Aquarium:
    def __init__(self, display, num_fish=4):
        self.display = display
        self.num_fish = num_fish
        self.fish_list = []
        self.bubble_list = []
        self.frame = 0
        self._phase_idx = 0

    @property
    def palette(self):
        return PHASES[self._phase_idx]

    @property
    def status(self):
        return self.palette['name']

    def _draw(self, col, row, text, color):
        self.display.text(font, text, col * CHAR_W, row * CHAR_H,
                          color, self.palette['water'])

    def _erase(self, col, row, length):
        self.display.fill_rect(col * CHAR_W, row * CHAR_H,
                               length * CHAR_W, CHAR_H, self.palette['water'])

    def action(self):
        """Button A tap -- next palette (dawn -> day -> dusk -> night)."""
        self._phase_idx = (self._phase_idx + 1) % len(PHASES)
        self.reset()

    def hold(self):
        """Button A hold -- nothing special in aquarium mode."""
        pass

    def reset(self):
        p = self.palette

        self.fish_list = [Fish(p) for _ in range(self.num_fish)]
        self.bubble_list = []
        self.frame = 0

        self.display.fill(p['water'])

        # Sand along the bottom
        for col in range(COLS):
            self._draw(col, ROWS - 1, ".", p['sand'])
            if random.random() < 0.3:
                self._draw(col, ROWS - 2, "_", p['sand'])

        # Seaweed across the tank
        for sx in range(3, COLS - 2, 6):
            height = random.randint(3, 6)
            for h in range(height):
                ch = random.choice(["|", "(", ")", "{"])
                self._draw(sx, ROWS - 2 - h, ch, p['weed'])

        # Phase name in the top-left (row 0 is never used by fish/bubbles)
        self._draw(0, 0, p['name'], p['surface'])

    def step(self):
        for f in self.fish_list:
            self._update_fish(f)

        if self.frame % 8 == 0:
            self.bubble_list.append(Bubble())
        for b in self.bubble_list:
            self._update_bubble(b)
        self.bubble_list = [b for b in self.bubble_list if b.row > 0]

        self.frame += 1

    def _update_fish(self, f):
        visible_start = max(0, f.last_col)
        visible_end   = min(COLS, f.last_col + len(f.shape))
        if visible_end > visible_start:
            self._erase(visible_start, f.row, visible_end - visible_start)

        f.last_col = f.col
        f.col += f.dx

        if f.dx > 0 and f.col > COLS:
            f.col = -len(f.shape)
            f.row = random.randint(2, ROWS - 6)
        elif f.dx < 0 and f.col + len(f.shape) < 0:
            f.col = COLS
            f.row = random.randint(2, ROWS - 6)

        if f.col + len(f.shape) > 0 and f.col < COLS:
            shape = f.shape
            draw_col = f.col
            if draw_col < 0:
                shape = shape[-draw_col:]
                draw_col = 0
            if draw_col + len(shape) > COLS:
                shape = shape[: COLS - draw_col]
            if shape:
                self._draw(draw_col, f.row, shape, f.color)

    def _update_bubble(self, b):
        if 0 <= b.last_row < ROWS:
            self._erase(b.col, b.last_row, 1)
        b.last_row = b.row
        b.row -= 1
        if b.row > 0:
            self._draw(b.col, b.row, b.glyph, BUBBLE)


def run():
    print("Starting aquarium...")
    from runscene import run as _run
    _run(Aquarium)


if not __import__("config").LOADING_APP:
    run()

"""Flappy bird: a one-button game, drawn with ASCII.

Button A tap : flap (also starts the game, and retries after a crash)
Button A hold: restart at any time

"""
import random

import config
import st7789py as st7789
import vga1_8x8 as font


CHAR = 8
COLS = config.SCREEN_W // CHAR
ROWS = config.SCREEN_H // CHAR

# Palette
BG        = st7789.color565( 98, 192, 206)   # sky
PIPE      = st7789.color565( 92, 190,  60)
PIPE_CAP  = st7789.color565(150, 225, 105)
GRASS     = st7789.color565(134, 214,  90)
DIRT      = st7789.color565(212, 184, 120)
BIRD      = st7789.color565(255, 214,  60)
BIRD_DEAD = st7789.color565(230,  90,  70)
HUD       = st7789.color565( 30,  52,  60)
BIG       = st7789.color565( 25,  40,  50)
PANEL     = st7789.color565(245, 250, 250)
DIM       = st7789.color565( 90, 120, 130)

# TODO) Make the game easier or harder!
FRAME_MS     = 80     # how often the game steps. Lower = faster.
GRAVITY      = 0.15   # rows per frame, added to speed every frame
FLAP         = -0.95  # upward kick on a tap (negative = up)
MAX_FALL     = 1.20   # terminal falling speed, so it stays fair
GAP          = 11     # height of the opening, in rows
PIPE_SPACING = 14     # columns between pipes
MAX_GAP_STEP = 4      # most the opening can move up/down between pipes
PIPE_W       = 4      # pipe width in columns
BIRD_COL     = 5      # the bird stays in this column

HUD_ROW    = 0
TOP_ROW    = 1                # highest row a pipe occupies
GRASS_ROW  = ROWS - 2         # the bird dies if it reaches this
DIRT_ROW   = ROWS - 1

READY = 0
PLAYING = 1
DEAD = 2


class Flappy:
    frame_ms = FRAME_MS

    def __init__(self, display):
        self.display = display
        n = COLS * ROWS
        self.cur_ch = [" "] * n
        self.cur_co = [0] * n
        self.prev_ch = ["\x00"] * n
        self.prev_co = [0] * n
        self.best = 0
        self._new_game()

    # API
    def reset(self):
        """Called when you switch into this mode."""
        n = COLS * ROWS
        self.prev_ch = ["\x00"] * n     # force a full repaint
        self.prev_co = [0] * n
        self.display.fill(BG)
        self._new_game()
        self._compose()
        self._flush()

    def action(self):
        """Button A tap: flap, start, or retry."""
        if self.state == READY:
            self.state = PLAYING
            self.vel = FLAP
        elif self.state == PLAYING:
            self.vel = FLAP
        else:                            # DEAD
            self._new_game()

    def hold(self):
        """Button A hold: start over from scratch."""
        self._new_game()

    def step(self):
        if self.state == PLAYING:
            self._update()
        elif self.state == READY:
            self.hover += 1
            self.bird_y = self.start_y + (0.5 if (self.hover // 4) % 2 else 0.0)
        self._compose()
        self._flush()

    @property
    def status(self):
        if self.state == READY:
            return "flappy ready"
        if self.state == DEAD:
            return "flappy dead score={} best={}".format(self.score, self.best)
        return "flappy score={}".format(self.score)

    # game logic
    def _new_game(self):
        self.state = READY
        self.start_y = float((TOP_ROW + GRASS_ROW) // 2)
        self.bird_y = self.start_y
        self.vel = 0.0
        self.score = 0
        self.hover = 0
        self.pipes = []
        self.last_gap = None
        self._spawn_pipe(COLS + 3)

    def _spawn_pipe(self, col):
        highest = TOP_ROW + 1
        lowest = GRASS_ROW - GAP - 1
        if lowest < highest:
            lowest = highest
        # Keep each opening within reach of the last one. 
        if self.last_gap is None:
            gap_top = (highest + lowest) // 2
        else:
            lo = self.last_gap - MAX_GAP_STEP
            hi = self.last_gap + MAX_GAP_STEP
            if lo < highest:
                lo = highest
            if hi > lowest:
                hi = lowest
            if hi < lo:
                hi = lo
            gap_top = random.randint(lo, hi)
        self.last_gap = gap_top
        self.pipes.append({
            "col": col,
            "gap_top": gap_top,
            "scored": False,
        })

    def _update(self):
        self.vel += GRAVITY
        if self.vel > MAX_FALL:
            self.vel = MAX_FALL
        self.bird_y += self.vel

        if self.bird_y < TOP_ROW:            # bonk the ceiling
            self.bird_y = TOP_ROW
            self.vel = 0.0

        if self.bird_y >= GRASS_ROW:         # hit the ground
            self.bird_y = GRASS_ROW - 1
            self._die()
            return

        for p in self.pipes:
            p["col"] -= 1
            if not p["scored"] and p["col"] + PIPE_W - 1 < BIRD_COL:
                p["scored"] = True
                self.score += 1
        self.pipes = [p for p in self.pipes if p["col"] + PIPE_W > 0]

        rightmost = -99
        for p in self.pipes:
            if p["col"] > rightmost:
                rightmost = p["col"]
        if not self.pipes or rightmost <= COLS - PIPE_SPACING:
            self._spawn_pipe(COLS)

        if self._hits_pipe():
            self._die()

    def _die(self):
        self.state = DEAD
        if self.score > self.best:
            self.best = self.score

    def _hits_pipe(self):
        row = int(self.bird_y)
        left = BIRD_COL
        right = BIRD_COL + 1
        for p in self.pipes:
            if p["col"] + PIPE_W - 1 < left or p["col"] > right:
                continue
            if row < p["gap_top"] or row > p["gap_top"] + GAP - 1:
                return True
        return False

    # drawing
    def _clear(self):
        for i in range(COLS * ROWS):
            self.cur_ch[i] = " "
            self.cur_co[i] = 0

    def _put(self, col, row, text, color):
        if row < 0 or row >= ROWS:
            return
        base = row * COLS
        for i in range(len(text)):
            c = col + i
            if 0 <= c < COLS:
                ch = text[i]
                self.cur_ch[base + c] = ch
                self.cur_co[base + c] = 0 if ch == " " else color

    def _center(self, row, text, color):
        self._put((COLS - len(text)) // 2, row, text, color)

    def _panel(self, row_start, row_end, col_start, col_end):
        width = col_end - col_start
        for row in range(row_start, row_end + 1):
            self._put(col_start, row, " " * width, 0)

    def _compose(self):
        self._clear()

        for p in self.pipes:
            self._draw_pipe(p)

        self._put(0, GRASS_ROW, "=" * COLS, GRASS)
        self._put(0, DIRT_ROW, "#" * COLS, DIRT)

        sprite = "X>" if self.state == DEAD else "@>"
        color = BIRD_DEAD if self.state == DEAD else BIRD
        self._put(BIRD_COL, int(self.bird_y), sprite, color)

        self._put(0, HUD_ROW, "score {}".format(self.score), HUD)
        best = "best {}".format(self.best)
        self._put(COLS - len(best), HUD_ROW, best, HUD)

        if self.state == READY:
            self._panel(13, 16, 3, COLS - 3)
            self._center(14, "TAP TO FLAP", BIG)
            self._center(16, "hold to restart", DIM)
        elif self.state == DEAD:
            self._panel(11, 18, 4, COLS - 4)
            self._center(12, "GAME OVER", BIG)
            self._center(14, "score {}".format(self.score), HUD)
            self._center(15, "best  {}".format(self.best), HUD)
            self._center(17, "tap to retry", DIM)

    def _draw_pipe(self, p):
        col = p["col"]
        gap_top = p["gap_top"]
        gap_bottom = gap_top + GAP - 1
        bar = "#" * PIPE_W

        for row in range(TOP_ROW, gap_top):
            self._put(col, row, bar, PIPE_CAP if row == gap_top - 1 else PIPE)
        for row in range(gap_bottom + 1, GRASS_ROW):
            self._put(col, row, bar, PIPE_CAP if row == gap_bottom + 1 else PIPE)

    def _flush(self):
        """Push only the cells that changed, batching each run of
        same-colored changed cells into one display.text() call."""
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


def run():
    from runscene import run as _run
    _run(Flappy)


if not __import__("config").LOADING_APP:
    run()

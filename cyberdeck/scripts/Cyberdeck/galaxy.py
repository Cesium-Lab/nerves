"""GALAXY -- an alternate sleep screen: a drifting Milky Way band.
 
A starfield with the Milky Way's dust band drifting across it, rendered
with a density ramp -- the same trick real ASCII-art galaxy conversions
use (a tool like jp2a turns a photo's brightness into characters from
faint to solid) -- except animated instead of static: the band ripples
and the stars twinkle.
 
Same reset()/step()/action()/hold() shape as sleepshow.py's
NorthernLights, so app.py can show whichever one config.SLEEP_SCENE
names without caring which it got. Button A tap/hold do nothing; this
is a sleep scene, same as NorthernLights.
"""
import random
 
import config
import st7789py as st7789
import vga1_8x8 as font
 
CHAR = 8
COLS = config.SCREEN_W // CHAR
ROWS = config.SCREEN_H // CHAR
 
# cheap 16-step sine, range -8..8. Index with x & 15.
SINE = (0, 3, 5, 7, 8, 7, 5, 3, 0, -3, -5, -7, -8, -7, -5, -3)
 
BG       = st7789.color565(  4,   4,  14)   # deep space
STAR_D   = st7789.color565( 90, 100, 150)
STAR_B   = st7789.color565(255, 255, 240)
TITLE    = st7789.color565(200, 200, 240)
DUST_LO  = st7789.color565( 60,  40, 110)   # outer band, dim violet
DUST_MID = st7789.color565(110,  90, 200)
DUST_HI  = st7789.color565(190, 170, 255)
CORE     = st7789.color565(255, 240, 210)   # galactic core, warm white
NEBULA   = st7789.color565(230, 140, 190)   # pink flecks through the dust
 
# density ramp, faintest to solid -- local band thickness picks the index
DENSITY = " .:-=+*#%@"
 
# TODO) STAR_COUNT is how crowded the background sky is. TITLE_TEXT is
#   the line across the top. BAND_TILT is how steeply the Milky Way band
#   cuts across the screen; BAND_WIDTH is how fat and dense it is at its
#   thickest point (near the core).
STAR_COUNT = 70
TITLE_TEXT = "Galaxy"
BAND_TILT = 0.22
BAND_WIDTH = 6
 
 
def _sin(x):
    return SINE[x & 15]
 
 
class Galaxy:
    frame_ms = 180
 
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
        random.seed(11)         # a fixed field, so the sky doesn't jump on reset
        self.stars = []
        for _ in range(STAR_COUNT):
            col = random.randint(0, COLS - 1)
            row = random.randint(1, ROWS - 2)
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
        return "galaxy"
 
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
        self._band(t)
        self._put((COLS - len(TITLE_TEXT)) // 2, 0, TITLE_TEXT, TITLE)
 
    def _stars(self, t):
        for col, row, phase in self.stars:
            twinkle = (t // 3 + phase) & 7
            if twinkle == 0:
                ch, color = "*", STAR_B
            elif twinkle < 2:
                ch, color = "+", STAR_B
            else:
                ch, color = ".", STAR_D
            self._put(col, row, ch, color)
 
    def _band(self, t):
        core_col = COLS * 6 // 10
        for col in range(COLS):
            # A slow diagonal tilt plus a gentle ripple, so the band
            # breathes instead of sitting there static.
            center = (ROWS // 2
                       - int((col - COLS / 2) * BAND_TILT)
                       + _sin(col + t // 6) // 3)
            dist_core = abs(col - core_col)
            width = BAND_WIDTH - dist_core * BAND_WIDTH // COLS
            if width < 2:
                width = 2
            for dy in range(-width, width + 1):
                row = center + dy
                if row < 1 or row >= ROWS - 1:
                    continue
                d = abs(dy)
                # Noisy edge so the band looks like dust, not a clean bar.
                noise = _sin(col * 3 + dy * 5 + t // 4) + _sin(col * 7 - dy * 2)
                local = width - d + noise // 4
                if local <= 0:
                    continue
                level = local * (len(DENSITY) - 1) // (width + 4)
                if level <= 0:
                    continue
                if level > len(DENSITY) - 1:
                    level = len(DENSITY) - 1
                ch = DENSITY[level]
                if dist_core < 3 and d <= 1:
                    color = CORE
                elif level >= 7:
                    color = DUST_HI
                elif level >= 4:
                    color = NEBULA if (col + dy) & 3 == 0 else DUST_MID
                else:
                    color = DUST_LO
                self._put(col, row, ch, color)
 
    def _flush(self):
        """Only send the character runs that actually changed."""
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
    _run(Galaxy)
 
 
if not __import__("config").LOADING_APP:
    run()
"""A tiny personality quiz

Button A tap: move the selector to the next answer
Button A hold: go to next question
"""
import st7789py as st7789
import vga1_8x8 as font_small
import vga1_16x16 as font_big
import config


# Palette
BG       = st7789.color565( 18,  20,  40)
HEADER   = st7789.color565(150, 160, 220)
QUESTION = st7789.color565(255, 245, 220)
OPTION   = st7789.color565(180, 190, 210)
SEL_BG   = st7789.color565( 60,  70, 130)
SEL_FG   = st7789.color565(255, 240, 160)
FOOTER   = st7789.color565(120, 130, 170)
TITLE    = st7789.color565(255, 200, 130)
DESC     = st7789.color565(230, 230, 245)

# Colors
CAT      = st7789.color565(255, 200, 130)
CAT_FACE = st7789.color565(120, 220, 255)

# Layout
CHAR_W = 8
MARGIN_X = 8
MAX_CHARS = (config.SCREEN_W - 2 * MARGIN_X) // CHAR_W
HEADER_Y = 6
QUESTION_Y = 24
QUESTION_LINE_H = 10
OPTIONS_Y = 78
OPTION_SPACING = 19
ART_Y = 158            # where the little cat is drawn
ART_LINE_H = 16        # the pictures use the big 16x16 font
FOOTER_Y = 222

# TODO) QUIZ
# Keep answers under ~36 characters so they fit on one line.
QUESTIONS = [
    ("your ideal sunday?", [
        ("nap in a sunbeam",    "cat"),
        ("float in the water",  "fish"),
        ("read something new",  "book"),
        ("go somewhere far",    "comet"),
    ]),
    ("pick a snack", [
        ("warm milk",       "cat"),
        ("seaweed chips",   "fish"),
        ("tea and toast",   "book"),
        ("pop rocks",       "comet"),
    ]),
    ("your desk looks like", [
        ("soft and messy",     "cat"),
        ("blue and calm",      "fish"),
        ("stacks of paper",    "book"),
        ("wires everywhere",   "comet"),
    ]),
    ("someone says hi", [
        ("blink slowly",     "cat"),
        ("swim closer",      "fish"),
        ("ask a question",   "book"),
        ("talk very fast",   "comet"),
    ]),
    ("pick a superpower", [
        ("always be warm",    "cat"),
        ("breathe water",     "fish"),
        ("know everything",   "book"),
        ("move at lightspeed", "comet"),
    ]),
]

# TODO) Change the faces of the cat! They can be anything you can type.

CAT_POSES = [
    [(" /\\_/\\ ", CAT),
     ("( o.o )", CAT_FACE),
     (" > ^ < ", CAT)],

    [(" /\\_/\\ ", CAT),
     ("( -.- )", CAT_FACE),
     (" > ^ < ", CAT)],

    [(" /\\_/\\ ", CAT),
     ("( ^.^ )", CAT_FACE),
     (" > w < ", CAT)],

    [(" /\\_/\\ ", CAT),
     ("( O.O )", CAT_FACE),
     (" > o < ", CAT)],

    [(" /\\_/\\ ", CAT),
     ("( u.u )", CAT_FACE),
     (" > z < ", CAT)],
]

# Result key
RESULTS = [
    ("cat", "COZY CAT", TITLE, [
        " /\\_/\\ ",
        "( o.o )",
        " > ^ < ",
    ], [
        "you run on sunbeams and",
        "snacks. napping is a",
        "valid personality trait.",
    ]),
    ("fish", "CALM FISH", st7789.color565(120, 200, 255), [
        "~~~~~~~~~~~",
        " ><(((*>   ",
        "~~~~~~~~~~~",
    ], [
        "you go with the flow and",
        "somehow never rush.",
        "the vibes are immaculate.",
    ]),
    ("book", "CURIOUS BOOK", st7789.color565(255, 220, 160), [
        ".---------.",
        "|  ?   ?  |",
        "'---------'",
    ], [
        "you ask one more question",
        "than everybody else, and",
        "you looked it up after.",
    ]),
    ("comet", "BRIGHT COMET", st7789.color565(255, 180, 220), [
        "  \\ | /  ",
        "-- (*) --",
        "  / | \\  ",
    ], [
        "you move fast and leave a",
        "trail of half finished",
        "brilliant ideas.",
    ]),
]
# ============================================================================

ASKING = 0
RESULT = 1


def _wrap(text, max_chars):
    """Wrap a single line of text to max_chars per line."""
    words = text.split()
    if not words:
        return [""]
    out = []
    cur = words[0]
    for w in words[1:]:
        if len(cur) + 1 + len(w) <= max_chars:
            cur += " " + w
        else:
            out.append(cur)
            cur = w
    out.append(cur)
    return out


class Quiz:
    def __init__(self, display):
        self.display = display
        self.q_idx = 0
        self.sel = 0
        self.scores = {}
        self.mode = ASKING
        self.result_idx = 0
        self._needs_render = True

    # API
    def reset(self):
        """Start the quiz over from question 1."""
        self.q_idx = 0
        self.sel = 0
        self.scores = {}
        self.mode = ASKING
        self.result_idx = 0
        self._needs_render = True

    def action(self):
        """Button A tap -- move to the next answer choice."""
        if self.mode == ASKING:
            options = QUESTIONS[self.q_idx][1]
            self.sel = (self.sel + 1) % len(options)
            self._needs_render = True

    def hold(self):
        """Button A hold -- lock in the answer / play again."""
        if self.mode == RESULT:
            self.reset()
            return
        key = QUESTIONS[self.q_idx][1][self.sel][1]
        self.scores[key] = self.scores.get(key, 0) + 1

        if self.q_idx + 1 < len(QUESTIONS):
            self.q_idx += 1
            self.sel = 0
        else:
            self.mode = RESULT
            self.result_idx = self._winner()
        self._needs_render = True

    def step(self):
        if self._needs_render:
            self._render()
            self._needs_render = False

    @property
    def status(self):
        if self.mode == RESULT:
            return "result: {}".format(RESULTS[self.result_idx][1])
        return "q{}/{} sel={}".format(
            self.q_idx + 1, len(QUESTIONS),
            QUESTIONS[self.q_idx][1][self.sel][0])

    # internal
    def _winner(self):
        best_i = 0
        best_n = -1
        for i in range(len(RESULTS)):
            n = self.scores.get(RESULTS[i][0], 0)
            if n > best_n:
                best_n = n
                best_i = i
        return best_i

    def _center_small(self, text, y, color):
        x = (config.SCREEN_W - len(text) * 8) // 2
        if x < 0:
            x = 0
        self.display.text(font_small, text, x, y, color, BG)

    def _center_big(self, text, y, color):
        x = (config.SCREEN_W - len(text) * 16) // 2
        if x < 0:
            x = 0
        self.display.text(font_big, text, x, y, color, BG)

    def _render(self):
        self.display.fill(BG)
        if self.mode == RESULT:
            self._render_result()
        else:
            self._render_question()

    def _render_question(self):
        q_text, options = QUESTIONS[self.q_idx]

        header = "question {} of {}".format(self.q_idx + 1, len(QUESTIONS))
        self.display.text(font_small, header, MARGIN_X, HEADER_Y, HEADER, BG)

        y = QUESTION_Y
        for line in _wrap(q_text, MAX_CHARS):
            self.display.text(font_small, line, MARGIN_X, y, QUESTION, BG)
            y += QUESTION_LINE_H

        y = OPTIONS_Y
        for i in range(len(options)):
            label = options[i][0]
            if i == self.sel:
                self.display.fill_rect(4, y - 5, config.SCREEN_W - 8, 18, SEL_BG)
                self.display.text(font_small, ">", MARGIN_X, y, SEL_FG, SEL_BG)
                self.display.text(font_small, label[:MAX_CHARS - 2],
                                  MARGIN_X + 16, y, SEL_FG, SEL_BG)
            else:
                self.display.text(font_small, label[:MAX_CHARS - 2],
                                  MARGIN_X + 16, y, OPTION, BG)
            y += OPTION_SPACING

        # A different cat for every question.
        stage = CAT_POSES[self.q_idx % len(CAT_POSES)]
        y = ART_Y
        for line, color in stage:
            self._center_big(line, y, color)
            y += ART_LINE_H

        self._center_small("tap=next   hold=pick", FOOTER_Y, FOOTER)

    def _render_result(self):
        _key, title, art_color, art, desc = RESULTS[self.result_idx]

        y = 18
        for line in art:
            self._center_big(line, y, art_color)
            y += 16

        self._center_small("you are a", 80, HEADER)

        self._center_big(title, 98, TITLE)

        y = 134
        for line in desc:
            self._center_small(line[:MAX_CHARS], y, DESC)
            y += 12

        self._center_small("hold to play again", FOOTER_Y, FOOTER)


def run():
    from runscene import run as _run
    _run(Quiz)


if not __import__("config").LOADING_APP:
    run()

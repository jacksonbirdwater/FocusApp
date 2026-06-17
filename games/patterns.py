import random


class PatternGame:
    """
    Colour-pattern completion game.

    A sequence of coloured circles is shown with the last one hidden.
    The player picks the missing colour from the button palette.

    Difficulty controls:
      easy   — 2 colours, 5-item pattern, 120 s
      medium — 3 colours, 5-item pattern,  90 s
      hard   — 3 colours, 6-item pattern,  60 s
    """

    DIFFICULTY_TIMES = {
        'easy': 120,
        'medium': 90,
        'hard': 60,
    }

    COLORS = ['blue', 'red', 'green', 'orange', 'purple', 'yellow', 'cyan']

    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.initial_time = self.DIFFICULTY_TIMES[difficulty]
        self.score = 0
        self.pattern = self.generate_pattern()
        self.expected_color = self.pattern[-1]

    # called when the player presses a colour button
    # returns True on correct, False on wrong

    def answer(self, selected_color):
        if selected_color == self.expected_color:
            self.score += 1
            self.pattern = self.generate_pattern()
            self.expected_color = self.pattern[-1]
            return True

        self.score = max(0, self.score - 1)
        return False

    #pattern generation
    def generate_pattern(self):
        colors = self.COLORS

        if self.difficulty == 'easy':
            variations = [
                lambda a, b: [a, b, a, b, a],
                lambda a, b: [a, a, b, b, a],
                lambda a, b: [a, b, b, a, b],
                lambda a, b: [b, a, b, a, b],
                lambda a, b: [b, b, a, a, b],
            ]
            a, b = random.sample(colors, 2)
            return random.choice(variations)(a, b)

        elif self.difficulty == 'medium':
            variations = [
                lambda a, b, c: [a, b, a, c, a],
                lambda a, b, c: [a, b, c, a, b],
                lambda a, b, c: [a, b, a, b, a],
                lambda a, b, c: [b, a, c, a, b],
                lambda a, b, c: [c, a, b, a, c],
                lambda a, b, c: [a, c, b, c, a],
            ]
            a, b, c = random.sample(colors, 3)
            return random.choice(variations)(a, b, c)

        else:  # hard
            variations = [
                lambda a, b, c: [a, b, a, c, a, b],
                lambda a, b, c: [a, b, c, a, b, c],
                lambda a, b, c: [a, b, a, b, c, c],
                lambda a, b, c: [b, a, c, b, a, c],
                lambda a, b, c: [a, c, b, a, c, b],
                lambda a, b, c: [c, a, b, c, a, b],
                lambda a, b, c: [a, b, c, c, b, a],
            ]
            a, b, c = random.sample(colors, 3)
            return random.choice(variations)(a, b, c)
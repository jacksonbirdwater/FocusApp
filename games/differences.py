import pygame
import random
import images


class DifferenceGame:
    """
    Manages all state and logic for the spot-the-difference game.

    Flow per puzzle:
      1. Show the base image for `game_timer` seconds.
      2. Flash white briefly.
      3. Randomly decide to show the changed or unchanged image.
      4. Player presses Yes (changed) or No (same).
      5. Correct → score + time bonus, advance puzzle.
         Wrong   → game over.
      6. After all puzzles → signal 'score_screen'.
    """

    DIFFICULTY_TIMES = {
        'easy': 45,
        'medium': 30,
        'hard': 15,
    }

    # seconds shown before the reveal flash
    PREVIEW_SECONDS = 5
    # bonus seconds awarded for a correct answer
    REVEAL_BONUS = 5
    # white-flash duration in milliseconds
    FLASH_DURATION = 300

    PUZZLE_NAMES = [
        'image1', 'image2', 'image3', 'image4', 'image5',
        'image6', 'image7', 'image8', 'image9', 'image10',
    ]

    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.score = 0

        # timer is managed externally (main.py owns timer_sec),
        # but we own the per-puzzle countdown and flash state.
        self.initial_time = self.DIFFICULTY_TIMES[difficulty]

        self.puzzles = self.PUZZLE_NAMES[:]
        random.shuffle(self.puzzles)
        self.current_puzzle = 0

        self.game_timer = self.PREVIEW_SECONDS   # seconds until reveal
        self.show_changed = False                # True once reveal is shown
        self.puzzle_is_changed = False           # whether this puzzle is the changed variant

        self.flashing = False
        self.flash_start = 0

        # load the first image
        self._load_current_image()

    # public helpers queried by main.py

    @property
    def done(self):
        return self.current_puzzle >= len(self.puzzles)

    # called once per second by main.py's timer event

    def tick(self):
        """
        Advance the per-puzzle preview countdown by one second.
        Returns True if the flash should begin (caller should NOT also
        decrement timer_sec for game logic — that's still main.py's job).
        """
        if self.show_changed or self.flashing:
            return False

        self.game_timer -= 1
        if self.game_timer <= 0:
            self._start_flash()
            return True
        return False

    # called every frame by main.py
 

    def update(self):
        """Resolve the flash and switch to the reveal image when ready."""
        if self.flashing:
            if pygame.time.get_ticks() - self.flash_start >= self.FLASH_DURATION:
                self._resolve_flash()

    # called when the player presses Yes or No
    # returns (correct: bool, bonus_seconds: int, signal: str | None)
    #   signal is 'score_screen' when the game should end, else None
  

    def answer(self, player_says_changed):
        correct = player_says_changed == self.puzzle_is_changed

        if correct:
            self.score += 1
            self.current_puzzle += 1

            if self.done:
                return True, 0, 'score_screen'

            # advance to next puzzle
            self.game_timer = self.PREVIEW_SECONDS
            self.show_changed = False
            self._load_current_image()
            return True, self.REVEAL_BONUS, None

        else:
            return False, 0, 'score_screen'

 
    # drawing
    

    def draw(self, surface, width, height):
        if self.flashing:
            surface.fill((255, 255, 255))
            return

        if self.current_image:
            img_w = self.current_image.get_width()
            img_h = self.current_image.get_height()
            img_x = (width - img_w) // 2
            img_y = (height - img_h) // 2
            surface.blit(self.current_image, (img_x, img_y))

 
    # private


    def _load_current_image(self):
        if not self.done:
            self.current_image = getattr(images, self.puzzles[self.current_puzzle])

    def _start_flash(self):
        self.flashing = True
        self.flash_start = pygame.time.get_ticks()

    def _resolve_flash(self):
        self.puzzle_is_changed = random.choice([True, False])
        name = self.puzzles[self.current_puzzle]
        if self.puzzle_is_changed:
            self.current_image = getattr(images, name + 'changed')
        else:
            self.current_image = getattr(images, name)
        self.show_changed = True
        self.flashing = False
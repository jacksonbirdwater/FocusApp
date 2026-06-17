import pygame
import random
import images


# Timing constants (milliseconds)
TILE_LIT_DURATION = 400      # how long a tile stays lit during playback
TILE_GAP_DURATION = 200      # gap between tiles during playback
POST_SEQUENCE_PAUSE = 600    # pause after full sequence before player's turn


DIFFICULTY_TIMES = {
    'easy': 120,
    'medium': 90,
    'hard': 60,
}


class SequenceGame:
    """
    Classic Simon-style sequence memory game.

    States
    ------
    'playback'  — the game is flashing tiles for the player to watch
    'input'     — the player must click tiles in order
    'pausing'   — brief pause between a correct full-sequence and next round
    'over'      — wrong tile pressed; caller should move to score_screen
    """

    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.initial_time = DIFFICULTY_TIMES[difficulty]
        self.score = 0
        self.level = 1

        # the growing sequence of tile indices (0-7)
        self.sequence = [random.randrange(7)]

        # playback state
        self.state = 'playback'
        self.playback_index = 0          # which tile in sequence we're about to show
        self.lit_tile = None             # index of currently lit tile, or None
        self.last_event_time = pygame.time.get_ticks()
        self.message = 'Watch the pattern'

        # player input state
        self.player_index = 0

        # pause state
        self.pause_start = 0

        # player-press flash state
        self.press_lit_tile = None   # index of tile lit by a player press
        self.press_lit_time = 0      # when it was lit

        # build ImageButton list from the pre-built tile surfaces in images.py
        self.buttons = _create_buttons()

        # placeholder audio — replace with real assets later
        self.sounds = [pygame.mixer.Sound(f'assets/audio/tone.mp3') for i in range(7)]
        self.fail_sound = pygame.mixer.Sound('assets/audio/fail.mp3')

    # called every frame from main.py

    def update(self, events):
        """
        Process events and advance internal state.
        Returns 'score_screen' when the game is over, else None.
        """
        now = pygame.time.get_ticks()

        # ---- handle mouse clicks ----
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.state == 'input':
                result = self._handle_click(event.pos)
                if result == 'score_screen':
                    return 'score_screen'

        # ---- unlight player-pressed tile after short flash ----
        if self.press_lit_tile is not None:
            if now - self.press_lit_time >= 250:
                self.buttons[self.press_lit_tile].set_lit(False)
                self.press_lit_tile = None

        # ---- advance playback ----
        if self.state == 'playback':
            self._advance_playback(now)

        # ---- resolve pause between rounds ----
        elif self.state == 'pausing':
            if now - self.pause_start >= POST_SEQUENCE_PAUSE:
                self._start_playback()

        return None

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.update(mouse_pos)
            button.draw(surface)

    # private — playback

    def _advance_playback(self, now):
        if self.lit_tile is not None:
            # tile is currently lit — wait for LIT duration then unlight
            if now - self.last_event_time >= TILE_LIT_DURATION:
                self.buttons[self.lit_tile].set_lit(False)
                self.lit_tile = None
                self.last_event_time = now
        else:
            # tile is dark — wait for GAP then light the next one
            if now - self.last_event_time >= TILE_GAP_DURATION:
                if self.playback_index < len(self.sequence):
                    idx = self.sequence[self.playback_index]
                    self.buttons[idx].set_lit(True)
                    self.lit_tile = idx
                    self.playback_index += 1
                    self.last_event_time = now
                    # placeholder: self.sounds[idx].play()
                else:
                    # finished showing the sequence
                    self.state = 'input'
                    self.player_index = 0
                    self.message = 'Repeat the pattern'

    # private — player input

    def _handle_click(self, pos):
        for idx, button in enumerate(self.buttons):
            if button.check_press(pos):
                # briefly light the pressed tile; update() will unlight it
                button.set_lit(True)
                self.press_lit_tile = idx
                self.press_lit_time = pygame.time.get_ticks()

                if idx == self.sequence[self.player_index]:
                    self.player_index += 1
                    if self.player_index == len(self.sequence):
                        # completed the full sequence correctly
                        self.score += 1
                        self.level += 1
                        self.sequence.append(random.randrange(7))
                        self.state = 'pausing'
                        self.pause_start = pygame.time.get_ticks()
                        self.message = 'Correct!'
                else:
                    # wrong tile
                    self.message = 'Wrong!'
                    # placeholder: self.fail_sound.play()
                    self.state = 'over'
                    return 'score_screen'
                break
        return None

    # private — round transition

    def _reset_all_buttons(self):
        for button in self.buttons:
            button.set_lit(False)
        self.press_lit_tile = None

    def _start_playback(self):
        self._reset_all_buttons()
        self.state = 'playback'
        self.playback_index = 0
        self.lit_tile = None
        self.last_event_time = pygame.time.get_ticks()
        self.message = 'Watch the pattern'


# Button layout helper — builds ImageButton instances from images.py tiles

class ImageButton:
    """Lightweight tile button using pre-built pygame Surfaces."""

    def __init__(self, position, normal_surface, lit_surface):
        self.normal_surface = normal_surface
        self.lit_surface = lit_surface
        self.current_surface = normal_surface
        self.rect = normal_surface.get_rect(topleft=position)
        self.hovered = False

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, surface):
        surface.blit(self.current_surface, self.rect)

    def set_lit(self, lit):
        self.current_surface = self.lit_surface if lit else self.normal_surface

    def check_press(self, pos):
        return self.rect.collidepoint(pos)


def _create_buttons():
    positions = [
        (80, 407),   # blue
        (210, 407),  # cyan
        (340, 407),  # green
        (40, 511),   # orange
        (150, 511),  # purple
        (273, 511),  # yellow
        (380, 511),  # red
    ]

    buttons = []

    for i, pos in enumerate(positions):
        buttons.append(
            ImageButton(
                pos,
                images.sequence_tiles[i],
                images.sequence_tiles_lit[i]
            )
        )

    return buttons
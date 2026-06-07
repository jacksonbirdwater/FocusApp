# import and initialize pygame, plus supporting modules
import pygame
pygame.init()
import images
import sys
import random

# game window dimensions are loaded from the images module
WIDTH = images.WIDTH
HEIGHT = images.HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# menu panel size and movement speed
MENU_WIDTH = 169
MENU_HEIGHT = HEIGHT
MENU_SPEED = 20
clock = pygame.time.Clock()

# timer rendering setup
timer_font = pygame.font.Font(None, 24)
timer_sec = 0
timer_text = timer_font.render("00:00", True, (0, 0, 0))
timer_running = False

# custom timer event that fires every second
# used to count down time during the difference game
timer = pygame.USEREVENT + 1
pygame.time.set_timer(timer, 1000)

# alias commonly used image assets from the images module
# this keeps the main code simpler by avoiding repeated images.<name> lookups.
logo_image = images.logo_image
menuline = images.menuline
welcomuser = images.welcomuser
bgdoodles = images.bgdoodles
difftitle = images.difftitle
difficultybg = images.difficultybg
patternstitle = images.patternstitle
seqtitle = images.seqtitle
howtoplaytitle = images.howtoplaytitle
howtoplaydiff = images.howtoplaydiff

# difference game image pairs (normal + changed version)
image1 = images.image1
image1changed = images.image1changed
image2 = images.image2
image2changed = images.image2changed
image3 = images.image3
image3changed = images.image3changed
image4 = images.image4
image4changed = images.image4changed
image5 = images.image5
image5changed = images.image5changed
image6 = images.image6
image6changed = images.image6changed
image7 = images.image7
image7changed = images.image7changed
image8 = images.image8
image8changed = images.image8changed
image9 = images.image9
image9changed = images.image9changed
image10 = images.image10
image10changed = images.image10changed


class Button:
    """Button wrapper for image-based interactive controls."""
    def __init__(self, position, size, filename, label=None):
        # load the button image and create a hover version
        self.normal_image = pygame.image.load('images/' + filename)
        self.normal_image = pygame.transform.scale(self.normal_image, size)

        self.hover_image = self.normal_image.copy()
        self.hover_image.fill(
            (40, 40, 40, 0),
            special_flags=pygame.BLEND_RGBA_SUB,
        )

        self.rect = self.normal_image.get_rect(topleft=position)
        self.hovered = False
        self.label = label

    def update(self, mouse_pos):
        # update the hover state for visual feedback
        self.hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, surface):
        # draw hovered or normal image at the button position
        image = self.hover_image if self.hovered else self.normal_image
        surface.blit(image, self.rect)

    def check_press(self, position):
        # used to detect mouse clicks inside the button area
        return self.rect.collidepoint(position)


class ExitButton(Button):
    """Special button that closes the game on click."""
    def check_press(self, position):
        if super().check_press(position):
            pygame.quit()
            sys.exit()


class TextButton:
    """Simple colored button for text-based answers."""
    def __init__(self, position, size, label, font, bg_color=(245, 245, 245), text_color=(0, 0, 0)):
        self.rect = pygame.Rect(position, size)
        self.hovered = False
        self.label = label
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, surface):
        # draw a simple rectangle button with centered text
        color = (220, 220, 220) if self.hovered else self.bg_color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)
        text = self.font.render(str(self.label), True, self.text_color)
        surface.blit(text, text.get_rect(center=self.rect.center))

    def check_press(self, position):
        return self.rect.collidepoint(position)


# color definitions used to draw the pattern sequence squares
COLOR_MAP = {
    'blue': (0, 120, 215),
    'green': (0, 180, 0),
    'purple': (153, 51, 255),
    'red': (220, 20, 60),
    'cyan': (0, 183, 235),
    'yellow': (255, 215, 0),
    'orange': (255, 140, 0),
}
PATTERN_COLORS = list(COLOR_MAP.keys())


def generate_pattern(level, difficulty):
    """Generate the visible pattern and the correct next color."""
    base_lengths = {'easy': 3, 'medium': 4, 'hard': 5}
    visible_len = base_lengths.get(difficulty, 3) + max(0, level - 1)
    cycle_size = min(4, max(2, visible_len // 2))
    cycle = random.sample(PATTERN_COLORS, k=cycle_size)
    full_pattern = [cycle[i % cycle_size] for i in range(visible_len + 1)]
    return full_pattern[:-1], full_pattern[-1]


def build_choices(correct_answer, difficulty):
    """Build a shuffled list of answer buttons containing the correct color."""
    other_colors = [color for color in PATTERN_COLORS if color != correct_answer]
    random.shuffle(other_colors)
    choices = [correct_answer] + other_colors[:3]
    random.shuffle(choices)
    return choices


def create_choice_buttons(pattern_choices, timer_font=None):
    """Create image buttons for the pattern answer choices."""
    buttons = []
    button_size = (80, 80)
    spacing_x = 110
    spacing_y = 120
    total_width = button_size[0] * 2 + spacing_x
    start_x = (WIDTH - total_width) // 2
    start_y = 300

    for index, choice in enumerate(pattern_choices):
        row = index // 2
        col = index % 2
        position = (start_x + col * spacing_x, start_y + row * spacing_y)
        image_name = f'patternbutton{choice}.png'
        button = Button(position, button_size, image_name, label=choice)
        buttons.append(button)

    return buttons


def draw_pattern_sequence(screen, pattern_sequence, font):
    """Draw the current pattern sequence in the center of the screen."""
    rect_size = 60
    max_width = WIDTH - 80
    count = len(pattern_sequence)
    if count == 0:
        return

    spacing = min(90, max(40, (max_width - rect_size) // max(1, count - 1)))
    total_width = rect_size + (count - 1) * spacing
    start_x = (WIDTH - total_width) // 2
    start_y = 140

    for index, color in enumerate(pattern_sequence):
        rect = pygame.Rect(start_x + index * spacing, start_y, rect_size, rect_size)
        pygame.draw.rect(screen, COLOR_MAP.get(color, (128, 128, 128)), rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)


def generate_sequence(level, difficulty):
    """Generate the visible number sequence and the correct next number."""
    base_lengths = {'easy': 3, 'medium': 4, 'hard': 5}
    visible_len = base_lengths.get(difficulty, 3) + max(0, level - 1)
    start = random.randint(1, 5) if difficulty == 'easy' else random.randint(1, 9)
    step_choices = [1, 2, 3] if difficulty == 'easy' else ([2, 3, 4] if difficulty == 'medium' else [2, 3, 4, 5])
    step = random.choice(step_choices)
    full_sequence = [start + i * step for i in range(visible_len + 1)]
    return full_sequence[:-1], full_sequence[-1]


def build_sequence_choices(correct_answer):
    """Create a list of numeric answer choices including the correct one."""
    choices = {correct_answer}
    delta = max(1, abs(correct_answer) // 2)
    while len(choices) < 4:
        wrong = correct_answer + random.choice([-delta - 1, -delta, -1, 1, delta, delta + 1])
        if wrong > 0:
            choices.add(wrong)
    return random.sample(list(choices), 4)


def create_sequence_choice_buttons(sequence_choices, timer_font):
    """Make text buttons for the numeric sequence answers."""
    buttons = []
    button_size = (80, 80)
    start_x = 80
    start_y = 300
    spacing_x = 110
    spacing_y = 120

    for index, choice in enumerate(sequence_choices):
        row = index // 2
        col = index % 2
        position = (start_x + col * spacing_x, start_y + row * spacing_y)
        button = TextButton(position, button_size, choice, timer_font)
        buttons.append(button)

    return buttons


def draw_sequence(screen, sequence, font):
    """Draw the numeric sequence boxes on the screen."""
    title = font.render('Sequence:', True, (0, 0, 0))
    screen.blit(title, (40, 110))

    rect_size = 60
    spacing = 90
    start_x = 50
    start_y = 150

    for index, number in enumerate(sequence):
        rect = pygame.Rect(start_x + index * spacing, start_y, rect_size, rect_size)
        pygame.draw.rect(screen, (220, 220, 220), rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)
        text = font.render(str(number), True, (0, 0, 0))
        screen.blit(text, text.get_rect(center=rect.center))


def start_pattern_game(pattern_difficulty, timer_font=None):
    pattern_level = 1
    pattern_sequence, pattern_correct_answer = generate_pattern(pattern_level, pattern_difficulty)
    pattern_choices = build_choices(pattern_correct_answer, pattern_difficulty)
    pattern_choice_buttons = create_choice_buttons(pattern_choices, timer_font)
    return pattern_level, pattern_sequence, pattern_correct_answer, pattern_choices, pattern_choice_buttons


def start_sequence_game(sequence_difficulty, timer_font=None):
    sequence_level = 1
    sequence_sequence, sequence_correct_answer = generate_sequence(sequence_level, sequence_difficulty)
    sequence_choices = build_sequence_choices(sequence_correct_answer)
    sequence_choice_buttons = create_sequence_choice_buttons(sequence_choices, timer_font)
    return sequence_level, sequence_sequence, sequence_correct_answer, sequence_choices, sequence_choice_buttons


def main():
    """Main game loop and state setup."""
    global timer_sec, timer_running

    # menu state and animation
    menu_x = -MENU_WIDTH
    menu_open = False

    # current screen identifier controls which UI is shown
    current_screen = 'main_menu'
    selected_difficulty = None

    # puzzle image order for the spot-the-difference game
    puzzles = ['image1', 'image2', 'image3', 'image4', 'image5',
               'image6', 'image7', 'image8', 'image9', 'image10']

    current_puzzle = 0
    show_changed = False
    game_timer = 0

    current_image = None
    current_image_name = ''

    score = 0
    initial_time = 0

    puzzle_is_changed = False

    # flash state for difference reveal transition
    flashing = False
    flash_start = 0
    flash_duration = 300

    reveal_bonus = 0

    # pattern game state
    pattern_difficulty = None
    pattern_level = 1
    pattern_sequence = []
    pattern_choices = []
    pattern_choice_buttons = []
    pattern_correct_answer = None
    pattern_message = ''

    # sequence game state
    sequence_difficulty = None
    sequence_level = 1
    sequence_sequence = []
    sequence_choices = []
    sequence_choice_buttons = []
    sequence_correct_answer = None
    sequence_message = ''

    # track which game mode was last active for retry logic
    last_game_mode = None
    how_to_play_mode = None

    # buttons visible on the main menu and general UI
    exit_button = ExitButton((139, 424), (221, 65), 'exitButton.png')
    select_puzzle_button = Button((139, 270), (221, 65), 'selectPuzzleButton.png')
    menu_button = Button((18, 18), (24, 24), 'menu.png')

    account_button = Button((3, 88), (94, 24), 'account.png')
    howto_button = Button((3, 163), (115, 20), 'howtoplay.png')
    back_home_button = Button((139, 14), (24, 24), 'backhome.png')

    # game mode selection buttons
    diff_button = Button((145, 229), (221, 65), 'differences.png')
    patt_button = Button((145, 361), (221, 65), 'patterns.png')
    seq_button = Button((145, 493), (221, 65), 'sequences.png')

    # universal home button used for many screens
    homebutton = Button((455, 18), (24, 24), 'backhome.png')

    # difficulty buttons for difference game
    easydiffbutton = Button((145, 253), (221, 65), 'easy.png')
    meddiffbutton = Button((145, 384), (221, 65), 'med.png')
    harddiffbutton = Button((145, 515), (221, 65), 'hard.png')

    # difficulty buttons for pattern game
    easypattbutton = Button((145, 253), (221, 65), 'Easy.png')
    medpattbutton = Button((145, 384), (221, 65), 'med.png')
    hardpattbutton = Button((145, 515), (221, 65), 'hard.png')

    # difficulty buttons for sequence game
    easyseqbutton = Button((145, 253), (221, 65), 'Easy.png')
    medseqbutton = Button((145, 384), (221, 65), 'med.png')
    hardseqbutton = Button((145, 515), (221, 65), 'hard.png')

    # shared start/how-to buttons
    start_button = Button((139, 316), (221, 65), 'startbutton.png')
    diff_start_howto_button = Button((139, 432), (221, 65), 'howtopla.png')

    # yes/no buttons for the difference reveal screen
    yes_button = Button((62, 500), (150, 60), 'yes.png')
    no_button = Button((277, 500), (150, 60), 'no.png')

    # retry/back controls on the score screen
    retrybutton = Button((144, 418), (212, 60), 'retrybutton.png')
    patterns_back_button = Button((344, 418), (120, 60), 'patterns.png')
    howtoplaypattbutton = Button((139, 432), (221, 65), 'howtoplaypattbutton.png')

    running = True
    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == timer and timer_running:
                # countdown timer tick: update the timer every second
                timer_sec -= 1

                # if we're on the difference game, also countdown the reveal timer
                if current_screen == 'game' and not show_changed:
                    game_timer -= 1
                    if game_timer <= 0:
                        # trigger the reveal transition after the short delay
                        flashing = True
                        flash_start = pygame.time.get_ticks()

                # stop the timer at zero and end the game if time is up
                if timer_sec <= 0:
                    timer_sec = 0
                    timer_running = False
                    pygame.time.set_timer(timer, 0)

                    if current_screen == 'game':
                        current_screen = 'score_screen'

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if menu_button.check_press(mouse_pos):
                    menu_open = not menu_open

                if current_screen == 'main_menu':
                    # main menu only has the start and exit controls
                    if select_puzzle_button.check_press(mouse_pos):
                        current_screen = 'select_puzzle'
                    elif exit_button.check_press(mouse_pos):
                        pass

                elif current_screen == 'select_puzzle':
                    # choose a game mode from the selection menu
                    if diff_button.check_press(mouse_pos):
                        current_screen = 'diff_difficulty'
                    elif patt_button.check_press(mouse_pos):
                        current_screen = 'patterns_screen'
                    elif seq_button.check_press(mouse_pos):
                        current_screen = 'sequences_screen'
                    elif homebutton.check_press(mouse_pos):
                        current_screen = 'main_menu'

                elif current_screen == 'diff_difficulty':

                    if easydiffbutton.check_press(mouse_pos):
                        selected_difficulty = 'easy'
                        current_screen = 'diff_start'

                    elif meddiffbutton.check_press(mouse_pos):
                        selected_difficulty = 'medium'
                        current_screen = 'diff_start'

                    elif harddiffbutton.check_press(mouse_pos):
                        selected_difficulty = 'hard'
                        current_screen = 'diff_start'

                    elif homebutton.check_press(mouse_pos):
                        current_screen = 'main_menu'

                elif current_screen == 'patterns_screen':
                    # choose the patterns difficulty level
                    if easypattbutton.check_press(mouse_pos):
                        pattern_difficulty = 'easy'
                        last_game_mode = 'patterns'
                        current_screen = 'patterns_start'
                    elif medpattbutton.check_press(mouse_pos):
                        pattern_difficulty = 'medium'
                        last_game_mode = 'patterns'
                        current_screen = 'patterns_start'
                    elif hardpattbutton.check_press(mouse_pos):
                        pattern_difficulty = 'hard'
                        last_game_mode = 'patterns'
                        current_screen = 'patterns_start'
                    elif homebutton.check_press(mouse_pos):
                        current_screen = 'main_menu'

                elif current_screen == 'sequences_screen':
                    # choose the sequences difficulty level
                    if easyseqbutton.check_press(mouse_pos):
                        sequence_difficulty = 'easy'
                        last_game_mode = 'sequences'
                        current_screen = 'sequences_start'
                    elif medseqbutton.check_press(mouse_pos):
                        sequence_difficulty = 'medium'
                        last_game_mode = 'sequences'
                        current_screen = 'sequences_start'
                    elif hardseqbutton.check_press(mouse_pos):
                        sequence_difficulty = 'hard'
                        last_game_mode = 'sequences'
                        current_screen = 'sequences_start'
                    elif homebutton.check_press(mouse_pos):
                        current_screen = 'main_menu'

                elif current_screen == 'patterns_start':
                    if start_button.check_press(mouse_pos):
                        if pattern_difficulty:
                            pattern_level, pattern_sequence, pattern_correct_answer, pattern_choices, pattern_choice_buttons = start_pattern_game(pattern_difficulty, timer_font)
                            pattern_message = 'Find the next color'
                            score = 0
                            current_screen = 'patterns_game'
                    elif howtoplaypattbutton.check_press(mouse_pos):
                        how_to_play_mode = 'patterns'
                        current_screen = 'how_to_play'
                    elif homebutton.check_press(mouse_pos):
                        current_screen = 'main_menu'

                elif current_screen == 'sequences_start':
                    if start_button.check_press(mouse_pos):
                        if sequence_difficulty:
                            sequence_level, sequence_sequence, sequence_correct_answer, sequence_choices, sequence_choice_buttons = start_sequence_game(sequence_difficulty, timer_font)
                            sequence_message = 'Find the next number'
                            score = 0
                            current_screen = 'sequences_game'
                    elif homebutton.check_press(mouse_pos):
                        current_screen = 'main_menu'

                elif current_screen == 'patterns_game':
                    # answer input for the pattern game
                    if homebutton.check_press(mouse_pos):
                        current_screen = 'main_menu'
                    for button in pattern_choice_buttons:
                        if button.check_press(mouse_pos):
                            if button.label == pattern_correct_answer:
                                # correct answer: advance the level and reload the next pattern
                                score += 1
                                pattern_level += 1
                                pattern_sequence, pattern_correct_answer = generate_pattern(pattern_level, pattern_difficulty)
                                pattern_choices = build_choices(pattern_correct_answer, pattern_difficulty)
                                pattern_choice_buttons = create_choice_buttons(pattern_choices, timer_font)
                                pattern_message = 'Correct! Next pattern.'
                            else:
                                pattern_message = f'Wrong answer. The right choice was {pattern_correct_answer}.'
                                current_screen = 'score_screen'

                elif current_screen == 'sequences_game':
                    # answer input for the sequence game
                    if homebutton.check_press(mouse_pos):
                        current_screen = 'main_menu'
                    for button in sequence_choice_buttons:
                        if button.check_press(mouse_pos):
                            if button.label == sequence_correct_answer:
                                score += 1
                                sequence_level += 1
                                sequence_sequence, sequence_correct_answer = generate_sequence(sequence_level, sequence_difficulty)
                                sequence_choices = build_sequence_choices(sequence_correct_answer)
                                sequence_choice_buttons = create_sequence_choice_buttons(sequence_choices, timer_font)
                                sequence_message = 'Correct! Next sequence.'
                            else:
                                sequence_message = f'Wrong answer. The right number was {sequence_correct_answer}.'
                                current_screen = 'score_screen'

                elif current_screen == 'how_to_play':
                    if homebutton.check_press(mouse_pos):
                        if how_to_play_mode == 'patterns':
                            current_screen = 'patterns_start'
                        else:
                            current_screen = 'main_menu'

                elif current_screen == 'diff_start':
                    if start_button.check_press(mouse_pos):
                        # set timer based on difficulty
                        if selected_difficulty == 'easy':
                            timer_sec = 45
                        elif selected_difficulty == 'medium':
                            timer_sec = 30
                        elif selected_difficulty == 'hard':
                            timer_sec = 15

                        initial_time = timer_sec
                        timer_running = True
                        pygame.time.set_timer(timer, 1000)

                        # shuffle puzzles each run
                        random.shuffle(puzzles)
                        current_puzzle = 0

                        # always start from base image
                        current_image = getattr(images, puzzles[current_puzzle])
                        current_image_name = puzzles[current_puzzle]

                        show_changed = False
                        game_timer = 5
                        reveal_bonus = 5
                        score = 0
                        current_screen = 'game'

                    elif diff_start_howto_button.check_press(mouse_pos):
                        current_screen = 'how_to_play'

                    elif homebutton.check_press(mouse_pos):
                        current_screen = 'main_menu'

                elif current_screen == 'score_screen':
                    if homebutton.check_press(mouse_pos):
                        current_screen = 'main_menu'
                        timer_running = False
                        pygame.time.set_timer(timer, 0)

                    if retrybutton.check_press(mouse_pos):
                        if last_game_mode == 'patterns':
                            current_screen = 'patterns_start'
                        elif last_game_mode == 'sequences':
                            current_screen = 'sequences_start'
                        else:
                            current_screen = 'diff_start'
                    if patterns_back_button.check_press(mouse_pos):
                        current_screen = 'patterns_screen'

                elif current_screen == 'game':
                    if show_changed and yes_button.check_press(mouse_pos):
                        if puzzle_is_changed:
                            print("correct")
                            score += 1
                            timer_sec += reveal_bonus
                            current_puzzle += 1

                            if current_puzzle >= len(puzzles):
                                current_screen = 'score_screen'
                            else:
                                show_changed = False
                                game_timer = 5
                                current_image = getattr(images, puzzles[current_puzzle])
                                current_image_name = puzzles[current_puzzle]

                        else:
                            print("wrong")
                            current_screen = 'score_screen'

                    elif show_changed and no_button.check_press(mouse_pos):
                        if not puzzle_is_changed:
                            print("correct")
                            score += 1
                            timer_sec += reveal_bonus
                            current_puzzle += 1

                            if current_puzzle >= len(puzzles):
                                current_screen = 'score_screen'
                            else:
                                show_changed = False
                                game_timer = 5
                                reveal_bonus = 5
                                current_image = getattr(images, puzzles[current_puzzle])
                                current_image_name = puzzles[current_puzzle]

                        else:
                            print("wrong")
                            current_screen = 'score_screen'

                    if homebutton.check_press(mouse_pos):
                        current_screen = 'main_menu'
                        timer_running = False
                        pygame.time.set_timer(timer, 0)

                # menu interactions
                if menu_open and menu_x > -MENU_WIDTH:
                    if account_button.check_press(mouse_pos):
                        current_screen = 'account_page'
                        menu_open = False
                    elif howto_button.check_press(mouse_pos):
                        if current_screen.startswith('patterns'):
                            how_to_play_mode = 'patterns'
                        else:
                            how_to_play_mode = 'diff'
                        current_screen = 'how_to_play'
                        menu_open = False
                    elif back_home_button.check_press(mouse_pos):
                        current_screen = 'main_menu'
                        menu_open = False

        # reveal logic after delay
        if flashing:
            if pygame.time.get_ticks() - flash_start >= flash_duration:
                puzzle_is_changed = random.choice([True, False])

                if puzzle_is_changed:
                    current_image = getattr(images, puzzles[current_puzzle] + 'changed')
                    current_image_name = puzzles[current_puzzle] + 'changed'
                else:
                    current_image = getattr(images, puzzles[current_puzzle])
                    current_image_name = puzzles[current_puzzle]

                show_changed = True
                flashing = False

        # format the timer display each frame
        mins = timer_sec // 60
        secs = timer_sec % 60
        timer_text = timer_font.render(f"{mins:02}:{secs:02}", True, (0, 0, 0))

        mouse_pos = pygame.mouse.get_pos()

        # update hover states for visible buttons on the current screen
        if current_screen == 'main_menu':
            exit_button.update(mouse_pos)
            select_puzzle_button.update(mouse_pos)

        elif current_screen == 'select_puzzle':
            diff_button.update(mouse_pos)
            patt_button.update(mouse_pos)
            seq_button.update(mouse_pos)

        elif current_screen == 'account_page':
            exit_button.update(mouse_pos)

        elif current_screen == 'diff_difficulty':
            easydiffbutton.update(mouse_pos)
            meddiffbutton.update(mouse_pos)
            harddiffbutton.update(mouse_pos)
            homebutton.update(mouse_pos)

        elif current_screen == 'patterns_screen':
            homebutton.update(mouse_pos)
            easypattbutton.update(mouse_pos)
            medpattbutton.update(mouse_pos)
            hardpattbutton.update(mouse_pos)

        elif current_screen == 'patterns_start':
            homebutton.update(mouse_pos)
            start_button.update(mouse_pos)
            howtoplaypattbutton.update(mouse_pos)

        elif current_screen == 'patterns_game':
            homebutton.update(mouse_pos)
            for button in pattern_choice_buttons:
                button.update(mouse_pos)

        elif current_screen == 'sequences_screen':
            homebutton.update(mouse_pos)
            easyseqbutton.update(mouse_pos)
            medseqbutton.update(mouse_pos)
            hardseqbutton.update(mouse_pos)

        elif current_screen == 'sequences_start':
            homebutton.update(mouse_pos)
            start_button.update(mouse_pos)

        elif current_screen == 'sequences_game':
            homebutton.update(mouse_pos)
            for button in sequence_choice_buttons:
                button.update(mouse_pos)

        elif current_screen == 'diff_start':
            start_button.update(mouse_pos)
            diff_start_howto_button.update(mouse_pos)
            homebutton.update(mouse_pos)

        elif current_screen == 'game':
            homebutton.update(mouse_pos)
            if show_changed:
                yes_button.update(mouse_pos)
                no_button.update(mouse_pos)

        elif current_screen == 'score_screen':
            homebutton.update(mouse_pos)
            retrybutton.update(mouse_pos)
            patterns_back_button.update(mouse_pos)

        menu_button.update(mouse_pos)

        if menu_open and menu_x > -MENU_WIDTH:
            account_button.update(mouse_pos)
            howto_button.update(mouse_pos)
            back_home_button.update(mouse_pos)

        # draw everything for the current screen
        screen.fill((255, 255, 255))

        if current_screen == 'main_menu':
            screen.blit(logo_image, (130, 45))
            screen.blit(bgdoodles, (0, 0))
            exit_button.draw(screen)
            select_puzzle_button.draw(screen)
            menu_button.draw(screen)

        elif current_screen == 'select_puzzle':
            screen.blit(bgdoodles, (0, 0))
            screen.blit(logo_image, (130, 45))
            menu_button.draw(screen)
            diff_button.draw(screen)
            patt_button.draw(screen)
            seq_button.draw(screen)
            homebutton.draw(screen)

        elif current_screen == 'account_page':
            screen.blit(welcomuser, (21, 61))
            exit_button.draw(screen)
            menu_button.draw(screen)

        elif current_screen == 'diff_difficulty':
            screen.blit(difftitle, (22, 73))
            menu_button.draw(screen)
            easydiffbutton.draw(screen)
            meddiffbutton.draw(screen)
            harddiffbutton.draw(screen)
            homebutton.draw(screen)

        elif current_screen == 'patterns_screen':
            screen.blit(patternstitle, (22, 30))
            menu_button.draw(screen)
            homebutton.draw(screen)
            easypattbutton.draw(screen)
            medpattbutton.draw(screen)
            hardpattbutton.draw(screen)

        elif current_screen == 'patterns_game':
            # clean white background for the pattern game
            screen.fill((255, 255, 255))

            homebutton.draw(screen)
            menu_button.draw(screen)

            if pattern_sequence:
                draw_pattern_sequence(screen, pattern_sequence, timer_font)

            for button in pattern_choice_buttons:
                button.draw(screen)

        elif current_screen == 'sequences_screen':
            screen.blit(seqtitle, (22, 30))
            menu_button.draw(screen)
            homebutton.draw(screen)
            easyseqbutton.draw(screen)
            medseqbutton.draw(screen)
            hardseqbutton.draw(screen)

        elif current_screen == 'sequences_start':
            screen.blit(seqtitle, (22, 30))
            menu_button.draw(screen)
            start_button.draw(screen)
            homebutton.draw(screen)

        elif current_screen == 'sequences_game':
            screen.fill((255, 255, 255))
            screen.blit(seqtitle, (22, 30))
            level_text = timer_font.render(f'Level {sequence_level} - {sequence_difficulty.title()}', True, (0, 0, 0))
            screen.blit(level_text, (40, 100))
            message_text = timer_font.render(sequence_message, True, (0, 0, 0))
            screen.blit(message_text, (40, 130))
            homebutton.draw(screen)
            menu_button.draw(screen)
            draw_sequence(screen, sequence_sequence, timer_font)
            for button in sequence_choice_buttons:
                button.draw(screen)

        elif current_screen == 'diff_start':
            screen.blit(difftitle, (22, 73))
            menu_button.draw(screen)
            start_button.draw(screen)
            diff_start_howto_button.draw(screen)
            homebutton.draw(screen)

        elif current_screen == 'patterns_start':
            screen.blit(patternstitle, (22, 30))
            menu_button.draw(screen)
            start_button.draw(screen)
            howtoplaypattbutton.draw(screen)
            homebutton.draw(screen)

        elif current_screen == 'how_to_play':
            screen.blit(howtoplaytitle, (161, 68))
            if how_to_play_mode == 'patterns':
                screen.blit(howtoplaypatt, (50, 150))
            else:
                screen.blit(howtoplaydiff, (50, 150))
            homebutton.draw(screen)
            menu_button.draw(screen)

        elif current_screen == 'game':
            screen.fill((255, 255, 255))

            if flashing:
                screen.fill((255, 255, 255))
            else:
                if current_image:
                    img_w = current_image.get_width()
                    img_h = current_image.get_height()
                    img_x = (WIDTH - img_w) // 2
                    img_y = (HEIGHT - img_h) // 2
                    screen.blit(current_image, (img_x, img_y))

            timer_rect = timer_text.get_rect(center=(248, 35))
            screen.blit(timer_text, timer_rect)

            homebutton.draw(screen)
            menu_button.draw(screen)

            if show_changed:
                yes_button.draw(screen)
                no_button.draw(screen)

        elif current_screen == 'score_screen':
            screen.fill((255, 255, 255))
            score_text = timer_font.render(f"Your score: {score}", True, (0, 0, 0))
            screen.blit(score_text, (176, 252))
            homebutton.draw(screen)
            menu_button.draw(screen)
            retrybutton.draw(screen)

        

        if menu_open and menu_x < 0:
            menu_x += MENU_SPEED
            if menu_x > 0:
                menu_x = 0
        elif not menu_open and menu_x > -MENU_WIDTH:
            menu_x -= MENU_SPEED
            if menu_x < -MENU_WIDTH:
                menu_x = -MENU_WIDTH

        pygame.draw.rect(screen, (255, 255, 255), (menu_x, 0, MENU_WIDTH, MENU_HEIGHT))

        if menu_x > -MENU_WIDTH:
            menu_button.draw(screen)
            screen.blit(menuline, (11, 52))
            account_button.draw(screen)
            howto_button.draw(screen)
            back_home_button.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
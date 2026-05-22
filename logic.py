import pygame
pygame.init()
import images
import sys
import random

WIDTH = images.WIDTH
HEIGHT = images.HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT))

MENU_WIDTH = 169
MENU_HEIGHT = HEIGHT
MENU_SPEED = 20
clock = pygame.time.Clock()

timer_font = pygame.font.Font(None, 24)
timer_sec = 0
timer_text = timer_font.render("00:00", True, (0, 0, 0))
timer_running = False

# timer updates every second during gameplay
timer = pygame.USEREVENT + 1
pygame.time.set_timer(timer, 1000)

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
    def __init__(self, position, size, filename):
        self.normal_image = pygame.image.load('images/' + filename)
        self.normal_image = pygame.transform.scale(self.normal_image, size)

        self.hover_image = self.normal_image.copy()
        self.hover_image.fill(
            (40, 40, 40, 0),
            special_flags=pygame.BLEND_RGBA_SUB,
        )

        self.rect = self.normal_image.get_rect(topleft=position)
        self.hovered = False

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, surface):
        # darkens button slightly when hovered
        image = self.hover_image if self.hovered else self.normal_image
        surface.blit(image, self.rect)

    def check_press(self, position):
        return self.rect.collidepoint(position)


class ExitButton(Button):
    def check_press(self, position):
        # closes game when exit is clicked
        if super().check_press(position):
            pygame.quit()
            sys.exit()


def main():
    global timer_sec, timer_running

    menu_x = -MENU_WIDTH
    menu_open = False

    # tracks which screen is currently active
    current_screen = 'main_menu'
    selected_difficulty = None

    # keeps puzzle order for each run
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

    flashing = False
    flash_start = 0
    flash_duration = 300  # controls quick transition flash
    reveal_bonus = 0

    exit_button = ExitButton((139, 424), (221, 65), 'exitButton.png')
    select_puzzle_button = Button((139, 270), (221, 65), 'selectPuzzleButton.png')
    menu_button = Button((18, 18), (24, 24), 'menu.png')
    account_button = Button((3, 88), (94, 24), 'account.png')
    howto_button = Button((3, 163), (115, 20), 'howtoplay.png')
    back_home_button = Button((139, 14), (24, 24), 'backhome.png')

    diff_button = Button((145, 229), (221, 65), 'differences.png')
    patt_button = Button((145, 361), (221, 65), 'patterns.png')
    seq_button = Button((145, 493), (221, 65), 'sequences.png')

    homebutton = Button((455, 18), (24, 24), 'backhome.png')

    easydiffbutton = Button((145, 253), (221, 65), 'easy.png')
    meddiffbutton = Button((145, 384), (221, 65), 'med.png')
    harddiffbutton = Button((145, 515), (221, 65), 'hard.png')

    start_button = Button((139, 316), (221, 65), 'startbutton.png')
    diff_start_howto_button = Button((139, 432), (221, 65), 'howtopla.png')

    yes_button = Button((62, 500), (150, 60), 'yes.png')
    no_button = Button((277, 500), (150, 60), 'no.png')

    retrybutton = Button((144, 418), (212, 60), 'retrybutton.png')

    running = True
    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == timer and timer_running:
                # countdown while game is active
                timer_sec -= 1

                if current_screen == 'game' and not show_changed:
                    game_timer -= 1

                    if game_timer <= 0:
                        # triggers transition flash before reveal
                        flashing = True
                        flash_start = pygame.time.get_ticks()

                if timer_sec <= 0:
                    # game ends when timer hits zero
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
                    if select_puzzle_button.check_press(mouse_pos):
                        current_screen = 'select_puzzle'

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

                        # reset puzzle order each game
                        random.shuffle(puzzles)

                        current_puzzle = 0
                        current_image = getattr(images, puzzles[current_puzzle])
                        show_changed = False

                        game_timer = 5
                        reveal_bonus = 5
                        score = 0

                        current_screen = 'game'

                elif current_screen == 'game':
                    if show_changed and yes_button.check_press(mouse_pos):
                        if puzzle_is_changed:
                            # correct answer
                            score += 1
                            timer_sec += reveal_bonus
                            current_puzzle += 1

                        else:
                            # wrong answer ends run
                            current_screen = 'score_screen'

                    elif show_changed and no_button.check_press(mouse_pos):
                        if not puzzle_is_changed:
                            score += 1
                            timer_sec += reveal_bonus
                            current_puzzle += 1
                        else:
                            current_screen = 'score_screen'

        # wait briefly then reveal image change
        if flashing:
            if pygame.time.get_ticks() - flash_start >= flash_duration:
                puzzle_is_changed = random.choice([True, False])

                # randomly selects changed or original image
                if puzzle_is_changed:
                    current_image = getattr(images, puzzles[current_puzzle] + 'changed')
                else:
                    current_image = getattr(images, puzzles[current_puzzle])

                show_changed = True
                flashing = False

        # converts seconds into mm:ss
        mins = timer_sec // 60
        secs = timer_sec % 60
        timer_text = timer_font.render(f"{mins:02}:{secs:02}", True, (0, 0, 0))

        mouse_pos = pygame.mouse.get_pos()

        # update button hover states depending on screen
        if current_screen == 'main_menu':
            select_puzzle_button.update(mouse_pos)

        elif current_screen == 'game':
            if show_changed:
                yes_button.update(mouse_pos)
                no_button.update(mouse_pos)

        # draw current screen
        screen.fill((255, 255, 255))

        if current_screen == 'game':
            if current_image:
                # keeps image centered regardless of size
                img_w = current_image.get_width()
                img_h = current_image.get_height()
                screen.blit(current_image, ((WIDTH - img_w) // 2,
                                            (HEIGHT - img_h) // 2))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
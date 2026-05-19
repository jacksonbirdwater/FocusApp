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
        image = self.hover_image if self.hovered else self.normal_image
        surface.blit(image, self.rect)

    def check_press(self, position):
        return self.rect.collidepoint(position)
class ExitButton(Button):
    def check_press(self, position):
        if super().check_press(position):
            pygame.quit()
            sys.exit()

def main():
    global timer_sec, timer_running

    menu_x = -MENU_WIDTH
    menu_open = False
    current_screen = 'main_menu'
    selected_difficulty = None

    puzzles = ['image1', 'image2', 'image3', 'image4', 'image5', 'image6', 'image7', 'image8', 'image9', 'image10']
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
    flash_duration = 300  # milliseconds
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
    easypattbutton = Button((145, 253), (221, 65), 'easy.png')
    medpattbutton = Button((145, 384), (221, 65), 'med.png')
    hardpattbutton = Button((145, 515), (221, 65), 'hard.png')
    easyseqbutton = Button((145, 253), (221, 65), 'easy.png')
    medseqbutton = Button((145, 384), (221, 65), 'med.png')
    hardseqbutton = Button((145, 515), (221, 65), 'hard.png')
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
                timer_sec -= 1

                if current_screen == 'game' and not show_changed:
                    game_timer -= 1
                    if game_timer <= 0:
                        # start a short flash before revealing the changed/unchanged image
                        flashing = True
                        flash_start = pygame.time.get_ticks()

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
                    if select_puzzle_button.check_press(mouse_pos):
                        current_screen = 'select_puzzle'
                    elif exit_button.check_press(mouse_pos):
                        pass

                elif current_screen == 'select_puzzle':
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
                    if homebutton.check_press(mouse_pos):
                        current_screen = 'main_menu'

                elif current_screen == 'sequences_screen':
                    if homebutton.check_press(mouse_pos):
                        current_screen = 'main_menu'

                elif current_screen == 'how_to_play':
                    if homebutton.check_press(mouse_pos):
                        current_screen = 'main_menu'

                elif current_screen == 'diff_start':
                    if start_button.check_press(mouse_pos):
                        if selected_difficulty == 'easy':
                            timer_sec = 45
                        elif selected_difficulty == 'medium':
                            timer_sec = 30
                        elif selected_difficulty == 'hard':
                            timer_sec = 15
                        initial_time = timer_sec
                        timer_running = True
                        pygame.time.set_timer(timer, 1000)
                        # randomize puzzle order for this run
                        random.shuffle(puzzles)
                        current_puzzle = 0
                        # Always start with unchanged image
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
                        current_screen = 'diff_start'

                elif current_screen == 'game':
                    if show_changed and yes_button.check_press(mouse_pos):
                        if puzzle_is_changed:
                            print("Correct!")
                            score += 1
                            timer_sec += reveal_bonus
                            current_puzzle += 1
                            if current_puzzle >= len(puzzles):
                                current_screen = 'score_screen'
                            else:
                                show_changed = False
                                game_timer = 5
                                # Always start with unchanged image for next puzzle
                                current_image = getattr(images, puzzles[current_puzzle])
                                current_image_name = puzzles[current_puzzle]
                        else:
                            print("Wrong!")
                            current_screen = 'score_screen'
                    elif show_changed and no_button.check_press(mouse_pos):
                        if not puzzle_is_changed:
                            print("Correct!")
                            score += 1
                            timer_sec += reveal_bonus
                            current_puzzle += 1
                            if current_puzzle >= len(puzzles):
                                current_screen = 'score_screen'
                            else:
                                show_changed = False
                                game_timer = 5
                                reveal_bonus = 5
                                # Always start with unchanged image for next puzzle
                                current_image = getattr(images, puzzles[current_puzzle])
                                current_image_name = puzzles[current_puzzle]
                        else:
                            print("Wrong!")
                            current_screen = 'score_screen'
                    if homebutton.check_press(mouse_pos):
                        current_screen = 'main_menu'
                        timer_running = False
                        pygame.time.set_timer(timer, 0)

                if menu_open and menu_x > -MENU_WIDTH:
                    if account_button.check_press(mouse_pos):
                        current_screen = 'account_page'
                        menu_open = False
                    elif howto_button.check_press(mouse_pos):
                        pass
                    elif back_home_button.check_press(mouse_pos):
                        current_screen = 'main_menu'
                        menu_open = False

        # handle flash timing (non-blocking)
        if flashing:
            if pygame.time.get_ticks() - flash_start >= flash_duration:
                # time to reveal changed/unchanged image
                puzzle_is_changed = random.choice([True, False])
                if puzzle_is_changed:
                    current_image = getattr(images, puzzles[current_puzzle] + 'changed')
                    current_image_name = puzzles[current_puzzle] + 'changed'
                else:
                    current_image = getattr(images, puzzles[current_puzzle])
                    current_image_name = puzzles[current_puzzle]
                show_changed = True
                flashing = False

        mins = timer_sec // 60
        secs = timer_sec % 60
        timer_text = timer_font.render(f"{mins:02}:{secs:02}", True, (0, 0, 0))

        mouse_pos = pygame.mouse.get_pos()

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

        elif current_screen == 'sequences_screen':
            homebutton.update(mouse_pos)
            easyseqbutton.update(mouse_pos)
            medseqbutton.update(mouse_pos)
            hardseqbutton.update(mouse_pos)

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

        menu_button.update(mouse_pos)

        if menu_open and menu_x > -MENU_WIDTH:
            account_button.update(mouse_pos)
            howto_button.update(mouse_pos)
            back_home_button.update(mouse_pos)

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

        elif current_screen == 'sequences_screen':
            screen.blit(seqtitle, (22, 30))
            menu_button.draw(screen)
            homebutton.draw(screen)
            easyseqbutton.draw(screen)
            medseqbutton.draw(screen)
            hardseqbutton.draw(screen)

        elif current_screen == 'diff_start':
            screen.blit(difftitle, (22, 73))
            menu_button.draw(screen)
            start_button.draw(screen)
            diff_start_howto_button.draw(screen)
            homebutton.draw(screen)

        elif current_screen == 'how_to_play':
            screen.blit(howtoplaytitle, (161, 68))
            screen.blit(howtoplaydiff, (50, 150))
            homebutton.draw(screen)
            menu_button.draw(screen)

        elif current_screen == 'game':
            # base background
            screen.fill((255, 255, 255))
            if flashing:
                # draw a brief white flash covering the screen so the transition is hidden
                screen.fill((255, 255, 255))
            else:
                if current_image:
                    # center image dynamically based on its current size
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
            score_text = timer_font.render(f"Your Score: {score}", True, (0, 0, 0))
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
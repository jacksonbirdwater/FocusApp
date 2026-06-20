import pygame
pygame.init()
pygame.mixer.music.load('assets/audio/music1.mp3')
pygame.mixer.music.play(-1)  

import images
import sys
from ui.button import Button, ExitButton
from games.patterns import PatternGame
from games.sequences import SequenceGame
from games.differences import DifferenceGame
from ui.slider import Slider
from data.stats import load as load_stats, record as record_stats


slider = Slider(position=(30, 620), width=200, initial_volume=0.5)

#window / constants
WIDTH = images.WIDTH
HEIGHT = images.HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT))

MENU_WIDTH = 169
MENU_HEIGHT = HEIGHT
MENU_SPEED = 20
clock = pygame.time.Clock()




#fonts & static label surfaces

timer_font = pygame.font.Font(None, 24)

pattern_font = pygame.font.SysFont('Montserrat Thin', 24)
pattern_text_surface = pygame.Surface((400, 29), pygame.SRCALPHA)
pattern_text_surface.fill((0, 0, 0, 0))
pattern_label = pattern_font.render('What comes next in this pattern?', True, (0, 0, 0))
pattern_text_surface.blit(pattern_label, pattern_label.get_rect(center=(200, 14)))

difference_font = pygame.font.SysFont('Montserrat Thin', 32)


#global countdown timer (counts down every second via USEREVENT+1)
TIMER_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TIMER_EVENT, 1000)

timer_sec = 0
timer_running = False
timer_text = timer_font.render('00:00', True, (0, 0, 0))


def start_timer(seconds):
    global timer_sec, timer_running
    timer_sec = seconds
    timer_running = True
    pygame.time.set_timer(TIMER_EVENT, 1000)


def stop_timer():
    global timer_running
    timer_running = False
    pygame.time.set_timer(TIMER_EVENT, 0)


def render_timer():
    global timer_text
    mins = timer_sec // 60
    secs = timer_sec % 60
    timer_text = timer_font.render(f'{mins:02}:{secs:02}', True, (0, 0, 0))



# Image aliases
logo_image      = images.logo_image
menuline        = images.menuline
welcomuser      = images.welcomuser
bgdoodles       = images.bgdoodles
difftitle       = images.difftitle
patternstitle   = images.patternstitle
seqtitle        = images.seqtitle
howtoplaytitle  = images.howtoplaytitle
howtoplaydiff   = images.howtoplaydiff
sunnyedmonds    = images.sunnyedmonds
howtoplaypatt   = images.howtoplaypatt


def get_color_image(color):
    return getattr(images, color)


#main loop

def main():
    global timer_sec, timer_running, timer_text

    #menu slide
    menu_x = -MENU_WIDTH
    menu_open = False

    #screen state
    current_screen = 'main_menu'
    selected_difficulty = None
    last_game_mode = None
    how_to_play_mode = NotImplementedError

    #game objects (created on start)
    diff_game: DifferenceGame | None = None
    pattern_game: PatternGame | None = None
    sequence_game: SequenceGame | None = None

    stats = load_stats()


    #button definitions

    #navigation
    menu_button          = Button((18, 18),   (24, 24),   'menu.png')
    homebutton           = Button((455, 18),  (24, 24),   'backhome.png')
    back_home_button     = Button((3, 88),    (94, 24),   'account.png')
    account_button       = Button((3, 88),    (94, 24),   'account.png')
    howto_button         = Button((3, 163),   (115, 20),  'howtoplay.png')
    exit_button          = ExitButton((139, 424), (221, 65), 'exitButton.png')
    account_back_button  = Button((139, 560), (221, 65), 'homebuttonpost.png')

    #main menu
    select_puzzle_button = Button((139, 270), (221, 65),  'selectPuzzleButton.png')

    #game mode selection
    diff_button          = Button((145, 229), (221, 65),  'differences.png')
    patt_button          = Button((145, 361), (221, 65),  'patterns.png')
    seq_button           = Button((145, 493), (221, 65),  'sequences.png')

    #difficulty (differences)
    easydiffbutton       = Button((145, 253), (221, 65),  'easy.png')
    meddiffbutton        = Button((145, 384), (221, 65),  'med.png')
    harddiffbutton       = Button((145, 515), (221, 65),  'hard.png')

    #difficulty (patterns)
    easypattbutton       = Button((145, 253), (221, 65),  'Easy.png')
    medpattbutton        = Button((145, 384), (221, 65),  'med.png')
    hardpattbutton       = Button((145, 515), (221, 65),  'hard.png')

    #difficulty (sequences)
    easyseqbutton        = Button((145, 253), (221, 65),  'Easy.png')
    medseqbutton         = Button((145, 384), (221, 65),  'med.png')
    hardseqbutton        = Button((145, 515), (221, 65),  'hard.png')

    #shared start / how-to
    start_button              = Button((139, 316), (221, 65), 'startbutton.png')
    diff_start_howto_button   = Button((139, 432), (221, 65), 'howtopla.png')
    howtoplaypattbutton       = Button((139, 432), (221, 65), 'howtoplaypattbutton.png')

    #differences game
    yes_button           = Button((62, 500),  (150, 60),  'yes.png')
    no_button            = Button((277, 500), (150, 60),  'no.png')

    #score screen
    retrybuttondiff      = Button((35, 413), (212, 60),  'retrybutton.png')
    retrybuttonpatt      = Button((35, 413), (212, 60),  'retrybutton.png')
    retrybuttonseq       = Button((35, 413), (212, 60),  'retrybutton.png')
    patterns_back_button = Button((267, 413), (212, 60),  'homebuttonpost.png')

    #pattern colour buttons
    bluebutton   = Button((80,  407), (80, 80), 'patternbuttonblue.png')
    cyanbutton   = Button((210, 407), (80, 80), 'patternbuttoncyan.png')
    greenbutton  = Button((340, 407), (80, 80), 'patternbuttongreen.png')
    orangebutton = Button((40,  511), (80, 80), 'patternbuttonorange.png')
    purplebutton = Button((150, 511), (80, 80), 'patternbuttonpurple.png')
    yellowbutton = Button((273, 511), (80, 80), 'patternbuttonyellow.png')
    redbutton    = Button((380, 511), (80, 80), 'patternbuttonred.png')

    color_buttons = {
        'blue':   bluebutton,
        'cyan':   cyanbutton,
        'green':  greenbutton,
        'orange': orangebutton,
        'purple': purplebutton,
        'yellow': yellowbutton,
        'red':    redbutton,
    }

    #helpers

    def final_score():
        """Return the score from whichever game is active."""
        if last_game_mode == 'differences' and diff_game:
            return diff_game.score
        if last_game_mode == 'patterns' and pattern_game:
            return pattern_game.score
        if last_game_mode == 'sequences' and sequence_game:
            return sequence_game.score
        return 0


    #main loop
  
    running = True
    while running:

        #collect events for games that need the full list
        events = pygame.event.get()

        # handle slider events
        for event in events:
            slider.handle_event(event)

        for event in events:

            if event.type == pygame.QUIT:
                running = False

            #global countdown tick
            if event.type == TIMER_EVENT and timer_running:
                timer_sec -= 1

                # let the differences game know a second has passed
                if current_screen == 'diff_game' and diff_game:
                    diff_game.tick()

                if timer_sec <= 0:
                    timer_sec = 0
                    stop_timer()
                    if last_game_mode:
                        record_stats(stats, last_game_mode, final_score())
                    current_screen = 'score_screen'

            #mouse clicks
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos

                #menu toggle (always active)
                if menu_button.check_press(pos):
                    menu_open = not menu_open

                #menu items (when open)
                if menu_open and menu_x > -MENU_WIDTH:
                    if account_button.check_press(pos):
                        current_screen = 'account_page'
                        menu_open = False
                    elif howto_button.check_press(pos):
                        how_to_play_mode = 'patterns' if current_screen.startswith('patterns') else 'diff'
                        current_screen = 'how_to_play'
                        menu_open = False
                    elif back_home_button.check_press(pos):
                        current_screen = 'main_menu'
                        menu_open = False

                #per-screen click handling

                elif current_screen == 'main_menu':
                    if select_puzzle_button.check_press(pos):
                        current_screen = 'select_puzzle'
                    elif exit_button.check_press(pos):
                        pass  # ExitButton calls sys.exit() internally

                elif current_screen == 'select_puzzle':
                    if diff_button.check_press(pos):
                        current_screen = 'diff_difficulty'
                    elif patt_button.check_press(pos):
                        current_screen = 'patterns_screen'
                    elif seq_button.check_press(pos):
                        current_screen = 'sequences_screen'
                    elif homebutton.check_press(pos):
                        current_screen = 'main_menu'

                #differences

                elif current_screen == 'diff_difficulty':
                    if easydiffbutton.check_press(pos):
                        selected_difficulty = 'easy'
                        current_screen = 'diff_start'
                    elif meddiffbutton.check_press(pos):
                        selected_difficulty = 'medium'
                        current_screen = 'diff_start'
                    elif harddiffbutton.check_press(pos):
                        selected_difficulty = 'hard'
                        current_screen = 'diff_start'
                    elif homebutton.check_press(pos):
                        current_screen = 'main_menu'

                elif current_screen == 'diff_start':
                    if start_button.check_press(pos):
                        diff_game = DifferenceGame(selected_difficulty)
                        last_game_mode = 'differences'
                        start_timer(diff_game.initial_time)
                        current_screen = 'diff_game'
                    elif diff_start_howto_button.check_press(pos):
                        how_to_play_mode = 'diff'
                        current_screen = 'how_to_play'
                    elif homebutton.check_press(pos):
                        current_screen = 'main_menu'

                elif current_screen == 'diff_game':
                    if homebutton.check_press(pos):
                        stop_timer()
                        current_screen = 'main_menu'
                    elif diff_game and diff_game.show_changed:
                        if yes_button.check_press(pos):
                            _, bonus, signal = diff_game.answer(player_says_changed=True)
                            timer_sec += bonus
                            if signal:
                                stop_timer()
                                record_stats(stats, 'differences', diff_game.score)
                                current_screen = signal
                        elif no_button.check_press(pos):
                            _, bonus, signal = diff_game.answer(player_says_changed=False)
                            timer_sec += bonus
                            if signal:
                                stop_timer()
                                record_stats(stats, 'differences', diff_game.score)
                                current_screen = signal

                #patterns

                elif current_screen == 'patterns_screen':
                    if easypattbutton.check_press(pos):
                        selected_difficulty = 'easy'
                        last_game_mode = 'patterns'
                        current_screen = 'patterns_start'
                    elif medpattbutton.check_press(pos):
                        selected_difficulty = 'medium'
                        last_game_mode = 'patterns'
                        current_screen = 'patterns_start'
                    elif hardpattbutton.check_press(pos):
                        selected_difficulty = 'hard'
                        last_game_mode = 'patterns'
                        current_screen = 'patterns_start'
                    elif homebutton.check_press(pos):
                        current_screen = 'main_menu'

                elif current_screen == 'patterns_start':
                    if start_button.check_press(pos):
                        pattern_game = PatternGame(selected_difficulty)
                        last_game_mode = 'patterns'
                        start_timer(pattern_game.initial_time)
                        current_screen = 'patterns_game'
                    elif howtoplaypattbutton.check_press(pos):
                        how_to_play_mode = 'patterns'
                        current_screen = 'how_to_play'
                    elif homebutton.check_press(pos):
                        current_screen = 'main_menu'

                elif current_screen == 'patterns_game':
                    if homebutton.check_press(pos):
                        stop_timer()
                        current_screen = 'main_menu'
                    else:
                        for color, btn in color_buttons.items():
                            if btn.check_press(pos) and pattern_game:
                                pattern_game.answer(color)
                                break

                #sequences

                elif current_screen == 'sequences_screen':
                    if easyseqbutton.check_press(pos):
                        selected_difficulty = 'easy'
                        last_game_mode = 'sequences'
                        current_screen = 'sequences_start'
                    elif medseqbutton.check_press(pos):
                        selected_difficulty = 'medium'
                        last_game_mode = 'sequences'
                        current_screen = 'sequences_start'
                    elif hardseqbutton.check_press(pos):
                        selected_difficulty = 'hard'
                        last_game_mode = 'sequences'
                        current_screen = 'sequences_start'
                    elif homebutton.check_press(pos):
                        current_screen = 'main_menu'

                elif current_screen == 'sequences_start':
                    if start_button.check_press(pos):
                        sequence_game = SequenceGame(selected_difficulty)
                        last_game_mode = 'sequences'
                        start_timer(sequence_game.initial_time)
                        current_screen = 'sequences_game'
                    elif homebutton.check_press(pos):
                        current_screen = 'main_menu'

                elif current_screen == 'sequences_game':
                    if homebutton.check_press(pos):
                        stop_timer()
                        current_screen = 'main_menu'
                    #tile clicks are handled inside sequence_game.update()

                #shared screens

                elif current_screen == 'how_to_play':
                    if homebutton.check_press(pos):
                        current_screen = 'patterns_start' if how_to_play_mode == 'patterns' else 'main_menu'

                elif current_screen == 'account_page':
                    if account_back_button.check_press(pos):
                        current_screen = 'main_menu'

                elif current_screen == 'score_screen':
                    if homebutton.check_press(pos):
                        stop_timer()
                        current_screen = 'main_menu'
                    elif retrybuttonpatt.check_press(pos):
                        if last_game_mode == 'patterns':
                            current_screen = 'patterns_start'
                        elif last_game_mode == 'sequences':
                            current_screen = 'sequences_start'
                        else:
                            current_screen = 'diff_start'
                    elif patterns_back_button.check_press(pos):
                        if last_game_mode == 'patterns':
                            current_screen = 'patterns_screen'
                        elif last_game_mode == 'sequences':
                            current_screen = 'sequences_screen'
                        else:
                            current_screen = 'select_puzzle'

        #per-frame game updates (outside event loop)

        if current_screen == 'diff_game' and diff_game:
            diff_game.update()

        if current_screen == 'sequences_game' and sequence_game:
            signal = sequence_game.update(events)
            if signal == 'score_screen':
                stop_timer()
                record_stats(stats, 'sequences', sequence_game.score)
                current_screen = 'score_screen'

        #timer display
        render_timer()
        mouse_pos = pygame.mouse.get_pos()


        #hover updates
       
        menu_button.update(mouse_pos)

        if current_screen == 'main_menu':
            exit_button.update(mouse_pos)
            select_puzzle_button.update(mouse_pos)
        elif current_screen == 'select_puzzle':
            diff_button.update(mouse_pos)
            patt_button.update(mouse_pos)
            seq_button.update(mouse_pos)
            homebutton.update(mouse_pos)
        elif current_screen == 'diff_difficulty':
            easydiffbutton.update(mouse_pos)
            meddiffbutton.update(mouse_pos)
            harddiffbutton.update(mouse_pos)
            homebutton.update(mouse_pos)
        elif current_screen == 'diff_start':
            start_button.update(mouse_pos)
            diff_start_howto_button.update(mouse_pos)
            homebutton.update(mouse_pos)
        elif current_screen == 'diff_game':
            homebutton.update(mouse_pos)
            if diff_game and diff_game.show_changed:
                yes_button.update(mouse_pos)
                no_button.update(mouse_pos)
        elif current_screen == 'patterns_screen':
            easypattbutton.update(mouse_pos)
            medpattbutton.update(mouse_pos)
            hardpattbutton.update(mouse_pos)
            homebutton.update(mouse_pos)
        elif current_screen == 'patterns_start':
            start_button.update(mouse_pos)
            howtoplaypattbutton.update(mouse_pos)
            homebutton.update(mouse_pos)
        elif current_screen == 'patterns_game':
            homebutton.update(mouse_pos)
            for btn in color_buttons.values():
                btn.update(mouse_pos)
        elif current_screen == 'sequences_screen':
            easyseqbutton.update(mouse_pos)
            medseqbutton.update(mouse_pos)
            hardseqbutton.update(mouse_pos)
            homebutton.update(mouse_pos)
        elif current_screen == 'sequences_start':
            start_button.update(mouse_pos)
            homebutton.update(mouse_pos)
        elif current_screen == 'sequences_game':
            homebutton.update(mouse_pos)
        elif current_screen == 'score_screen':
            homebutton.update(mouse_pos)
            retrybuttonpatt.update(mouse_pos)
            patterns_back_button.update(mouse_pos)
        elif current_screen == 'account_page':
            account_back_button.update(mouse_pos)

        if menu_open and menu_x > -MENU_WIDTH:
            account_button.update(mouse_pos)
            howto_button.update(mouse_pos)
            back_home_button.update(mouse_pos)

        # drawing
        screen.fill((255, 255, 255))

        if current_screen == 'main_menu':
            screen.blit(bgdoodles, (0, 0))
            screen.blit(logo_image, (130, 45))
            select_puzzle_button.draw(screen)
            exit_button.draw(screen)
            menu_button.draw(screen)
            slider.draw(screen)
            screen.blit(sunnyedmonds, (417, 635))

        elif current_screen == 'select_puzzle':
            screen.blit(bgdoodles, (0, 0))
            screen.blit(logo_image, (130, 45))
            diff_button.draw(screen)
            patt_button.draw(screen)
            seq_button.draw(screen)
            homebutton.draw(screen)
            menu_button.draw(screen)

        elif current_screen == 'account_page':
            # background
            screen.fill((255, 255, 255))

            # friendly header
            title_font  = pygame.font.SysFont('Montserrat Thin', 28, bold=True)
            sub_font    = pygame.font.SysFont('Montserrat Thin', 18)
            label_font  = pygame.font.SysFont('Montserrat Thin', 14, bold=True)
            value_font  = pygame.font.SysFont('Montserrat Thin', 22)

            title_surf = title_font.render('My Stats', True, (50, 50, 50))
            screen.blit(title_surf, title_surf.get_rect(center=(WIDTH // 2, 55)))

            welcome_surf = sub_font.render('Here\'s how you\'re getting on!', True, (130, 130, 130))
            screen.blit(welcome_surf, welcome_surf.get_rect(center=(WIDTH // 2, 85)))

            # card colours per mode
            card_colours = {
                'differences': (255, 220, 180),   # warm orange
                'patterns':    (180, 230, 200),   # soft green
                'sequences':   (180, 210, 255),   # sky blue
            }
            icon_labels = {
                'differences': 'Differences',
                'patterns':    'Patterns',
                'sequences':   'Sequences',
            }

            card_x      = 30
            card_w      = WIDTH - 60
            card_h      = 120
            card_radius = 18
            start_y     = 115

            for i, mode in enumerate(['differences', 'patterns', 'sequences']):
                hs  = stats[mode]['high_score']
                gp  = stats[mode]['games_played']
                cy  = start_y + i * (card_h + 14)
                col = card_colours[mode]

                # card shadow
                shadow_rect = pygame.Rect(card_x + 3, cy + 4, card_w, card_h)
                pygame.draw.rect(screen, (200, 200, 200), shadow_rect, border_radius=card_radius)

                # card body
                card_rect = pygame.Rect(card_x, cy, card_w, card_h)
                pygame.draw.rect(screen, col, card_rect, border_radius=card_radius)
                pygame.draw.rect(screen, (255, 255, 255), card_rect, 2, border_radius=card_radius)

                # mode title
                mode_surf = label_font.render(icon_labels[mode], True, (60, 60, 60))
                screen.blit(mode_surf, (card_x + 18, cy + 16))

                # divider line
                pygame.draw.line(screen, (255, 255, 255),
                                 (card_x + 18, cy + 40),
                                 (card_x + card_w - 18, cy + 40), 1)

                # stats row
                hs_label  = sub_font.render('Best Score', True, (90, 90, 90))
                hs_value  = value_font.render(str(hs), True, (40, 40, 40))
                gp_label  = sub_font.render('Games Played', True, (90, 90, 90))
                gp_value  = value_font.render(str(gp), True, (40, 40, 40))

                screen.blit(hs_label,  (card_x + 18,        cy + 52))
                screen.blit(hs_value,  (card_x + 18,        cy + 72))
                screen.blit(gp_label,  (card_x + card_w // 2 + 10, cy + 52))
                screen.blit(gp_value,  (card_x + card_w // 2 + 10, cy + 72))

            account_back_button.draw(screen)
            menu_button.draw(screen)

        elif current_screen == 'diff_difficulty':
            screen.blit(difftitle, (22, 73))
            easydiffbutton.draw(screen)
            meddiffbutton.draw(screen)
            harddiffbutton.draw(screen)
            homebutton.draw(screen)
            menu_button.draw(screen)

        elif current_screen == 'diff_start':
            screen.blit(difftitle, (22, 73))
            start_button.draw(screen)
            diff_start_howto_button.draw(screen)
            homebutton.draw(screen)
            menu_button.draw(screen)

        elif current_screen == 'diff_game':
            if diff_game:
                label_surf = difference_font.render(diff_game.label, True, (0, 0, 0))
                label_rect = label_surf.get_rect(center=(WIDTH // 2, 122))
                screen.blit(label_surf, label_rect)
                diff_game.draw(screen, WIDTH, HEIGHT)
            timer_rect = timer_text.get_rect(center=(248, 35))
            screen.blit(timer_text, timer_rect)
            score_text = timer_font.render(f'Score: {diff_game.score if diff_game else 0}', True, (0, 0, 0))
            screen.blit(score_text, (10, 35))
            homebutton.draw(screen)
            menu_button.draw(screen)
            if diff_game and diff_game.show_changed:
                yes_button.draw(screen)
                no_button.draw(screen)

        elif current_screen == 'patterns_screen':
            screen.blit(patternstitle, (22, 30))
            easypattbutton.draw(screen)
            medpattbutton.draw(screen)
            hardpattbutton.draw(screen)
            homebutton.draw(screen)
            menu_button.draw(screen)

        elif current_screen == 'patterns_start':
            screen.blit(patternstitle, (22, 30))
            start_button.draw(screen)
            howtoplaypattbutton.draw(screen)
            homebutton.draw(screen)
            menu_button.draw(screen)

        elif current_screen == 'patterns_game':
            timer_rect = timer_text.get_rect(center=(248, 35))
            screen.blit(timer_text, timer_rect)
            score_text = timer_font.render(f'Score: {pattern_game.score if pattern_game else 0}', True, (0, 0, 0))
            screen.blit(score_text, (10, 35))
            screen.blit(pattern_text_surface, (50, 161))

            if pattern_game:
                pattern_y = 250
                start_x = 110
                spacing = 70
                for idx, color in enumerate(pattern_game.pattern):
                    x = start_x + idx * spacing
                    if idx == len(pattern_game.pattern) - 1:
                        pygame.draw.circle(screen, (220, 220, 220), (x, pattern_y), 25)
                        pygame.draw.circle(screen, (160, 160, 160), (x, pattern_y), 20, 2)
                    else:
                        img = get_color_image(color)
                        screen.blit(img, img.get_rect(center=(x, pattern_y)))

            for btn in color_buttons.values():
                btn.draw(screen)
            homebutton.draw(screen)
            menu_button.draw(screen)

        elif current_screen == 'sequences_screen':
            screen.blit(seqtitle, (22, 30))
            easyseqbutton.draw(screen)
            medseqbutton.draw(screen)
            hardseqbutton.draw(screen)
            homebutton.draw(screen)
            menu_button.draw(screen)

        elif current_screen == 'sequences_start':
            screen.blit(seqtitle, (22, 30))
            start_button.draw(screen)
            homebutton.draw(screen)
            menu_button.draw(screen)

        elif current_screen == 'sequences_game':
            timer_rect = timer_text.get_rect(center=(248, 35))
            screen.blit(timer_text, timer_rect)
            score_text = timer_font.render(f'Score: {sequence_game.score if sequence_game else 0}', True, (0, 0, 0))
            screen.blit(score_text, (10, 85))
            if sequence_game:
                level_text_font = pygame.font.SysFont('Montserrat Thin', 28)
                level_text = level_text_font.render(
                    f'Level {sequence_game.level} — {selected_difficulty.title()}', True, (0, 0, 0))
                screen.blit(level_text, (10, 120))
                message_text = timer_font.render(sequence_game.message, True, (0, 0, 0))
                screen.blit(message_text, (10, 160))
                sequence_game.draw(screen)
            homebutton.draw(screen)
            menu_button.draw(screen)

        elif current_screen == 'how_to_play':
            screen.blit(howtoplaytitle, (161, 68))
            screen.blit(howtoplaypatt if how_to_play_mode == 'patterns' else howtoplaydiff, (50, 150))
            homebutton.draw(screen)
            menu_button.draw(screen)

        elif current_screen == 'score_screen':
            score_text = timer_font.render(f'Your score: {final_score()}', True, (0, 0, 0))
            screen.blit(score_text, (200, 252))
            homebutton.draw(screen)
            retrybuttonpatt.draw(screen)
            patterns_back_button.draw(screen)
            menu_button.draw(screen)

        # sliding menu overlay (drawn last so it sits on top)
        if menu_open and menu_x < 0:
            menu_x += MENU_SPEED
            if menu_x > 0:
                menu_x = 0
        elif not menu_open and menu_x > -MENU_WIDTH:
            menu_x -= MENU_SPEED
            if menu_x < -MENU_WIDTH:
                menu_x = -MENU_WIDTH

        if menu_x > -MENU_WIDTH:
            pygame.draw.rect(screen, (255, 255, 255), (menu_x, 0, MENU_WIDTH, MENU_HEIGHT))
            screen.blit(menuline, (menu_x + 11, 52))
            account_button.rect.x = menu_x + 3
            howto_button.rect.x = menu_x + 3
            back_home_button.rect.x = menu_x + 3
            account_button.draw(screen)
            howto_button.draw(screen)
            back_home_button.draw(screen)
            menu_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
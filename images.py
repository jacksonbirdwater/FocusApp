import pygame

WIDTH, HEIGHT = 500, 650

# Load and scale all static images
logo_image = pygame.image.load('images/logo.png')
logo_image = pygame.transform.scale(logo_image, (241, 113))
menuline = pygame.image.load('images/sidemenuline.png')
menuline = pygame.transform.scale(menuline, (147, 1))
welcomuser = pygame.image.load('images/welcome.png')
welcomuser = pygame.transform.scale(welcomuser, (255, 39))
bgdoodles = pygame.image.load('images/bgdoodles.png')
bgdoodles = pygame.transform.scale(bgdoodles, (WIDTH, HEIGHT))
difftitle = pygame.image.load('images/difftitle.png')
difftitle = pygame.transform.scale(difftitle, (456, 150))
difficultybg = pygame.image.load('images/difficultybg.png')
difficultybg = pygame.transform.scale(difficultybg, (WIDTH, HEIGHT))
patternstitle = pygame.image.load('images/patternstitle.png')
patternstitle = pygame.transform.scale(patternstitle, (456, 193))
seqtitle = pygame.image.load('images/seqtitle.png')
seqtitle = pygame.transform.scale(seqtitle, (456, 202))
import pygame

WIDTH, HEIGHT = 500, 650

logo_image = pygame.image.load('assets/images/logo.png')
logo_image = pygame.transform.scale(logo_image, (241, 113))
menuline = pygame.image.load('assets/images/sidemenuline.png')
menuline = pygame.transform.scale(menuline, (147, 1))
welcomuser = pygame.image.load('assets/images/welcome.png')
welcomuser = pygame.transform.scale(welcomuser, (255, 39))
bgdoodles = pygame.image.load('assets/images/bgdoodles.png')
bgdoodles = pygame.transform.scale(bgdoodles, (WIDTH, HEIGHT))
difftitle = pygame.image.load('assets/images/difftitle.png')
difftitle = pygame.transform.scale(difftitle, (456, 150))
difficultybg = pygame.image.load('assets/images/difficultybg.png')
difficultybg = pygame.transform.scale(difficultybg, (WIDTH, HEIGHT))
difficultybgg = pygame.image.load('assets/images/difficultybgg.png')
difficultybgg = pygame.transform.scale(difficultybgg, (WIDTH, HEIGHT))
patternstitle = pygame.image.load('assets/images/patternstitle.png')
patternstitle = pygame.transform.scale(patternstitle, (456, 193))
seqtitle = pygame.image.load('assets/images/seqtitle.png')
seqtitle = pygame.transform.scale(seqtitle, (456, 202))
howtoplaytitle = pygame.image.load('assets/images/howtoplaydifftitle.png')
howtoplaytitle = pygame.transform.scale(howtoplaytitle, (178, 68))
howtoplaydiff = pygame.image.load('assets/images/howtoplaydiff.png')
howtoplaydiff = pygame.transform.scale(howtoplaydiff, (400, 400))
howtoplaypatt = pygame.image.load('assets/images/howtoplaypatt.png')
howtoplaypatt = pygame.transform.scale(howtoplaypatt, (400, 400))
textbg = pygame.image.load('assets/images/text.png')
textbg = pygame.transform.scale(textbg, (400, 29))
sunnyedmonds = pygame.image.load('assets/images/sunny edmonds.png')
sunnyedmonds = pygame.transform.scale(sunnyedmonds, (83, 12))
imagechange = pygame.image.load('assets/images/imagechange.png')
imagechange = pygame.transform.scale(imagechange, (397, 39))


#images for differences game
image1 = pygame.image.load('assets/images/image1.png')
image1 = pygame.transform.scale(image1, (400, 267))
image1changed = pygame.image.load('assets/images/image1changed.png')
image1changed = pygame.transform.scale(image1changed, (400, 267))
image2 = pygame.image.load('assets/images/image2.png')
image2 = pygame.transform.scale(image2, (400, 267))
image2changed = pygame.image.load('assets/images/image2changed.png')
image2changed = pygame.transform.scale(image2changed, (400, 267))
image3 = pygame.image.load('assets/images/image3.png')
image3 = pygame.transform.scale(image3, (400, 267))
image3changed = pygame.image.load('assets/images/image3changed.png')
image3changed = pygame.transform.scale(image3changed, (400, 267))
image4 = pygame.image.load('assets/images/image4.png')
image4 = pygame.transform.scale(image4, (400, 267))
image4changed = pygame.image.load('assets/images/image4changed.png')
image4changed = pygame.transform.scale(image4changed, (400, 267))
image5 = pygame.image.load('assets/images/image5.png')
image5 = pygame.transform.scale(image5, (400, 267))
image5changed = pygame.image.load('assets/images/image5changed.png')
image5changed = pygame.transform.scale(image5changed, (400, 267))
image6 = pygame.image.load('assets/images/image6.png')
image6 = pygame.transform.scale(image6, (400, 267))
image6changed = pygame.image.load('assets/images/image6changed.png')
image6changed = pygame.transform.scale(image6changed, (400, 267))
image7 = pygame.image.load('assets/images/image7.png')
image7 = pygame.transform.scale(image7, (400, 267))
image7changed = pygame.image.load('assets/images/image7changed.png')
image7changed = pygame.transform.scale(image7changed, (400, 267))
image8 = pygame.image.load('assets/images/image8.png')
image8 = pygame.transform.scale(image8, (400, 267))
image8changed = pygame.image.load('assets/images/image8changed.png')
image8changed = pygame.transform.scale(image8changed, (400, 267))
image9 = pygame.image.load('assets/images/image9.png')
image9 = pygame.transform.scale(image9, (400, 267))
image9changed = pygame.image.load('assets/images/image9changed.png')
image9changed = pygame.transform.scale(image9changed, (400, 267))
image10 = pygame.image.load('assets/images/image10.png')
image10 = pygame.transform.scale(image10, (400, 267))
image10changed = pygame.image.load('assets/images/image10changed.png')
image10changed = pygame.transform.scale(image10changed, (400, 267))

#images for patterns game
green = pygame.image.load('assets/images/circlegreen.png')
green = pygame.transform.scale(green, (50, 50))
red = pygame.image.load('assets/images/circlered.png')
red = pygame.transform.scale(red, (50, 50))
purple = pygame.image.load('assets/images/circlepurple.png')
purple = pygame.transform.scale(purple, (50, 50))
blue = pygame.image.load('assets/images/circleblue.png')
blue = pygame.transform.scale(blue, (50, 50))
cyan = pygame.image.load('assets/images/circlecyan.png')
cyan = pygame.transform.scale(cyan, (50, 50))
yellow = pygame.image.load('assets/images/circleyellow.png')
yellow = pygame.transform.scale(yellow, (50, 50))
orange = pygame.image.load('assets/images/circleorange.png')
orange = pygame.transform.scale(orange, (50, 50))

blueseq = pygame.image.load('assets/images/blueseq.png')
blueseq = pygame.transform.scale(blueseq, (80, 80))
redseq = pygame.image.load('assets/images/redseq.png')
redseq = pygame.transform.scale(redseq, (80, 80))
greenseq = pygame.image.load('assets/images/greenseq.png')
greenseq = pygame.transform.scale(greenseq, (80, 80))
purpleseq = pygame.image.load('assets/images/purpleseq.png')
purpleseq = pygame.transform.scale(purpleseq, (80, 80))
cyanseq = pygame.image.load('assets/images/cyanseq.png')
cyanseq = pygame.transform.scale(cyanseq, (80, 80))
yellowseq = pygame.image.load('assets/images/yellowseq.png')
yellowseq = pygame.transform.scale(yellowseq, (80, 80))
orangeseq = pygame.image.load('assets/images/orangeseq.png')
orangeseq = pygame.transform.scale(orangeseq, (80, 80))

patternbuttonblue = pygame.image.load('assets/images/patternbuttonblue.png')
patternbuttonblue = pygame.transform.scale(patternbuttonblue, (80, 80))
patternbuttoncyan = pygame.image.load('assets/images/patternbuttoncyan.png')
patternbuttoncyan = pygame.transform.scale(patternbuttoncyan, (80, 80))
patternbuttongreen = pygame.image.load('assets/images/patternbuttongreen.png')
patternbuttongreen = pygame.transform.scale(patternbuttongreen, (80, 80))
patternbuttonorange = pygame.image.load('assets/images/patternbuttonorange.png')
patternbuttonorange = pygame.transform.scale(patternbuttonorange, (80, 80))
patternbuttonpurple = pygame.image.load('assets/images/patternbuttonpurple.png')
patternbuttonpurple = pygame.transform.scale(patternbuttonpurple, (80, 80))
patternbuttonyellow = pygame.image.load('assets/images/patternbuttonyellow.png')
patternbuttonyellow = pygame.transform.scale(patternbuttonyellow, (80, 80))
patternbuttonred = pygame.image.load('assets/images/patternbuttonred.png')
patternbuttonred = pygame.transform.scale(patternbuttonred, (80, 80))

sequence_tiles = [
    patternbuttonblue,
    patternbuttoncyan,
    patternbuttongreen,
    patternbuttonorange,
    patternbuttonpurple,
    patternbuttonyellow,
    patternbuttonred
]

sequence_tiles_lit = [
    blueseq,
    cyanseq,
    greenseq,
    orangeseq,
    purpleseq,
    yellowseq,
    redseq
]


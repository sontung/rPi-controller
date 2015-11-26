import pygame
GLASS                = (  93,  93,  97)
GLASS_SHAD           = (  64,  64,  64)
WINDOW_FRAME         = ( 161,  94,   8)
WINDOW_FRAME_SHAD    = (  82,  47,   3)
screen = pygame.display.set_mode((600,590))
while True:
    img = pygame.image.load("assets\\images\\bg.jpg")
    screen.blit(img, (0, 0))
    pygame.display.update()
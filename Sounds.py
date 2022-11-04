import pygame

# Playing the 'click' sound when the player clicks on the menu
def PlayClickSound():
    pygame.mixer.Channel(0).play(pygame.mixer.Sound('Sounds/MenuClick.wav'))
import pygame

# Playing the 'click' sound when the player clicks on the menu
def PlayClickSound():
    pygame.mixer.Channel(0).play(pygame.mixer.Sound('Sounds/MenuClick.wav'))

def PlayGoldenGearCollection():
    pygame.mixer.Channel(1).play(pygame.mixer.Sound('Sounds/Golden Gear.wav'))
    # pygame.mixer.Channel(0).play(pygame.mixer.Sound('Sounds/Golden Gear.mp3'))
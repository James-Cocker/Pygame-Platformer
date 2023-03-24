import pygame

# Playing the 'click' sound when the player clicks on the menu
def PlayClickSound():
    pygame.mixer.Channel(0).play(pygame.mixer.Sound('Sounds/MenuClick.wav'))

def PlayGoldenGearCollection():
    pygame.mixer.Channel(1).play(pygame.mixer.Sound('Sounds/Golden Gear.wav'))

def PlayerDamagedSound():
    pygame.mixer.Channel(2).play(pygame.mixer.Sound('Sounds/Damaged.wav'))

def VolumeClickSound():
    pygame.mixer.Channel(3).play(pygame.mixer.Sound('Sounds/VolClick.wav'))

def PlayerJumpSound():
    pygame.mixer.Channel(4).play(pygame.mixer.Sound('Sounds/Jump.wav'))

def BlindingSpiderAttackSound():
    pygame.mixer.Channel(5).play(pygame.mixer.Sound('Sounds/Blinding Spider Attack.wav'))

def PlaySpringSound():
    pygame.mixer.Channel(6).play(pygame.mixer.Sound('Sounds/Spring.wav'))

def PlayRespawnSound():
    pygame.mixer.Channel(7).play(pygame.mixer.Sound('Sounds/Respawn.wav'))
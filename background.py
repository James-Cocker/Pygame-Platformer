import pygame

class Background(pygame.sprite.Sprite):    # Used to create a template for the background image, inherit from the parent class 'Sprite'
    def __init__(self,FullPath):     # position, tile size
        super().__init__()           # Run the initialisation routine of pygame's parent class
        self.image = pygame.image.load(FullPath + '.png')
        self.rect = self.image.get_rect(topleft = (0,0))

    def ResetLevel(self, XOffset):
        self.rect.x -= XOffset

    # Will scroll through the level, shifting each tile to the left or right 
    def update(self, XShift):
        self.rect.x += XShift
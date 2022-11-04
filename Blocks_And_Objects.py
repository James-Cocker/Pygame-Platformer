import pygame
from Support import ImportFolder


class Tile(pygame.sprite.Sprite):           # Used to create a template for each tile, inherit from the parent class 'Sprite'
    def __init__(self,pos,size,type):       # position, tile size
        super().__init__()                  # Run the initialisation routine of pygame's parent class
        self.image = pygame.Surface((size,size))    # Create a surface with the dimesnions of the given tile size
        self.rect = self.image.get_rect(topleft = pos)      # Give the rectangle for the surface the same dimensions as the image
        self.type = type                    # Set type of tile
        

        # If deciding to draw the abstract level, the different blocks are colour coded as such
        if type == 'Normal':
            self.image.fill('Gray')
        elif type == 'Damaging':
            self.image.fill('Red')
            self.rect.y += 48
        elif type == 'Platform':
            self.image.fill('Blue')
        elif type == 'Spring':
            self.image.fill('Yellow')
            self.rect.y += 40
        elif type == 'Respawn':
            self.image.fill('Orange')
            self.rect.y += 64
        elif type == 'Portal':
            self.image.fill('Green')
            self.rect.y += 168

    # Will reset level upon player death
    def ResetLevel(self, XOffset, YOffset):
        self.rect.x -= XOffset
        self.rect.y -= YOffset

    # Will scroll through the level, shifting each tile to the left or right 
    def update(self,XShift, YShift):
        self.rect.x += XShift
        self.rect.y += YShift



class RespawnPoint(Tile):
    def __init__(self,pos,size,type):
        super().__init__(pos,size,type)     # Run the initialisation routine of Tile
        # Import assets and set attributes
        self.ImportAssets()
        self.ID = 0                         # Where ID is the number of the respawn point
        self.Status = 'Idle'
        self.PreviousStatus = 'Idle'
        self.FrameIndex = 0
        self.AnimationSpeed = 0.15
        self.Saving = False
        self.image = self.Animations['Idle'][self.FrameIndex]                # Fill the surface with the animation frame 'idle'
        self.rect = self.image.get_rect(midbottom = self.rect.midbottom)                # Give the rectangle for the surface the same dimensions as the image

    def ImportAssets(self):
        # Set arrays for each animation state
        self.Animations = {'Idle':[], 'Saving':[], 'Startup':[]}

        # Add each image to the arrays for later use
        for Animation in self.Animations.keys():
            FullPath = 'SpriteSheets/AnimatedObjects/Save/' + Animation
            self.Animations[Animation] = ImportFolder(FullPath)

    def Animate(self):
        # If we have swapped to a new status, set animation speed (back) to default and frame index to 0
        if self.Status != self.PreviousStatus:
            self.PreviousStatus = self.Status
            self.FrameIndex = 0

        Animation = self.Animations[self.Status]
        self.Animation = Animation 

        # Loop over frame index
        self.FrameIndex += self.AnimationSpeed
        if self.FrameIndex >= len(Animation):
            if self.Status == 'Saving':
                self.Status = 'Idle'
            self.FrameIndex = 0

        # Set image and rect of the respawn point
        self.image = Animation[int(self.FrameIndex)]
        self.rect = self.image.get_rect(midbottom = self.rect.midbottom)

    def update(self, XShift, YShift):
        # Shifting the respawn point, and animating it
        self.rect.x += XShift
        self.rect.y += YShift

        self.Animate()
import pygame
from Support import ImportFolder

class Enemy(pygame.sprite.Sprite):
    def __init__(self, Animations, AnimationsPath, Speed, SpawnPoint):
        super().__init__()
        # Import assets
        self.ImportAssets(Animations, AnimationsPath)
        # Enemy's Attributes
        self.Speed = Speed
        self.Gravity = 10
        # Emeny Animation attributes
        self.FrameIndex = 0
        self.AnimationSpeed = 0.15
        self.FacingRight = True
        self.Status = 'Walk'
        self.PreviousStatus = 'Walk'
        # Enemy's image and rect
        self.image = self.Animations['Walk'][self.FrameIndex]                # Fill the player surface with the animation frame 'Walk'
        self.rect = self.image.get_rect(topleft = SpawnPoint)     # Give the rectangle for the surface the same dimensions as the image

    def ImportAssets(self, Animations, AnimationsPath):
        # Loop through all animations and import it into the array
        self.Animations = Animations

        for Animation in self.Animations.keys():
            FullPath = AnimationsPath + Animation
            self.Animations[Animation] = ImportFolder(FullPath)

    # Will reset enemies upon player death
    def ResetLevel(self, XOffset):
        self.rect.x -= XOffset

    def Death(self):
        self.kill()

    def Animate(self):
        # Reset frame index when switching animation statuses
        if self.Status != self.PreviousStatus:
            self.PreviousStatus = self.Status
            self.FrameIndex = 0

        Animation = self.Animations[self.Status]
        self.Animation = Animation 

        # Loop over frame index
        self.FrameIndex += self.AnimationSpeed
        if self.FrameIndex >= len(Animation):
            self.FrameIndex = 0

        # Set enemy's image and rect
        AnimFrame = Animation[int(self.FrameIndex)]
        if self.FacingRight:
            self.image = AnimFrame
        else:
            self.image = pygame.transform.flip(AnimFrame, True, False)    # We want to flip in the x axis, but not the y axis

        self.rect = self.image.get_rect(midbottom = self.rect.midbottom)

    def update(self, XShift):
        # Update the enemy by moving it along with the world and animating it
        self.rect.x += XShift

        self.Animate()

# First type of enemy
class BlindingSpider(Enemy):
    def __init__(self, SpawnPoint):
        Speed = 3
        Animations = {'Attack':[], 'Walk':[]}
        AnimationsPath = 'SpriteSheets/Enemies/Blinding Spider/'
        super().__init__(Animations, AnimationsPath, Speed, SpawnPoint)

# Second type of enemy
class FlowerEnemy(Enemy):
    def __init__(self):
        Speed = 0.7
        Animations = {'Attack':[], 'Walk':[]}
        AnimationsPath = 'SpriteSheets/Enemies/Flower Enemy/'
        super().__init__(Animations, AnimationsPath, Speed)
    
    def GetStatus(self):
        ()

# Third type of enemy
class WheelBot(Enemy):
    def __init__(self):
        Speed = 0.7
        Animations = {'Attack':[], 'Walk':[]}
        AnimationsPath = 'SpriteSheets/Enemies/Wheel Bot/'
        super().__init__(Animations, AnimationsPath, Speed)
    
    def GetStatus(self):
        print()

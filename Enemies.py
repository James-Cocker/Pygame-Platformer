import pygame
from Support import ImportFolder

class Enemy():
    def __init__(self, Animations, AnimationsPath):
        # Import assets and set attributes
        self.ImportAssets(Animations, AnimationsPath)
        self.Status = 'Walk'
        self.PreviousStatus = 'Walk'
        self.FrameIndex = 0
        self.AnimationSpeed = 0.15
        self.image = self.Animations['Walk'][self.FrameIndex]                # Fill the player surface with the animation frame 'Walk'
        self.rect = self.image.get_rect(midbottom = self.rect.midbottom)     # Give the rectangle for the surface the same dimensions as the image

    def ImportAssets(self, Animations, AnimationsPath):
        # Loop through all animations and import it into the array
        self.Animations = Animations

        for Animation in self.Animations.keys():
            FullPath = AnimationsPath + Animation
            self.Animations[Animation] = ImportFolder(FullPath)

    # def GetStatus():
    #     print()

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
        self.image = Animation[int(self.FrameIndex)]
        self.rect = self.image.get_rect(midbottom = self.rect.midbottom)

    def update(self, XShift, YShift):
        # Update the enemy by moving it along with the world and animating it
        self.rect.x += XShift
        self.rect.y += YShift

        # self.GetStatus()
        self.Animate()

# First type of enemy
class BlindingSpider(Enemy):
    def __init__():
        Animations = {'Attack':[], 'Walk':[]}
        AnimationsPath = 'SpriteSheets/Enemies/Blinding Spider/'
        super().__init__(Animations, AnimationsPath)

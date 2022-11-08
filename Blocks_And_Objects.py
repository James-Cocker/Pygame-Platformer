import pygame
from Support import ImportFolder

# The parent class for each class in this file
class Tile(pygame.sprite.Sprite):           # Used to create a template for each tile, inherit from the parent class 'Sprite'
    def __init__(self,pos,size,TileSize,type):       # position, tile size
        super().__init__()                  # Run the initialisation routine of pygame's parent class
        self.type = type                    # Set type of tile

        self.image = pygame.Surface((size[0],size[1]))             # Create a surface with the dimesnions of the given tile size, where size is a tuple with [0] being its x dimension size
        self.rect = self.image.get_rect(midbottom = (pos[0]+(size[0]/2), pos[1]+(TileSize)))             # Give the rectangle for the surface the same dimensions as the image, where pos is a tuple for the top left 
                                                                                                         # of the image. I have chosen to force this into being the 'midbottom' as when the class is inherited from 
                                                                                                         # animated objects, not all objects are the same height and width (e.g spring).
        # If deciding to draw the abstract level, the different blocks are colour coded as such
        if type == 'Normal':
            self.image.fill('Gray')
        elif type == 'Damaging':
            self.image.fill('Red')
        elif type == 'Platform':
            self.image.fill('Blue')


    # Will reset level upon player death
    def ResetLevel(self, XOffset):
        self.rect.x -= XOffset

    # Will scroll through the level, shifting each tile to the left or right 
    def update(self,XShift):
        self.rect.x += XShift

# Parent class for 'enemy' and the other objects such as 'respawn point'
class AnimatedObject(Tile):
    def __init__(self,pos,size,TileSize,AnimSpeed,type,Animations,FullPath):        # position, tile size
        super().__init__(pos,size,TileSize,type)                  # Run the initialisation routine of pygame's parent class

        self.Animations = Animations            # Set arrays for each animation state
        self.ImportAssets(FullPath)
        self.Status = 'Idle'
        self.PreviousStatus = 'Idle'
        self.FrameIndex = 0
        self.AnimationSpeed = AnimSpeed
        self.image = self.Animations['Idle'][self.FrameIndex]                # Fill the surface with the animation frame 'idle'
        self.rect = self.image.get_rect(midbottom = self.rect.midbottom)                # Give the rectangle for the surface the same dimensions as the image

    def ImportAssets(self, Path):
        # Add each image to the arrays for later use
        for Animation in self.Animations.keys():
            FullPath = Path + Animation
            self.Animations[Animation] = ImportFolder(FullPath)

    def update(self, XShift):           # Override tile's update method as we must animate the object as well
        # Shifting the respawn point, and animating it
        self.rect.x += XShift

        self.Animate()          # Each class has unique animation routines, hence no need to define it and for it to be overriden in each instance of the class


# --- Enemies ---

# Parent Class for each enemy
class Enemy(AnimatedObject):
    def __init__(self, AnimationsPath, Speed, SpawnPoint, Size, TileSize):
        AnimSpeed = 0.15
        type = 'Enemy'
        Animations = {'Attack':[], 'Idle':[]}
        super().__init__(SpawnPoint, Size, TileSize, AnimSpeed, type, Animations, AnimationsPath)
        # Enemy's Attributes
        self.Speed = Speed
        self.Gravity = 10
        self.FacingRight = True

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
            self.image = pygame.transform.flip(AnimFrame, True, False)          # We want to flip in the x axis, but not the y axis
            
        self.rect = self.image.get_rect(midbottom = self.rect.midbottom)

# First type of enemy
class BlindingSpider(Enemy):
    def __init__(self, SpawnPoint, TileSize):
        Speed = 3
        Size = (80, 32)
        AnimationsPath = 'SpriteSheets/Enemies/Blinding Spider/'
        super().__init__(AnimationsPath, Speed, SpawnPoint, Size, TileSize)

# Second type of enemy
class FlowerEnemy(Enemy):
    def __init__(self, SpawnPoint, TileSize):
        Speed = 0.7
        Size =()####################
        AnimationsPath = 'SpriteSheets/Enemies/Flower Enemy/'
        super().__init__(AnimationsPath, Speed, SpawnPoint, Size, TileSize)

# Third type of enemy
class WheelBot(Enemy):
    def __init__(self, SpawnPoint, TileSize):
        Speed = 0.7
        Size = ()###################
        AnimationsPath = 'SpriteSheets/Enemies/Wheel Bot/'
        super().__init__(AnimationsPath, Speed, SpawnPoint, Size, TileSize)
    

# --- General Animated Objects ---

# Portal
class Portal(AnimatedObject):
    def __init__(self, pos, size, TileSize, type):
        Animations = {'Idle':[], 'Warp':[]}
        Path = 'SpriteSheets/AnimatedObjects/Portal/'
        AnimSpeed = 0.15
        super().__init__(pos, size, TileSize, AnimSpeed, type, Animations, Path)     # Run the initialisation routine of Animated object (and hence tile)

    def Animate(self):          # Creating the animate function to be used inside the parent class
        Animation = self.Animations[self.Status]
        self.Animation = Animation 

        # Loop over frame index
        self.FrameIndex += self.AnimationSpeed
        if self.FrameIndex >= len(Animation):
            self.FrameIndex = 0

        # Set image and rect of the respawn point
        self.image = Animation[int(self.FrameIndex)]
        self.rect = self.image.get_rect(midbottom = self.rect.midbottom)

# Respawn point
class RespawnPoint(AnimatedObject):
    def __init__(self, pos, size, TileSize, type):
        Animations = {'Idle':[], 'Saving':[], 'Startup':[]}
        Path = 'SpriteSheets/AnimatedObjects/Save/'
        AnimSpeed = 0.15
        super().__init__(pos, size, TileSize, AnimSpeed, type, Animations, Path)     # Run the initialisation routine of Animated object (and hence tile)
        # Set attributes of respawn point
        self.ID = 0                         # Where ID is the number of the respawn point
        self.Saving = False

    def Animate(self):
        # If we have swapped to a new status, set animation speed (back) to default and frame index to 0
        if self.Status != self.PreviousStatus:
            self.PreviousStatus = self.Status
            self.FrameIndex = 0

        Animation = self.Animations[self.Status]
        self.Animation = Animation 

        # Loop over frame index
        self.FrameIndex += self.AnimationSpeed
        if int(self.FrameIndex) == len(self.Animation) - 1:
            if self.Status == 'Saving':
                self.Status = 'Idle'
            self.FrameIndex = 0

        # Set image and rect of the respawn point
        self.image = Animation[int(self.FrameIndex)]
        self.rect = self.image.get_rect(midbottom = self.rect.midbottom)

# Spring
class Spring(AnimatedObject):
    def __init__(self, pos, size, TileSize, type):
        Animations = {'Idle':[], 'Bounce':[]}
        Path = 'SpriteSheets/AnimatedObjects/Spring/'
        AnimSpeed = 0.3
        super().__init__(pos, size, TileSize, AnimSpeed, type, Animations, Path)     # Run the initialisation routine of Animated object (and hence tile)

    def Animate(self):
        Animation = self.Animations[self.Status]

        # Add onto frame index
        self.FrameIndex += self.AnimationSpeed

        # Set image and rect of spring
        self.image = Animation[int(self.FrameIndex)]
        self.rect = self.image.get_rect(midtop = self.rect.midtop)

        if int(self.FrameIndex) == len(Animation) - 1:
            self.FrameIndex = 0
            self.Status = 'Idle'
            self.Animation = self.Animations[self.Status] 
            self.image = self.Animation[self.FrameIndex]

# Golden Gear
class GoldenGear(AnimatedObject):
    def __init__(self, pos, size, TileSize, type, ToMove):
        Animations = {'Idle':[]}
        Path = 'SpriteSheets/AnimatedObjects/Golden Gear/'
        super().__init__(pos, size, TileSize, 0, type, Animations, Path)     # Run the initialisation routine of Animated object (and hence tile)

        # Set attributes
        InitialYPos = self.rect.y
        self.UpperBound = InitialYPos
        self.LowerBound = InitialYPos + ToMove
        self.Y_ToMove = 0
        self.MoveUp = False

    def Animate(self):
        # Coin floats up and down, so shift y pos up to a certain point, then back down
        self.rect = self.image.get_rect(center = self.rect.center)                # Give the rectangle for the surface the same dimensions as the image
        
        YPos = self.rect.y
        
        if self.MoveUp:
            self.rect.y -= 1
            if YPos < self.UpperBound:
                self.MoveUp = False
        else:
            self.rect.y += 1
            if YPos > self.LowerBound:
                self.MoveUp = True
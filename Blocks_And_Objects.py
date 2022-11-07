import pygame
from Support import ImportFolder


class Tile(pygame.sprite.Sprite):           # Used to create a template for each tile, inherit from the parent class 'Sprite'
    def __init__(self,pos,size,TileSize,type):       # position, tile size
        super().__init__()                  # Run the initialisation routine of pygame's parent class
        self.type = type                    # Set type of tile

        self.image = pygame.Surface((size[0],size[1]))             # Create a surface with the dimesnions of the given tile size, where size is a tuple with [0] being its x dimension size
        self.rect = self.image.get_rect(midbottom = (pos[0]+(size[0]/2), pos[1]+(TileSize)))             # Give the rectangle for the surface the same dimensions as the image, where pos is a tuple for the top left 
                                                                                                         # of the image. I have chosen to force this into being the 'midbottom' as when the class is inherited from 
                                                                                                         # animated objects, not all objects are the same height and width (e.g spring).
        # If deciding to draw the abstract levd2424el, the different blocks are colour coded as such
        if type == 'Normal':
            self.image.fill('Gray')
        elif type == 'Damaging':
            self.image.fill('Red')
        elif type == 'Platform':
            self.image.fill('Blue')
        # Uncomment this, and comment out the filling of images for programmer mode including the animated objects
        # elif type == 'Spring':
        #     self.image.fill('Yellow')
        # elif type == 'Respawn':
        #     self.image.fill('Orange')
        # elif type == 'Portal':
        #     self.image.fill('Green')

    # Will reset level upon player death
    def ResetLevel(self, XOffset):
        self.rect.x -= XOffset

    # Will scroll through the level, shifting each tile to the left or right 
    def update(self,XShift):
        self.rect.x += XShift


class AnimatedObject(Tile):
    def __init__(self,pos,size,TileSize,AnimSpeed,type,Animations,FullPath):        # position, tile size
        super().__init__(pos,size,TileSize,type)                  # Run the initialisation routine of pygame's parent class

        self.Animations = Animations            # Set arrays for each animation state
        self.ImportAssets(FullPath)
        self.ID = 0                         # Where ID is the number of the respawn point
        self.Status = 'Idle'
        self.PreviousStatus = 'Idle'
        self.FrameIndex = 0
        self.AnimationSpeed = AnimSpeed
        self.Saving = False
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


class RespawnPoint(AnimatedObject):
    def __init__(self, pos, size, TileSize, type):
        Animations = {'Idle':[], 'Saving':[], 'Startup':[]}
        Path = 'SpriteSheets/AnimatedObjects/Save/'
        AnimSpeed = 0.15
        super().__init__(pos, size, TileSize, AnimSpeed, type, Animations, Path)     # Run the initialisation routine of Animated object (and hence tile)

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


class GoldenGear(AnimatedObject):
    def __init__(self, pos, size, TileSize, type):
        Animations = {'Idle':[]}
        Path = 'SpriteSheets/AnimatedObjects/Golden Gear/'
        super().__init__(pos, size, TileSize, 0, type, Animations, Path)     # Run the initialisation routine of Animated object (and hence tile)

        # Set attributes
        InitialYPos = self.rect.y
        self.UpperBound = InitialYPos - 64
        self.LowerBound = InitialYPos
        self.Y_ToMove = 0
        self.MoveUp = True

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
import pygame
from pygame import K_SPACE
from Support import ImportFolder
from Sounds import *


class Player(pygame.sprite.Sprite):
    def __init__(self, SpawnPoint, ObtainedDoubleJump, ObtainedDash):
        super().__init__()
        self.ImportAssets()
        self.RespawnPoint = SpawnPoint
        self.FrameIndex = 0             # Used to pick one of the animation frames
        self.AnimationSpeed = 0.15      # How fast image will update
        self.image = self.Animations['Idle'][self.FrameIndex]                # Fill the player surface with the animation frame 'idle'
        self.rect = self.image.get_rect(topleft = SpawnPoint)                # Give the rectangle for the surface the same dimensions as the image

        # Player Movement
        self.Direction = pygame.math.Vector2(0,0)
        self.PlayerSpeed = 8
        self.NormalSpeed = self.PlayerSpeed
        self.Gravity = 0.9
        self.JumpSpeed = -17
        self.OnPlatform = False
        self.IsJumping = False
        self.IsFalling = False
        self.Alive = True

        # Player Abilities
        self.SpacePressed = False
        self.ObtainedDoubleJump = ObtainedDoubleJump
        self.DoubleJump = ObtainedDoubleJump
        self.ObtainedDash = ObtainedDash
        self.Dash = ObtainedDash

        # Player Status
        self.Status = 'Idle'
        self.PreviousStatus  = 'Idle'
        self.FacingRight = True

        # Player collisions
        self.OnCeiling = False
        self.OnGround = False
        self.OnRight = False
        self.OnLeft = False

    def ImportAssets(self):
        # Set arrays for each animation state
        self.Animations = {'Idle':[], 'Run':[], 'Jump':[], 'Dash':[], 'Death':[], 'Fall':[]}

        # Add each image to the arrays for later use
        for Animation in self.Animations.keys():
            FullPath = 'SpriteSheets/PlayerAnimation/' + Animation
            self.Animations[Animation] = ImportFolder(FullPath)
    
    def Animate(self):
        # If we have swapped to a new status, set animation speed (back) to default and frame index to 0
        if self.Status != self.PreviousStatus:
            self.PreviousStatus = self.Status
            self.AnimationSpeed = 0.15
            self.FrameIndex = 0

        Animation = self.Animations[self.Status]
        self.Animation = Animation 
        
        # Loop over frame index
        self.FrameIndex += self.AnimationSpeed
        if self.FrameIndex >= len(Animation):
            self.FrameIndex = 0

        # Flipping player
        AnimFrame = Animation[int(self.FrameIndex)]
        if self.FacingRight:
            self.image = AnimFrame
        else:
            self.image = pygame.transform.flip(AnimFrame, True, False)    # We want to flip in the x axis, but not the y axis

        # Set the rectangle of the player when touching the floor (and hitting walls)
        if self.OnGround:
            if self.ObtainedDoubleJump and self.DoubleJump == False: 
                self.DoubleJump = True

            if self.OnRight:
                self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
            elif self.OnLeft:
                self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
            else:
                self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        
        # Set the rectangle of the player when hitting the ceiling (and hitting walls)
        elif self.OnCeiling and self.OnRight:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.OnCeiling and self.OnLeft:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.OnCeiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)  

    def GetInput(self):
        # Detect whether the player is moving left or right, setting the direction accordingly
        Key = pygame.key.get_pressed()
        if Key[pygame.K_RIGHT]:
            self.Direction.x = 1
            self.FacingRight = True
        elif Key[pygame.K_LEFT]:
            self.Direction.x = -1
            self.FacingRight = False
        else:
            self.Direction.x = 0

        # Test if player is jumping
        if self.SpacePressed:
            self.SpacePressed = False
            # See if player is attempting a normal jump
            if self.IsJumping == False and self.IsFalling == False:
                PlayerJumpSound()
                self.IsJumping = True
                self.Jump(self.JumpSpeed)
            # See if player is double jumping
            elif self.DoubleJump and self.OnGround == False:
                self.DoubleJump = False
                PlayerJumpSound()
                self.IsJumping = True
                self.Jump(self.JumpSpeed + 5)            

    def GetStatus(self):
        # Override all statuses if the player has died
        if self.Alive == False:
            self.Status = 'Death'
        else:
            # Detect player status animation state from direction
            if self.Direction.y < 0:
                self.Status = 'Jump'
                self.AnimationSpeed = 0.2
            elif self.Direction.y > self.Gravity:
                self.Status = 'Fall'
            else:
                # Player is running or idling
                if self.Direction.x != 0 and self.Status != 'Jump':
                    self.Status = 'Run'
                elif self.OnGround:
                    self.Status = 'Idle'
            
    def ApplyGravity(self):
        # Add gravity onto the player
        self.Direction.y += self.Gravity
        self.rect.y += self.Direction.y

    def PlayerDeath(self):
        # Set player death
        self.Direction.x = 0
        self.Alive = False
        self.Status = 'Death'

    def Jump(self, JumpSpeed):
        # Add jump speed onto the y direction (this will decrease over time due to gravity)
        self.Direction.y = JumpSpeed

    def update(self):
        # Update the player's inputs, status and animation
        if self.Alive:
            self.GetInput()
            self.GetStatus()
        self.Animate()

        
        
        
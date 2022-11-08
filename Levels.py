import pygame, time
from Blocks_And_Objects import *
from player import Player
from Enemies import *
from Menu import *
from background import Background

# Set constants
ScreenWidth = 1280
ScreenHeight = 720
TileSize = 64

# Creating the call that will be used for each level
class Level:
    # Creating an initialisation routine
    def __init__(self, level_data, surface, CurrentLevelNum, ProgrammerMode, InGameMenu, ToDisableTimer):
        # Set attributes
        self.TimerFont = pygame.font.SysFont("8-Bit-Madness", 80)
        self.display_surface = surface
        self.CurrentLevelNum = CurrentLevelNum
        self.ProgrammerMode = ProgrammerMode
        
        # Setup Level
        self.setup_level(level_data)

        # Resetting level
        self.DistanceMovedX = 0              # Used to keep track of how far the tileset and background will need to move should the player die
        self.DistanceMovedY = 0
        self.WorldShiftX = 0
        self.CurrentX = 0

        # Menu
        self.InGameMenu = InGameMenu
        self.MenuDisplayed = False
        self.CollectedGoldenGear = False
        self.GoldenGearImg = pygame.image.load('MenuItems/Golden Gear.png').convert_alpha()

        # Timer
        self.ToDisableTimer = ToDisableTimer
        self.LevelStartTime = time.time()

        # Indicates whether the player has beaten the level (hit the portal)
        self.FinishedLevel = False

          
    # Used when generating and to display the level
    def setup_level(self,layout):
        NormalBlock = 142                               # The ID from the abstract .csv file of the tile which repesents a normal block the player is able to stand upon
        DamagingBlocks = [270, 271]                     # Same as above, except for tiles such as spikes
        PlatformBlocks = [58,59,60,61,62,72,73,75,76]   # Platform tiles whereby the player is able to jump on, but will not be used in x-collisions 
        SpringBlock = 281
        RespawnBlock = 305
        PortalBlock = 322
        BlindingSpiderEnemy = 290
        InvisibleEnemyBlock = 286
        goldengear = 307
        PlayerSpawn = 285
        
        
        self.RespawnReached = 0
        self.RespawnPointLocations = []                 # Variable to store the x and y position of each respawn point

        # Setting up the types of sprites for the level tiles and player
        self.tiles = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.springs = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.RespawnPoints = pygame.sprite.Group()
        self.AnimatedObjects = pygame.sprite.Group()
        self.background = pygame.sprite.GroupSingle()

        Path = 'Levels/Level ' + str(self.CurrentLevelNum) + '/Level ' + str(self.CurrentLevelNum)
        self.background.add(Background(Path))

        for RowIndex,Row in enumerate(layout):          # Enumerate gives index and information
            for ColumnIndex,Column in enumerate(Row):           # For each row, cycle through each cell
                # e.g. this will print each cell's contents with the exact row and column 
                # print(f'{RowIndex},{ColumnIndex}:{Column}')
                x = ColumnIndex * TileSize
                y = RowIndex * TileSize   

                # Creating a Tile for each value in the csv file. N ~> Normal, D ~> Damaging, P ~> Platform, S ~> Spring, 1000 ~> Player spawn point
                CurrentValue = int(Column)

                if CurrentValue == NormalBlock:
                    tile = Tile((x,y),(TileSize,TileSize), TileSize, 'Normal')        
                    self.tiles.add(tile)
                if CurrentValue == InvisibleEnemyBlock:
                    tile = Tile((x,y),(TileSize,TileSize), TileSize, 'Normal')        
                    self.tiles.add(tile)
                elif CurrentValue in DamagingBlocks:
                    tile = Tile((x,y),(TileSize,16), TileSize, 'Damaging') 
                    self.tiles.add(tile)
                elif CurrentValue in PlatformBlocks:
                    tile = Tile((x,y),(TileSize,TileSize), TileSize, 'Platform') 
                    self.tiles.add(tile)
                elif CurrentValue == SpringBlock:
                    tile = Spring((x,y), (64,32), TileSize, 'Spring') 
                    self.tiles.add(tile)
                    self.springs.add(tile)
                    self.AnimatedObjects.add(tile)
                elif CurrentValue == RespawnBlock:
                    tile = RespawnPoint((x,y), (64,76), TileSize, 'Respawn')     # Each respawn point will recieve an ID. The first respawn point will recieve an ID of 1   
                    self.tiles.add(tile)
                    self.RespawnPoints.add(tile)
                    self.RespawnPointLocations.append([x,y])
                    self.AnimatedObjects.add(tile)
                elif CurrentValue == PortalBlock:
                    tile = Portal((x,y),(112,164), TileSize, 'Portal')     
                    self.portal = tile   
                    self.tiles.add(tile)
                    self.AnimatedObjects.add(tile)
                elif CurrentValue == BlindingSpiderEnemy:
                    enemy = BlindingSpider((x,y))
                    self.enemies.add(enemy)
                elif CurrentValue == goldengear:
                    tile = GoldenGear((x,y), (48,48), TileSize, 'GoldenGear')
                    self.GoldenGear = tile
                    self.tiles.add(tile)
                    self.AnimatedObjects.add(tile)
                elif CurrentValue == PlayerSpawn:
                    print("Make Player")
                    PlayerSprite = Player((x, y))
                    self.player.add(PlayerSprite)

        self.RespawnPointLocations.sort(key=lambda key:key[0])          # Sort respawn point locations by their x value, then set them IDs. This is because the player will always move through the level left to right,
                                                                        # so the first respawn point will always be the leftmost one

        # Allows for a max of 5 respawn points (not flexible, but a for or while loop is unessesary)
        for RespawnPointNum in self.RespawnPoints:
            if RespawnPointNum.rect.x == self.RespawnPointLocations[0][0]:
                RespawnPointNum.ID = 1
            elif RespawnPointNum.rect.x == self.RespawnPointLocations[1][0]:
                RespawnPointNum.ID = 2
            elif RespawnPointNum.rect.x == self.RespawnPointLocations[2][0]:
                RespawnPointNum.ID = 3
            elif RespawnPointNum.rect.x == self.RespawnPointLocations[3][0]:
                RespawnPointNum.ID = 4
            elif RespawnPointNum.rect.x == self.RespawnPointLocations[4][0]:
                RespawnPointNum.ID = 5

    # A scrolling routine to take the player and see if they are at the preset border. If they are then set
    # the player's speed to 0 and set the entire world to move accordingly at the inverted player speed
    def ScrollX(self, player):
        # getting variables
        player_x = player.rect.centerx      # If you get a 'nonetype' error here, it will mean the csv doesnt have a player spawn point
        Direction_x = player.Direction.x

        # Player borders
        MinPlayerX = 450
        MaxPlayerX = ScreenWidth - MinPlayerX

        # Checking if the player is within the border, if not then move the world as such
        if player_x < MinPlayerX and Direction_x < 0:
            self.WorldShiftX = player.NormalSpeed
            player.PlayerSpeed = 0

        elif player_x > MaxPlayerX and Direction_x > 0:
            self.WorldShiftX = -(player.NormalSpeed)
            player.PlayerSpeed = 0

        else:
            self.WorldShiftX = 0
            player.PlayerSpeed = player.NormalSpeed

    def X_CollisionCheck(self, player):
        # Apply player's horizontal movement
        player.rect.x += player.Direction.x * player.PlayerSpeed

        # Apply enemies horizontal movement
        for Enemy in self.enemies:
            if Enemy.FacingRight: Enemy.rect.x += Enemy.Speed
            else: Enemy.rect.x += -Enemy.Speed
            

        # Now check for collision
        for sprite in self.tiles.sprites():
            # Do not check for x collisions with platforms or spikes, just normal blocks
            if sprite.type == 'Normal':
                # Player x collision
                if sprite.rect.colliderect(player.rect):
                    if player.Direction.x < 0:
                        player.rect.left = sprite.rect.right
                        player.OnLeft = True
                        self.CurrentX = player.rect.left
                    elif player.Direction.x > 0:
                        player.rect.right = sprite.rect.left
                        player.OnRight = True
                        self.CurrentX = player.rect.right

                # Enemy x collision
                for Enemy in self.enemies:
                    if sprite.rect.colliderect(Enemy.rect):
                        Enemy.rect.right = sprite.rect.left
                        Enemy.FacingRight = not Enemy.FacingRight           # Use not operator to invert boolean

        # Resetting 'on left' and 'on right' attributes when player stops or moves in opposite direction
        if player.OnLeft and (player.rect.left < self.CurrentX or player.Direction.x >= 0):
            player.OnLeft = False
        if player.OnRight and (player.rect.left > self.CurrentX or player.Direction.x <= 0):
            player.OnRight = False

    def Y_CollisionCheck(self, player):
        # Apply vertical movement
        player.ApplyGravity()

        # Apply enemies horizontal movement
        for Enemy in self.enemies:
            Enemy.rect.y += Enemy.Gravity

        # Now check for collision
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                # GENERAL PLAYER COLLISION CHECKS:

                # Player has beaten the level and should be put onto the next
                if sprite.type == 'Portal' and sprite.Status != 'Warp':
                    sprite.Status = 'Warp'
                    sprite.FrameIndex = 0

                # Kill player if they land on a set of spikes, or other damaging block
                if sprite.type == 'Damaging':
                    player.PlayerDeath()

                # Bounce player if they hit a spring
                if sprite.type == 'Spring':
                    sprite.Status = 'Bounce'
                    player.IsJumping = True
                    player.OnGround = False
                    player.rect.bottom = sprite.rect.top
                    player.Jump(-20)

                # If they hit a respawn point, check they have not already done so, then set their new spawn point to here
                elif sprite.type == 'Respawn':
                    if self.RespawnReached == sprite.ID - 1:            # If they have reached the next respawn point
                        player.RespawnPoint = (player.rect.x, player.rect.y)
                        self.RespawnReached += 1
                        self.DistanceMovedX = 0              
                        self.DistanceMovedY = 0     
                        sprite.Status = 'Saving'
                        sprite.FrameIndex = 0

                elif sprite.type == 'GoldenGear':
                    PlayGoldenGearCollection()
                    self.CollectedGoldenGear = True
                    sprite.kill()
                

                # PLAYER Y COLLISION CHECKS:

                # If it is none of the above, and it is not a platform then keep them on top of the tile
                elif player.Direction.y > 0 and (sprite.type != 'Platform' or player.OnPlatform):
                    player.rect.bottom = sprite.rect.top
                    player.Direction.y = 0
                    player.IsJumping = False
                    player.OnGround = True
                # If the player hits their head, then reset direction and set on ceiling to true
                elif player.Direction.y < 0 and sprite.type != 'Platform':
                    player.rect.top = sprite.rect.bottom
                    player.Direction.y = 0
                    player.OnCeiling = True

                # If the block is a platform then ensure player is physically above it before applying y collision checks
                if sprite.type == 'Platform' and player.rect.bottom <= sprite.rect.bottom and player.Direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.Direction.y = 0
                    player.IsJumping = False
                    player.OnGround = True
                    player.OnPlatform = True

            # ENEMY Y COLLISION CHECKS
            for Enemy in self.enemies:
                if sprite.rect.colliderect(Enemy.rect):
                    if sprite.type == 'Damaging':
                        Enemy.Death()
                    elif sprite.type ==  'Normal':
                        Enemy.rect.bottom = sprite.rect.top

        
        # Setting player's ground, platform and ceiling attributes
        if player.OnGround and player.Direction.y < 0 or player.Direction.y > 1:
            player.OnGround = False
            player.OnPlatform = False
        if player.OnCeiling and player.Direction.y > 0:
            player.OnCeiling = False

        # 'Direction' will be 0 (or 0.9) when the player is standing still
        # When the player jumps, their direction will be max negative (-17) and arc to 0 as they reach the peak of their jump
        # On their decent (falling), their direction will accelerate (due to gravity) in the positive direction
        # The reason 7 has been chosen is so that the player may have some leaniency when falling off a block and attempting to jump (so that they may fall a little whithout it counting as falling)
        # This, in my opinion, helps with playability and smoothness of the game
        if player.Direction.y >= 7:
            player.IsFalling = True
        else:
            player.IsFalling = False

    def CheckResetLevel(self, player):
        # Check for the player to have died, and finished their death animation before resetting level and player
        if player.Status == 'Death' and int(player.FrameIndex) == len(player.Animation) - 1:
            
            player.FrameIndex = len(player.Animation) - 1

            # Reset Level
            background = self.background.sprite
            background.ResetLevel(self.DistanceMovedX)
            for tile in self.tiles:
                tile.ResetLevel(self.DistanceMovedX)
            self.DistanceMovedX = 0

            # Reset enemies
            for Enemy in self.enemies:
                Enemy.ResetLevel(self.DistanceMovedX)
            
            # Start the startup animation of the respawn point
            for RespawnPointNum in self.RespawnPoints:
                if RespawnPointNum.ID == self.RespawnReached and RespawnPointNum.Status != 'Startup':
                    RespawnPointNum.Status = 'Startup'
                    RespawnPointNum.FrameIndex = 0
                    break

                # Reset Player
                if RespawnPointNum.Status == 'Startup' and (int(RespawnPointNum.FrameIndex) == len(RespawnPointNum.Animation) - 2):
                    player.Direction.y = 0
                    RespawnPointNum.Status = 'Idle'
                    player.FrameIndex = 0
                    player.rect = player.image.get_rect(topleft = player.RespawnPoint)
                    player.Alive = True
             
    def UpdateTimer(self, DisableTimer):
        # Update timer by subtracting current time from level start time
        ElapsedTime = time.time() - self.LevelStartTime

        # If they havent disabled the timer, then display it in the bottom left
        if DisableTimer == False:
            TimerText = self.TimerFont.render("Time: " + str(round(ElapsedTime,1)), True, (255,255,255))
            self.display_surface.blit(TimerText, (50,ScreenHeight-60))
        
    def run(self):
        # --- Drawing and Updating Screen ---

        # Calling the scrolling through level function
        self.tiles.update(self.WorldShiftX)            
        
        # If the user is in "Programmer mode" then display the 'tiles'
        if self.ProgrammerMode:
            # Tiles
            self.tiles.draw(self.display_surface)
        else:
            # Background
            self.background.update(self.WorldShiftX)
            self.background.draw(self.display_surface)

        self.AnimatedObjects.draw(self.display_surface)    


        # --- Check for End of Game ---

        # Check portal's status       
        if self.portal.Status == 'Warp':            # The only time the warp animation is played is when the player has reached the portal
            if (int(self.portal.FrameIndex) == len(self.portal.Animation) - 1):        
                self.FinishedLevel = True


        # --- Animation ---

        # Enemies
        for Enemy in self.enemies:
            Enemy.update(self.WorldShiftX)
            self.display_surface.blit(Enemy.image, (Enemy.rect.x, Enemy.rect.y))


        # --- World shifting and Player ---

        # Check that the portal isnt warping before changing the player or scrolling the world
        if self.portal.Status != 'Warp':
            # Get player
            player = self.player.sprite

            # - World Shifting -

            # Update distance moved by player (for respawn point)
            self.DistanceMovedX += self.WorldShiftX

            # Scroll level
            self.ScrollX(player)


            # - Player -
            self.player.update()
            self.CheckResetLevel(player)

            PlayerWidth = player.rect.width         # Storing the temporary value of the width so the player can be checked for collisions with the correct rect, 
            player.rect.width = 25                  # then it can be put back for when the next animation slide is placed on the rect
            self.portal.rect.y += 156               # Similar with portal, except shift it up and down  
            
            self.X_CollisionCheck(player)           # Check collisions for the x and y directions of the player. This must be done separately so that we know wether 
            self.Y_CollisionCheck(player)           # the player needs to be 'pushed' in the x or y direction of a block

            if player.FacingRight:
                self.display_surface.blit(player.image, (player.rect.x - 24, player.rect.y))
            else:
                self.display_surface.blit(player.image, (player.rect.x - 50, player.rect.y))
            
            player.rect.width = PlayerWidth         # Restore player's rect for the image processing
            self.portal.rect.y -= 156               # Restore portal's rect
        else:
            # Stop shifting world
            self.WorldShiftX = 0


        # Display menu 
        if self.MenuDisplayed:
            self.InGameMenu.update()
            self.InGameMenu.Buttons.draw(self.display_surface)
            self.ToDisableTimer = self.InGameMenu.DisableTimer


        # Updating timer
        self.UpdateTimer(self.ToDisableTimer)
            

        # Display golden gear if collected
        if self.CollectedGoldenGear:
            self.display_surface.blit(self.GoldenGearImg, (ScreenWidth - 100, ScreenHeight - 100))
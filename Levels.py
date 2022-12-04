import pygame, time
from Blocks_And_Objects import *
from player import Player
from Menu import *
from Sounds import *
from background import Background

# Set constants
ScreenWidth = 1280
ScreenHeight = 640
TileSize = 64

# Creating the call that will be used for each level
class Level:
    # Creating an initialisation routine
    def __init__(self, level_data, surface, CurrentLevelNum, ProgrammerMode, InGameMenu, ToDisableTimer, PlayerLivesAndAbilities):
        # Set attributes
        self.TimerFont = pygame.font.SysFont("8-Bit-Madness", 80)
        self.display_surface = surface
        self.CurrentLevelNum = CurrentLevelNum
        self.ProgrammerMode = ProgrammerMode
        self.Scrolling = False

        # Health Bar
        self.PlayerLives = PlayerLivesAndAbilities[0]
        self.HealthBarImg = pygame.image.load('MenuItems/Health Bar/' + str(self.PlayerLives) + '.png').convert_alpha()

        # Player Abilities          
        self.SpacePressed = False           # Used to get the keydown for space, when user presses double jump
        self.ShiftPressed = False           # Used to get the keydown for shift, when user wants to dash
        self.PlayerLivesAndAbilities = PlayerLivesAndAbilities          # An array in the form [ No. of lives (between 1 and 5), double jump collected?, dash collected? ]
        
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
        self.SavedGoldenGear = False            # If saved is true, it means the user has collected the golden gear and hit a check point
        self.GoldenGearImg = pygame.image.load('MenuItems/Golden Gear.png').convert_alpha()

        # Timer
        self.ToDisableTimer = ToDisableTimer
        self.LevelStartTime = time.time()

        # To tell if player has chosen to exit the level
        self.SaveAndExit = False

        # Indicates whether the player has beaten the level (hit the portal)
        self.FinishedLevel = False

          
    # Used when generating and to display the level
    def setup_level(self,layout):
        NormalBlock = 142                               # The ID from the abstract .csv file of the tile which repesents a normal block the player is able to stand upon
        DamagingBlocks = [270, 271]                     # Same as above, except for tiles such as spikes
        PlatformBlocks = [58,59,60,61,62,72,73,75,76]   # Platform tiles whereby the player is able to jump on, but will not be used in x-collisions 
        SpringBlock = 281                               # Ect...
        RespawnBlock = 305
        PortalBlock = 322
        BlindingSpiderEnemy = 290
        WheelBotEnemy = 303
        InvisibleEnemyWall = 286
        goldengear = 307
        PlayerSpawn = 285
        doublejump = 287
        dash = 288
        
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
        self.GoldenGearObj = pygame.sprite.GroupSingle()

        Path = 'Levels/Level ' + str(self.CurrentLevelNum) + '/Level ' + str(self.CurrentLevelNum)
        self.background.add(Background(Path))

        for RowIndex,Row in enumerate(layout):              # Enumerate gives index and information
            for ColumnIndex,Column in enumerate(Row):       # For each row, cycle through each cell
                # e.g. this will print each cell's contents with the exact row and column 
                # print(f'{RowIndex},{ColumnIndex}:{Column}')
                x = ColumnIndex * TileSize
                y = RowIndex * TileSize   

                # Creating a Tile for each value in the csv file. N ~> Normal, D ~> Damaging, P ~> Platform, S ~> Spring, 1000 ~> Player spawn point
                CurrentValue = int(Column)

                if CurrentValue == NormalBlock:
                    tile = Tile((x,y),(TileSize,TileSize), TileSize, 'Normal')        
                    self.tiles.add(tile)
                elif CurrentValue == InvisibleEnemyWall:
                    tile = Tile((x,y),(TileSize,TileSize), TileSize, 'EnemyWall')        
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
                    tile = Portal((x,y),(112,12), TileSize, 'Portal')     
                    self.portal = tile   
                    self.tiles.add(tile)
                    self.AnimatedObjects.add(tile)
                elif CurrentValue == BlindingSpiderEnemy:
                    enemy = BlindingSpider((x,y), TileSize)
                    self.enemies.add(enemy)
                    self.tiles.add(enemy)
                elif CurrentValue == WheelBotEnemy:
                    enemy = WheelBot((x,y), TileSize)
                    self.enemies.add(enemy)
                    self.tiles.add(enemy)
                elif CurrentValue == goldengear:
                    tile = GoldenGear((x,y), (48,48), TileSize, 'GoldenGear', 30)
                    self.GoldenGear = tile
                    self.tiles.add(tile)
                    self.GoldenGearObj.add(tile)
                elif CurrentValue == doublejump:
                    tile = DoubleJump((x,y), (64,58), TileSize, 'DoubleJump', 30)
                    self.tiles.add(tile)
                    self.AnimatedObjects.add(tile)
                elif CurrentValue == dash:
                    tile = Dash((x,y), (46,38), TileSize, 'Dash', 30)
                    self.tiles.add(tile)
                    self.AnimatedObjects.add(tile)
                elif CurrentValue == PlayerSpawn:
                    PlayerSprite = Player((x, y), self.PlayerLivesAndAbilities[1], self.PlayerLivesAndAbilities[2])
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
        new_player_x = player_x + Direction_x

        # Player borders
        MinPlayerX = 450
        MaxPlayerX = ScreenWidth - MinPlayerX

        # Checking if the player is within the border, if not then move the world as such
        if player.Status != 'Death':
            if player.Dashing:
                if (new_player_x < MinPlayerX) or (new_player_x > MaxPlayerX):
                    self.WorldShiftX = -round(Direction_x) * 7
                    player.PlayerSpeed = 0

            else:
                if new_player_x < MinPlayerX and Direction_x < 0:
                    self.WorldShiftX = player.NormalSpeed
                    player.PlayerSpeed = 0

                elif new_player_x > MaxPlayerX and Direction_x > 0:
                    self.WorldShiftX = -(player.NormalSpeed)
                    player.PlayerSpeed = 0

                else:
                    self.WorldShiftX = 0
                    player.PlayerSpeed = player.NormalSpeed
        else:
            self.WorldShiftX = 0
            player.PlayerSpeed = 0

        # Move the level if they are still not within bounds
        if Direction_x == 0:
            if player_x < MinPlayerX - 20:
                self.WorldShiftX += 2
                player.rect.x += 2
            elif player_x > MaxPlayerX + 20:
                self.WorldShiftX -= 2
                player.rect.x -= 2

    def X_CollisionCheck(self, player):
        # Apply player's horizontal movement if the world is not scrolling
        player.rect.centerx += player.Direction.x * player.PlayerSpeed

        # Apply enemies horizontal movement
        for Enemy in self.enemies:
            if Enemy.Status != 'Attack':
                if Enemy.FacingRight: Enemy.rect.x += Enemy.Speed
                else: Enemy.rect.x += -Enemy.Speed
            else:
                if (int(Enemy.FrameIndex) == len(Enemy.Animation) - 1):         # Enemy has finished attack animation
                    Enemy.Status = 'Idle'

        # Now check for collision
        for sprite in self.tiles.sprites():
            # Player x collision
            if sprite.type == 'Normal' and sprite.rect.colliderect(player.rect):            # Do not check for x collisions with platforms or spikes, just normal blocks
                if player.Direction.x < 0:
                    player.rect.left = sprite.rect.right + 5
                    player.OnLeft = True
                    self.CurrentX = player.rect.left
                elif player.Direction.x > 0:
                    player.rect.right = sprite.rect.left - 5
                    player.OnRight = True
                    self.CurrentX = player.rect.right
                else:
                    if player.FacingRight:
                        player.rect.right = sprite.rect.left - 5
                        self.CurrentX = player.rect.right
                    else:
                        player.rect.left = sprite.rect.right + 5
                        self.CurrentX = player.rect.left
            # Enemy x collision
            if sprite.type == 'Normal' or sprite.type == 'EnemyWall':
                for Enemy in self.enemies:
                    if sprite.rect.colliderect(Enemy.rect):
                        if Enemy.FacingRight:
                            Enemy.rect.right = sprite.rect.left
                        else:
                            Enemy.rect.left = sprite.rect.right
                        Enemy.FacingRight = not Enemy.FacingRight           # Use not operator to invert boolean
            
        # Resetting 'on left' and 'on right' attributes when player stops or moves in opposite direction
        if player.OnLeft and (player.rect.left < self.CurrentX or player.Direction.x >= 0):
            player.OnLeft = False
        if player.OnRight and (player.rect.left > self.CurrentX or player.Direction.x <= 0):
            player.OnRight = False

    def Y_CollisionCheck(self, player):
        # Apply vertical movement
        player.ApplyGravity()

        # Kill player if too far down in level
        if player.rect.y > ScreenHeight + 20:
            player.PlayerDeath()

        # Now check for collision
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                # GENERAL PLAYER COLLISION CHECKS:

                # Player has beaten the level and should be put onto the next
                if sprite.type == 'Portal' and sprite.Status != 'Warp':
                    sprite.Status = 'Warp'
                    sprite.FrameIndex = 0

                # Kill player if they land on a set of spikes, or other damaging block
                if sprite.type == 'Damaging' or sprite.type == 'Enemy':
                    player.PlayerDeath()
                    if sprite.type == 'Enemy':
                        if sprite.Status != 'Attack': BlindingSpiderAttackSound()           # As to only play the sound once
                        sprite.Status = 'Attack'

                # Bounce player if they hit a spring
                if sprite.type == 'Spring':
                    PlaySpringSound()
                    sprite.Status = 'Bounce'
                    player.IsJumping = True
                    player.OnGround = False
                    if player.ObtainedDoubleJump: player.DoubleJump = True
                    player.rect.bottom = sprite.rect.top
                    player.Jump(-20)

                # If they hit a respawn point, check they have not already done so, then set their new spawn point to here
                elif sprite.type == 'Respawn':
                    if self.RespawnReached == sprite.ID - 1:            # If they have reached the next respawn point
                        player.RespawnPoint = player.rect.topleft#(player.rect.x, player.rect.y)
                        if self.CollectedGoldenGear:
                            self.SavedGoldenGear = True
                        self.RespawnReached += 1
                        self.DistanceMovedX = 0              
                        self.DistanceMovedY = 0     
                        sprite.Status = 'Saving'
                        sprite.FrameIndex = 0

                elif sprite.type == 'GoldenGear':
                    if self.CollectedGoldenGear == False:
                        PlayGoldenGearCollection()
                        self.CollectedGoldenGear = True

                elif sprite.type == 'DoubleJump':
                    PlayGoldenGearCollection()
                    self.PlayerLivesAndAbilities[1] = True          # An array in the form [ No. of lives (between 1 and 5), double jump collected?, dash collected? ]
                    player.ObtainedDoubleJump = True
                    sprite.kill()

                elif sprite.type == 'Dash':
                    PlayGoldenGearCollection()
                    self.PlayerLivesAndAbilities[2] = True          # An array in the form [ No. of lives (between 1 and 5), double jump collected?, dash collected? ]
                    player.ObtainedDash = True
                    sprite.kill()
                

                # PLAYER Y COLLISION CHECKS:

                # If it is none of the above, and it is not a platform then keep them on top of the tile
                elif player.Direction.y > 0 and (sprite.type == 'Normal' or sprite.type == 'Damaging'):
                    player.rect.bottom = sprite.rect.top
                    player.Direction.y = 0
                    player.IsJumping = False
                    player.OnGround = True
                # If the player hits their head, then reset direction and set on ceiling to true
                elif player.Direction.y < 0 and sprite.type == 'Normal':
                    player.rect.top = sprite.rect.bottom
                    player.Direction.y = 0
                    player.OnCeiling = True

                # If the block is a platform then ensure player is physically above it before applying y collision checks
                if sprite.type == 'Platform' and (player.rect.bottom <= (sprite.rect.top + 10) or player.Direction.y > 10 and player.rect.bottom <= (sprite.rect.bottom - 20)) and player.Direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.Direction.y = 0
                    player.IsJumping = False
                    player.OnGround = True
                    player.OnPlatform = True
        
        # Setting player's ground, platform and ceiling attributes
        if player.OnGround and player.Direction.y < 0 or player.Direction.y > 1:
            player.OnGround = False
            player.OnPlatform = False
        if player.OnCeiling and player.Direction.y > 0:
            player.OnCeiling = False

        # 'Direction' will be 0 (or 0.9) when the player is standing still.
        # When the player jumps, their direction will be max negative (-17) and arc to 0 as they reach the peak of their jump.
        # On their decent, their direction will accelerate (due to gravity) in the positive direction.
        # The reason 10 has been chosen is so that the player may have some leaniency when falling off a block and attempting to jump (so that they may fall a little whithout it counting as falling)
        # This, in my opinion, helps with playability and smoothness of the game
        if player.Direction.y >= 10:
            player.IsFalling = True
        else:
            player.IsFalling = False

    def ChangePlayerLives(self, Amount):
        if self.PlayerLives > 0 and Amount < 0:
            self.PlayerLives -= 1
            if self.SavedGoldenGear == False:
                self.CollectedGoldenGear = False
            PlayerDamagedSound()
        elif self.PlayerLives < 5 and Amount > 0:
            self.PlayerLives += 1
        self.PlayerLivesAndAbilities[0] += Amount
        self.HealthBarImg = pygame.image.load('MenuItems/Health Bar/' + str(self.PlayerLives) + '.png').convert_alpha()

    def CheckResetLevel(self, player):
        # Check for the player to have died, and finished their death animation before resetting level and player
        if player.Status == 'Death' and (int(player.FrameIndex) == len(player.Animation) - 1):
            player.SpacePressed = False         # So that the player does not bounce after being respawned
            player.ShiftPressed = False         # So that the player does not dash after being respawned

            player.FrameIndex = len(player.Animation) - 1         # Keep the player at the last frame of death so this loop will continue

            # Reset Level
            background = self.background.sprite
            background.ResetLevel(self.DistanceMovedX)
            for tile in self.tiles:
                tile.ResetLevel(self.DistanceMovedX)
            
            # Reset distance moved by player (when hitting the barrier)
            self.DistanceMovedX = 0
            
            # Reset Player if they havent hit a respawn point
            if self.RespawnReached == 0:
                self.ChangePlayerLives(-1)
                player.Direction.y = 0
                player.FrameIndex = 0
                player.rect = player.image.get_rect(topleft = player.RespawnPoint)
                player.Alive = True
            else:
                # Start the startup animation of the respawn point
                for RespawnPointNum in self.RespawnPoints:
                    if RespawnPointNum.ID == self.RespawnReached and RespawnPointNum.Status != 'Startup':
                        RespawnPointNum.Status = 'Startup'
                        RespawnPointNum.FrameIndex = 0
                        break

                    # Reset Player
                    if RespawnPointNum.Status == 'Startup' and (int(RespawnPointNum.FrameIndex) == len(RespawnPointNum.Animation) - 2):
                        self.ChangePlayerLives(-1)
                        RespawnPointNum.Status = 'Idle'
                        player.Direction.y = 0
                        player.FrameIndex = 0
                        player.rect = player.image.get_rect(topleft = (player.RespawnPoint[0] + 30, player.RespawnPoint[1] - 30))
                        player.Alive = True
               
    def UpdateTimer(self, DisableTimer):
        # Update timer by subtracting current time from level start time
        self.ElapsedTime = str(round(time.time() - self.LevelStartTime,1))

        # If they havent disabled the timer, then display it in the bottom left
        if DisableTimer == False:
            TimerText = self.TimerFont.render("Time: " + self.ElapsedTime, True, (255,255,255))
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


        # --- Check for End of Game ---

        # Check portal's status       
        if self.portal.Status == 'Warp':            # The only time the warp animation is played is when the player has reached the portal
            if (int(self.portal.FrameIndex) == len(self.portal.Animation) - 1):        
                self.FinishedLevel = True


        # --- Updating Level Objects ---

        # - General Animated Objects -
        self.AnimatedObjects.draw(self.display_surface)   

        # - Enemies -
        for Enemy in self.enemies:          # We are not adding enemies to self.animated objects because we want them to render on top of objects such as springs and portals
            self.display_surface.blit(Enemy.image, (Enemy.rect.x, Enemy.rect.y))

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
            if self.SpacePressed: 
                player.SpacePressed = True
                self.SpacePressed = False
            if self.ShiftPressed:
                player.ShiftPressed = True
                self.ShiftPressed = False

            # Update player and check for level reset
            self.player.update()
            self.CheckResetLevel(player)

            PlayerWidth = player.rect.width         # Storing the temporary value of the width so the player can be checked for collisions with the correct rect, 
            player.rect.width = 25                  # then it can be put back for when the next animation slide is placed on the rect

            self.X_CollisionCheck(player)           # Check collisions for the x and y directions of the player. This must be done separately so that we know wether 
            self.Y_CollisionCheck(player)           # the player needs to be 'pushed' in the x or y direction of a block

            # Draw player
            if player.FacingRight:
                self.display_surface.blit(player.image, (player.rect.x - 24, player.rect.y))
            else:
                self.display_surface.blit(player.image, (player.rect.x - 50, player.rect.y))
            
            player.rect.width = PlayerWidth      # Restore player's rect for the image processing
        else:
            self.WorldShiftX = 0                 # Stop shifting world if warping


        # --- Other ---

        # Display menu 
        if self.MenuDisplayed:
            self.InGameMenu.update()
            self.ToDisableTimer = self.InGameMenu.DisableTimer
            for Button in self.InGameMenu.Buttons:
                if Button.Name == 'Exit' and Button.Clicked:
                    self.SaveAndExit = True

        # Updating timer
        self.UpdateTimer(self.ToDisableTimer)
            
        # Display health bar
        self.display_surface.blit(self.HealthBarImg, (50, 0))

        # Display golden gear in bottom right if collected, otherwise display it on the screen
        if self.CollectedGoldenGear:
            self.display_surface.blit(self.GoldenGearImg, (ScreenWidth - 100, ScreenHeight - 100))
        else:
            self.GoldenGearObj.draw(self.display_surface)
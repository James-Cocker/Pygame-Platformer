# Main things about pygame are surfaces and rectangles
# Surfaces are used to display items
# Rectangles can be used to place items on surfaces, detect collision and much more

# To create a surface: newSurface = pygame.Surface((width,height))
# To display surface:  Screen.blit(Screen,(x,y))     -       Note blit stands for block transfer, to copy the contents of one surface to another

# To create a rectangle: NewRect = pygame.Rect(x,y,w,h)
# Or to create a rectangle around a surface: NewRect = Surface.get_rect(position = (x,y)) where position = 'topright / topleft / centre'
# To draw a rectangle: pygame.draw.Rect(Surface, colour, NewRect)
# To place a rectangle on a surface: Screen.blit(surface, NewRect)

# Placing a sprite on the screen https://www.google.com/search?q=how+to+place+a+sprite+onto+the+screen+python&oq=how+to+place+a+sprite+onto+the+screen+python&aqs=chrome..69i57j33i10i160l2.11378j0j7&sourceid=chrome&ie=UTF-8#kpvalbx=_GFQKY-inBIeA8gKtzYjYCw_13   

# TEXT
# pygame.display.set_caption("Hello World")

#    Defining Font Attributes
# myFont = pygame.font.SysFont("Segoe UI", 90)
# helloWorld = myFont.render("Hello World", 1, (255, 0, 255), (255, 255, 255))
    # Otherwise draw all objects onto the screen
    #Screen.blit(helloWorld, (0, 0))

import pygame,sys
from Levels import *
from Support import ImportCSV
from pygame import mixer

# Initialising pygame
pygame.init()

# Defining size of game window
screen = pygame.display.set_mode((ScreenWidth, ScreenHeight)) 

# Creating clock - to set max frame rate to 60
Clock = pygame.time.Clock()

# Set current level to intro (0th level)
CurrentLevelNum = 0

# Player background game music
mixer.music.load('MenuItems/BackgroundMusic.mp3')
mixer.music.set_volume(0.2)
mixer.music.play()  

# Routine to load and return the next level automatically after the prvious has been completed
def MoveToNextLevel(CurrentLevelNum, TempToDisableTimer):
    CurrentLevelNum += 1
    CSVPath = 'Levels/Level ' + str(CurrentLevelNum) + '/Level ' + str(CurrentLevelNum) + '.csv'
    return Level(ImportCSV(CSVPath), screen, CurrentLevelNum, ProgrammerMode, InGameMenu, TempToDisableTimer), CurrentLevelNum

# Create Menu (only needs to be created once each time the program is loaded - a new menu is not needed for each level)
InGameMenu = CreateInGameMenu((300,100), screen)

# Giving the main file acess to the class Level
ProgrammerMode = False          # Set to true if you would like to see world as the basic rectangles the computer sees 
CurrentLevel = Level(ImportCSV('Levels/Level 0/Level 0.csv'), screen, CurrentLevelNum, ProgrammerMode, InGameMenu, False)


# In-game infinite loop
while True:
    # check if we pressed quit
    for event in pygame.event.get():
        if event.type==pygame.QUIT: sys.exit()
        # Create an in-game menu if escape is pressed
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            # Show menu
            if CurrentLevel.MenuDisplayed == False:
                CurrentLevel.MenuDisplayed = True
            # Hide Menu
            else:
                CurrentLevel.MenuDisplayed = False    

    screen.fill((11, 11, 11))    # Remove the previous frame we drew on the screen by filling it with black (so they do not overlap)

    # Running the next level when the player compltes the first one
    if CurrentLevel.FinishedLevel == False:
        CurrentLevel.run()              
    else:
        TempToDisableTimer = CurrentLevel.ToDisableTimer
        CurrentLevel, CurrentLevelNum = MoveToNextLevel(CurrentLevelNum, TempToDisableTimer)

    # Update the screen and keep the frame rate at 60
    pygame.display.update()
    Clock.tick(60)
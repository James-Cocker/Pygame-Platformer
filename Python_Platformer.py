import pygame, sys
from Levels import *
from Support import *
from pygame import mixer

# Initialising pygame
pygame.init()

# Defining size of game window
screen = pygame.display.set_mode((ScreenWidth, ScreenHeight))

# Creating clock - to set max frame rate to 60
Clock = pygame.time.Clock()

# Set Level Variables
GameWon = False
StartedGame = False
CurrentLevelNum = -1
NumberOfLastLevel = 3
ProgrammerMode = False          # Set to true if you would like to see world as the basic rectangles the computer sees

# Player background game music
mixer.music.load('MenuItems/BackgroundMusic.mp3')
mixer.music.set_volume(0.2)
mixer.music.play()  

# Set player lives and abilities - This is not done in 'player' or 'Levels' as the player should retain their number of lives through the entire playthrough (lives are never reset back to 5)
# This is in the format [ No. of lives (between 1 and 5), double jump collected?, dash collected? ]
PlayerLivesAndAbilities = [5, False, False]

# Routine to load and return the next level automatically after the prvious has been completed
def MoveToNextLevel(CurrentLevelNum, PlayerLivesAndAbilities, MaxLevelReached):
    # Increase max level num if they are progressing through the game (to prevent incrementing by one when player is replaying old levels)
    CurrentLevelNum += 1
    if MaxLevelReached <= CurrentLevelNum:
        MaxLevelReached = CurrentLevelNum
    TempToDisableTimer = CurrentLevel.ToDisableTimer
    CSVPath = 'Levels/Level ' + str(CurrentLevelNum) + '/Level ' + str(CurrentLevelNum) + '.csv'
    return Level(ImportCSV(CSVPath), screen, CurrentLevelNum, ProgrammerMode, InGameMenu, TempToDisableTimer, PlayerLivesAndAbilities), CurrentLevelNum, MaxLevelReached


# --- Name Screen ---

Name = DisplayNameScreen(screen)
MaxLevelReached,PlayerID = LoadLevelsReached(Name)

# Create Menus (only needs to be created once each time the program is loaded)
TitleScreen = CreateTitleScreen(screen)
LevelSelectionScreen = CreateLevelSelectionScreen(screen)
InGameMenu = CreateInGameMenu((300,100), screen)


# --- Title Screen ---

while StartedGame == False:
    for event in pygame.event.get():
        if event.type==pygame.QUIT: sys.exit()
        elif event.type==pygame.MOUSEBUTTONDOWN:
            TitleScreen.MouseDown = True

    screen.fill((11, 11, 11))    # Remove the previous frame we drew on the screen by filling it with black (so they do not overlap)
    TitleScreen.update()

    # Loop through each button in title screen and check for 'start' or 'load game'
    for button in TitleScreen.Buttons:
        if button.Name == 'Start' and button.Clicked:
            CurrentLevelNum = MaxLevelReached
            StartedGame = True
            break
        elif button.Name == 'Load Game' and button.Clicked:
            StartedGame = True
            break

    pygame.display.update()
    Clock.tick(60)


# The indefinite loop when the player has selected 'start' or 'load game'
while True:

    # --- Level selection screen ---

    # Give this its own routine so that when user 'returns' back to level selection screen, their max level reached (and hence the buttons available to them) have updated
    CreateButtonsForLevelSelectionScreen(int(MaxLevelReached), LevelSelectionScreen)

    while CurrentLevelNum == -1:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                SaveScores(MaxLevelReached, PlayerID)
                sys.exit()
            elif event.type==pygame.MOUSEBUTTONDOWN:
                LevelSelectionScreen.MouseDown = True

        screen.fill((11, 11, 11))
        LevelSelectionScreen.update()

        for button in LevelSelectionScreen.Buttons:
            for Num in range(len(LevelSelectionScreen.Buttons)):
                if button.Name == ('Level ' + str(Num)) and button.Clicked:
                    CurrentLevelNum = Num
                    break

        pygame.display.update()
        Clock.tick(60)


    # Giving the main file acess to the class Level
    CSVPath = 'Levels/Level ' + str(CurrentLevelNum) + '/Level ' + str(CurrentLevelNum) + '.csv'
    CurrentLevel = Level(ImportCSV(CSVPath), screen, CurrentLevelNum, ProgrammerMode, InGameMenu, False, PlayerLivesAndAbilities)


    # --- In-game loop ---

    while InGameMenu.Return == False:
        # check if we pressed quit
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                SaveScores(MaxLevelReached, PlayerID)
                sys.exit()
            elif event.type==pygame.MOUSEBUTTONDOWN:
                InGameMenu.MouseDown = True
            # Create an in-game menu if escape is pressed
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Show menu
                    if CurrentLevel.MenuDisplayed == False:
                        CurrentLevel.MenuDisplayed = True
                    # Hide Menu
                    else:
                        CurrentLevel.MenuDisplayed = False
                elif event.key == pygame.K_SPACE:
                    CurrentLevel.SpacePressed = True
                elif event.key == pygame.K_LSHIFT:
                    CurrentLevel.ShiftPressed = True

        screen.fill((11, 11, 11))

        # Running the next level when the player compltes the first one
        if CurrentLevel.FinishedLevel == False:
            CurrentLevel.run()               
        elif int(CurrentLevelNum) < NumberOfLastLevel:
            CurrentLevel, CurrentLevelNum, MaxLevelReached = MoveToNextLevel(int(CurrentLevelNum), PlayerLivesAndAbilities, int(MaxLevelReached))
        else:
            # Display winning screen and return back to menu
            continue

        # Save and exit if the user has chosen to quit the game from pressing 'exit' in the in-game menu
        if CurrentLevel.SaveAndExit:
            SaveScores(MaxLevelReached, PlayerID)
            sys.exit()

        # Update the screen and keep the frame rate at 60
        pygame.display.update()
        Clock.tick(60)

    # Reset Level num, menu return and buttons
    CurrentLevelNum = -1
    InGameMenu.Return = False
    for button in LevelSelectionScreen.Buttons:
        button.Clicked = False
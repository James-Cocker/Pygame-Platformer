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
NumberOfLastLevel = 9
ProgrammerMode = False          # Set to true if you would like to see world as the basic rectangles the computer sees

# Player background game music
mixer.music.load('MenuItems/BackgroundMusic.mp3')
mixer.music.set_volume(0.2)
mixer.music.play()  

# Set player lives and abilities - This is not done in 'player' or 'Levels' as the player should retain their abilities through the entire playthrough
# This is in the format [ No. of lives (between 1 and 5), double jump collected?, dash collected? ]
#PlayerLivesAndAbilities = [5, True, True]

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
MaxLevelReached,PlayerInfo,PlayerID,PlayerLivesAndAbilities = LoadLevelsReached(Name)

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
                SaveScores(MaxLevelReached, PlayerID, PlayerInfo)
                sys.exit()
            elif event.type==pygame.MOUSEBUTTONDOWN:
                LevelSelectionScreen.MouseDown = True

        screen.fill((11, 11, 11))
        LevelSelectionScreen.update()

        # Check for button presses on level selection or stats/ high score screens
        for button in LevelSelectionScreen.Buttons:
            if button.Clicked:
                if 'Level' in button.Name and not('Off' in button.Name):
                    CurrentLevelNum = int(button.Name[-1])
                    break
                elif button.Name == 'See Stats':
                    DisplayStatsScreen(MaxLevelReached,PlayerID,PlayerInfo,screen)
                elif button.Name == 'See High Scores':
                    DisplayHighScoreScreen(MaxLevelReached,PlayerID,PlayerInfo,screen)
                button.Clicked = False

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
                SaveScores(MaxLevelReached, PlayerID, PlayerInfo)
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

        # Running the next level when the player completes the first one
        if CurrentLevel.FinishedLevel == False:
            CurrentLevel.run()
            # Reset Level if all lives are lost
            # if CurrentLevel.LostAllLives:
            #     CurrentLevel = Level(ImportCSV(CSVPath), screen, CurrentLevelNum, ProgrammerMode, InGameMenu, False, PlayerLivesAndAbilities)
        else:
            if int(CurrentLevelNum) != 0:
                PreviousTime = float(PlayerInfo[(int(CurrentLevelNum)*2)])

                # Save level completion time if it has not been filled in (when it = -1.0) or if the player has beaten their prvious score
                if CurrentLevel.ToDisableTimer == False and (float(CurrentLevel.ElapsedTime) < PreviousTime or str(PreviousTime) == "-1.0"):
                    PlayerInfo[(int(CurrentLevelNum)*2)] = str(CurrentLevel.ElapsedTime)
                # Save golden gear separately as long as it is not already true (meaning if the player does one run in a short time without the golden gear, then another and collects the golden gear their saved progress
                # will show them with a short time and still haven collected the golden gear - but this was the desired intent)
                if str(PlayerInfo[1+(int(CurrentLevelNum)*2)]) == 'False':
                    PlayerInfo[1+(int(CurrentLevelNum)*2)] = str(CurrentLevel.CollectedGoldenGear)

            if int(CurrentLevelNum) == NumberOfLastLevel:
                # Save scores and return player back to level selection once game is over
                SaveScores(MaxLevelReached, PlayerID, PlayerInfo)
                InGameMenu.Return = True
            else:
                # Otherwise move to next level
                CurrentLevel, CurrentLevelNum, MaxLevelReached = MoveToNextLevel(int(CurrentLevelNum), PlayerLivesAndAbilities, int(MaxLevelReached))

        # Save and exit if the user has chosen to quit the game from pressing 'exit' in the in-game menu
        if CurrentLevel.SaveAndExit:
            SaveScores(MaxLevelReached, PlayerID, PlayerInfo)
            sys.exit()

        # Update the screen and keep the frame rate at 60
        pygame.display.update()
        Clock.tick(60)

    # Reset Level num, menu return and buttons
    CurrentLevelNum = -1
    InGameMenu.Return = False
    for button in LevelSelectionScreen.Buttons:
        button.Clicked = False
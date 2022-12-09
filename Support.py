from csv import reader
from os import walk
import pygame, sys
from Sounds import *

def ImportFolder(Path):
    SurfaceList = []
    for _,__,ImageFiles in walk(Path):       # Underscore to indicate we do not care about looping through these
        for Image in ImageFiles:
            FullPath = Path + "/" + str(Image)
            ImageSurface = pygame.image.load(FullPath).convert_alpha()
            SurfaceList.append(ImageSurface)
    # Return the list of images for animation
    return SurfaceList

def ImportCSV(Path):
    # Used to import the level's cvs file into an array
    Contents = []
    with open(Path,'r') as Map:         # If this errors, it means there is no 'next map' in the next level 
        CSVReader = reader(Map,delimiter = ',')
        for Row in CSVReader:
            Contents.append(Row)
    return Contents

def DisplayNameScreen(screen):
    # Creating clock - to set max frame rate to 60
    Clock = pygame.time.Clock()
    PressedEnter = False
    NameText = ""
    Font = pygame.font.SysFont("8-Bit-Madness", 50)
    BackgroundImg = pygame.image.load('MenuItems/Menus/Name Screen.png').convert_alpha()

    while PressedEnter == False:
        for event in pygame.event.get():
            if event.type==pygame.QUIT: sys.exit()
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    PressedEnter = True
                    PlayClickSound()
                    return NameText
                elif event.key==pygame.K_BACKSPACE:
                    NameText = NameText[:-1]
                elif len(NameText) <= 9:
                    NameText += event.unicode

        screen.fill((11, 11, 11))
        screen.blit(BackgroundImg, (0,0))

        OutputText = Font.render(NameText, True, (20,20,20))
        screen.blit(OutputText, (528,274))

        pygame.display.update()
        Clock.tick(60)

def ReadFile():
    with open("Players/Players.txt") as PlayersFile:
        Lines = [line.strip().split(",") for line in PlayersFile]
    
    return Lines

def SaveUpdatedFile(Lines):
    with open('Players/Players.txt', mode='w') as PlayersFile:
        FileText = ""
        for PlayerInfo in Lines:
            for Element in PlayerInfo:
                FileText += str(Element) + ","
            FileText = FileText[:len(FileText)-1]       # Taking off last comma
            FileText += "\n"
        
        # Remove the last character ("\") from the text to be written to the txt file - the "n" was already taken off by the last comma shortening
        FileText = FileText[:len(FileText)-1]
        PlayersFile.write(FileText)

def LoadLevelsReached(Name):
    Name = Name.upper()         # Convert name to uppercase so case won't matter with text input
    ListNum = 0                 # To identify which list in the 2d array we are on, so that the player's ID can be saved

    # Open the file and see if the user's name can be found, in which case save their row number (ID) and return their max level reached
    Lines = ReadFile()

    for PlayerInfo in Lines:
        if PlayerInfo[0] == Name:
            PlayerID = ListNum

            if PlayerInfo[len(PlayerInfo)-2] == '1': DoubleJump = True
            else: DoubleJump = False

            if PlayerInfo[len(PlayerInfo)-1] == '1': Dash = True
            else: Dash = False

            PlayerLivesAndAbilities = [5, DoubleJump, Dash]

            return PlayerInfo[1], PlayerInfo, PlayerID, PlayerLivesAndAbilities
        ListNum += 1

    # Otherwise set the player's ID to the next line in the csv file
    PlayerID = ListNum

    # In the format: Name, max level reached, time taken for level 0, golden gear collected? (T/F), time taken for level 1, golden gear collected? (T/F), ect... and the last two are 'double jump collected?(1/0), dash collected?(1/0)' 
    PlayerInfo = [Name,0,-1,False,-1,False,-1,False,-1,False,-1,False,-1,False,-1,False,-1,False,-1,False,-1,False, 0, 0]
    Lines.append(PlayerInfo)

    SaveUpdatedFile(Lines)

    # Creating the new player's lives and abilities to be returned
    PlayerLivesAndAbilities = [5,False,False]

    # If player has just created new entry in the csv then report their max level as 0 and return their ID in table (row num)
    return 0, PlayerInfo, PlayerID, PlayerLivesAndAbilities

def DisplayHighScoreScreen(MaxLevelReached, PlayerID, PlayerInfoToSave, screen):
    # Creating a 2D array of all level times, in the form [[Player 1s Level 1 time, P1s Level 2 time, ect..], [P2s Level 1 time, ect...], ect...]           --- >          Intro level is not stored or displayed in high scores
    AllListsOfLevelTimes = []
    ListOfLevelTimes = []
    IndexesOFTimes = [2,4,6,8,10,12,14,16,18,20]      # Statically set list of indexes as it would be hard to loop through dynamically
    OutputTextLocations = [(180,220),(180,270),(180,320),(180,370),(180,420),(700,220),(700,270),(700,320),(700,370)]         # Same for text locations
    
    Lines = ReadFile()
    for PlayerInfo in Lines:
        for LevelNum in range(9):           # Looping through from 0 to 8 (9 times, once for each level)
            ListOfLevelTimes.append(PlayerInfo[(IndexesOFTimes[LevelNum])])
        AllListsOfLevelTimes.append(ListOfLevelTimes)
        ListOfLevelTimes = []

    # Sort through array of times and put into lists of best times for each level, along with the players name. The lists are in the form [Best time for Level 1, Best time for l2, ect...],[Name of player with best time for Level 1, ect...]
    SortedLevelTimes = []
    SortedPlayerNames = []
    for LevelNum in range(9):
        BestPlayer = ""
        LowestTime = 9000.0
        for PlayerNum in range(len(AllListsOfLevelTimes)):
            CurrentVal = AllListsOfLevelTimes[PlayerNum][LevelNum]
            if CurrentVal != "-1" and float(CurrentVal) <= float(LowestTime):
                LowestTime = CurrentVal
                BestPlayer = Lines[PlayerNum][0]
        SortedLevelTimes.append(LowestTime)
        SortedPlayerNames.append(BestPlayer)

    # Display background and have the text overlay this
    Background = pygame.image.load('MenuItems/Menus/High Scores Screen.png').convert_alpha()
    screen.blit(Background, (0,0))

    Font = pygame.font.SysFont("8-Bit-Madness", 45)
    for LevelNum in range(9):
        Text = "Level " + str(LevelNum+1) + ": " + SortedLevelTimes[LevelNum] + "s (" + SortedPlayerNames[LevelNum] + ")"
        OutputText = Font.render(Text, True, (0,0,0))
        screen.blit(OutputText, OutputTextLocations[LevelNum])
    pygame.display.update()

    # Then pause the screen until the user presses a key
    ReturnUponKeyPress(MaxLevelReached, PlayerID, PlayerInfoToSave)
    
def DisplayStatsScreen(MaxLevelReached, PlayerID, PlayerInfo, screen):
    Background = pygame.image.load('MenuItems/Menus/Stats Screen.png').convert_alpha()
    GoldenGear = pygame.image.load('MenuItems/Golden Gear Stats.png').convert_alpha()
    screen.blit(Background, (0,0))

    IndexesOFTimes = [2,4,6,8,10,12,14,16,18]      # Statically set list of indexes
    OutputTextLocations = [(330,220),(330,270),(330,320),(330,370),(330,420),(700,220),(700,270),(700,320),(700,370)]         # Same for text locations

    Font = pygame.font.SysFont("8-Bit-Madness", 45)
    for LevelNum in range(9):           # Loops through all 9 levels in the order 0 to 8
        if PlayerInfo[(IndexesOFTimes[LevelNum])] != -1:
            print(PlayerInfo,PlayerInfo[1+(LevelNum*2)], str(1+LevelNum*2))
            if str(PlayerInfo[3+(LevelNum*2)]) == 'True':
                screen.blit(GoldenGear, (OutputTextLocations[LevelNum][0] - 45, OutputTextLocations[LevelNum][1] - 5))
            
            Text = "Level " + str(LevelNum+1) + ": " + PlayerInfo[(IndexesOFTimes[LevelNum])] + "s"
            OutputText = Font.render(Text, True, (0,0,0))
            screen.blit(OutputText, OutputTextLocations[LevelNum])
    pygame.display.update()

    ReturnUponKeyPress(MaxLevelReached, PlayerID, PlayerInfo)

def ReturnUponKeyPress(MaxLevelReached, PlayerID, PlayerInfo):
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT: 
                SaveScores(MaxLevelReached, PlayerID, PlayerInfo)
                sys.exit()
            elif event.type==pygame.KEYDOWN:
                PlayClickSound()
                return

def SaveScores(MaxLevelReached, PlayerID, PlayerInfo):
    # Open the file and see if the user's name can be found, in which case save their row number (ID) and return their max level reached
    Lines = ReadFile()

    PlayerInfo[1] = MaxLevelReached
    Lines[PlayerID] = PlayerInfo

    SaveUpdatedFile(Lines)
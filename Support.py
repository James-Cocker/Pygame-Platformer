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
            return PlayerInfo[1], PlayerID
        ListNum += 1
    # Otherwise set the player's ID to the next line in the csv file
    PlayerID = ListNum

    # In the format: Name, max level reached, time taken for level 1, golden gear collected? (T/F), time taken for level 2, golden gear collected? (T/F), ect...
    Lines.append([Name,0,-1,False,-1,False,-1,False,-1,False,-1,False,-1,False,-1,False,-1,False,-1,False])

    SaveUpdatedFile(Lines)

    # If player has just created new entry in the csv then report their max level as 0 and return their ID in table (row num)
    return 0, PlayerID

def LoadScores():
    print()

def SaveScores(MaxLevelReached, PlayerID):
    # Open the file and see if the user's name can be found, in which case save their row number (ID) and return their max level reached
    Lines = ReadFile()
    Lines[PlayerID][1] = MaxLevelReached

    SaveUpdatedFile(Lines)
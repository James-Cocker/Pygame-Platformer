from csv import reader
from os import walk
import pygame, sys

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
                    return NameText
                elif event.key==pygame.K_BACKSPACE:
                    NameText = NameText[:-1]
                elif len(NameText) <= 9:
                    NameText += event.unicode

        screen.fill((11, 11, 11))
        screen.blit(BackgroundImg, (0,0))

        OutputText = Font.render(NameText, True, (160,160,160))
        screen.blit(OutputText, (528,274))

        pygame.display.update()
        Clock.tick(60)
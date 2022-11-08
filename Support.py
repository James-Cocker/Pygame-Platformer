from csv import reader
from os import walk     # Walk returns 3 things: directory path, directory name, file names (we only want the file names here)
import pygame

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

import pygame, sys
from pygame import mixer
from Sounds import *
from Support import *

global Volume
global RecordedVolume
Volume = 0.2
RecordedVolume = Volume


def CreateInGameMenu(MenuOffset, Screen):
    menu = Menu('MenuItems/Menus/Menu.png', Screen, "In-Game Menu")

    ButtonsToMake = [['ArrowDown',201,182],['ArrowUp',434,182],['Volume',252,189],['Timer',252,240],['Return',259,290],['Exit',281,341]]
    menu.CreateButtons(ButtonsToMake, MenuOffset)

    return menu


def CreateTitleScreen(Screen):
    menu = Menu('MenuItems/Menus/Title Screen.png', Screen, "Title Screen")

    ButtonsToMake = [['Start',544,300], ['Load Game',524,371]]
    menu.CreateButtons(ButtonsToMake, (0,0))

    return menu


def CreateLevelSelectionScreen(Screen):
    menu = Menu('MenuItems/Menus/Level Selection Screen.png', Screen, "Level Selection Screen")

    return menu


def CreateButtonsForLevelSelectionScreen(MaxLevelReached, LevelSelectionScreen):
    for button in LevelSelectionScreen.Buttons:
        button.kill()

    ButtonsToMake = [['Level 0',550,197],['Level 1',244,277],['Level 2',550,277],['Level 3',856,277],['Level 4',244,357],['Level 5',550,357],['Level 6',856,357],['Level 7',244,436],['Level 8',550,436],['Level 9',856,436],['See Stats',158,183],['See High Scores',907,183],]

    # Loop through each button and set it to the 'off' image if the user is unable to press it 
    Counter = 0
    for Button in ButtonsToMake:
        if Counter > MaxLevelReached and Counter <= 9:
            Button[0] += " Off"
        Counter += 1
    
    LevelSelectionScreen.CreateButtons(ButtonsToMake, (0,0))


class Menu():
    def __init__(self, MenuBackgroundImgPath, Screen, MenuType):
        # Displaying Menu
        self.image = pygame.image.load(MenuBackgroundImgPath).convert_alpha()
        self.rect = self.image.get_rect()
        self.DisplaySurface = Screen
        self.DisplayingMenu = False
        self.MenuType = MenuType 
        self.Return = False         # Indicates if player has pressed 'Return' in the in-game menu
        
        # Buttons
        self.Buttons = pygame.sprite.Group()
        self.MouseDown = False

        # Setup for specific menus
        if MenuType == "In-Game Menu":
            self.DisableTimer = False
        elif MenuType == "Level Selection Screen":
            self.MaxLevelReached = 0

            
    def CreateButtons(self, Buttons, MenuOffset):
        # Set Offset
        self.MenuOffset = MenuOffset

        # Create buttons
        for ButtonNum in range(len(Buttons)):
            ButtonName = Buttons[ButtonNum][0]
            FullPath = "MenuItems/Buttons/" + str(ButtonName) + ".png"
            ButtonImage = pygame.image.load(FullPath).convert_alpha()
            button = Button(ButtonName, Buttons[ButtonNum][1], Buttons[ButtonNum][2], ButtonImage)
            self.Buttons.add(button)

        if self.MenuType == "In-Game Menu":
            # Add offset to buttons
            for button in self.Buttons:
                button.rect.x += MenuOffset[0]
                button.rect.y += MenuOffset[1]

    def update(self):
        # Refresh images
        self.DisplaySurface.blit(self.image, self.MenuOffset)
        self.Buttons.draw(self.DisplaySurface)
        
        # Call buttons' update routine when the user clicks the mouse
        if self.MouseDown:
            # Update each button
            for button in self.Buttons:
                button.update()

                # Check if timer has been disabled
                if button.Name == 'Timer':
                    if button.On == False:
                        self.DisableTimer = True
                    else:
                        self.DisableTimer = False

                elif button.Name == 'Return' and button.Clicked:
                    self.Return = True
                    button.Clicked = False

            # Reset mouse down
            self.MouseDown = False


class Button(pygame.sprite.Sprite):
    def __init__(self, Name, ButtonPosX, ButtonPosY, Img):
        super().__init__()
        # Give the timer and volume buttons an 'off' and 'on' to check for later
        if Name == 'Timer' or Name == 'Volume':     # For the two togglable buttons
            self.On = True
        
        # Set attributes
        self.Name = Name
        self.image = Img
        self.rect = self.image.get_rect()
        self.rect.topleft = (ButtonPosX, ButtonPosY)
        self.Clicked = False
    
    def update(self):
        # Get mouse pos
        MousePos = pygame.mouse.get_pos()

        # Check if the mouse is colliding with the button. No need to check whether the mouse is being clicked as the update function is only run when this happens
        if self.rect.collidepoint(MousePos):
            # Play click sound for anything other the vol up and down buttons (as the user will typically press these multiple times within a short interval)
            if self.Name != 'ArrowDown' and self.Name != 'ArrowUp':
                PlayClickSound()

            # Get volume and recorded volume
            global Volume
            global RecordedVolume

            # Set each button the attribute 'clicked'
            self.Clicked = True
            
            # --- Buttons for in-game menu ---

            # Button has been clicked
            if self.Name == 'ArrowDown' and Volume >= 0.1 and Volume != -1:
                # Turn music down by 0.1
                Volume -= 0.1
                RecordedVolume = Volume
                VolumeClickSound()

            elif self.Name == 'ArrowUp' and Volume <= 0.9 and Volume != -1:
                # Turn music up by 0.1
                Volume += 0.1
                RecordedVolume = Volume
                VolumeClickSound()
                
            elif self.Name == 'Volume':
                # Mute music
                if self.On:
                    self.image = pygame.image.load("MenuItems/Buttons/VolumeOff.png").convert_alpha()
                    self.On = False
                    Volume = -1
                # Unute music
                else:
                    self.image = pygame.image.load("MenuItems/Buttons/Volume.png").convert_alpha()
                    self.On = True
                    Volume = RecordedVolume

            elif self.Name == 'Timer':
                # Hide timer
                if self.On:
                    self.image = pygame.image.load("MenuItems/Buttons/TimerOff.png").convert_alpha()
                    self.On = False

                # Display timer
                else:
                    self.image = pygame.image.load("MenuItems/Buttons/Timer.png").convert_alpha()
                    self.On = True

            # Ensure the volume is a float to 1 d.p
            Volume = round(Volume, 1)
            # Check if volume has been set to off
            if Volume == -1:
                mixer.music.set_volume(0)
            # Otherwise set volume to new volume
            else:
                mixer.music.set_volume(Volume)

        # To check if the user has stopped clicking
        if pygame.mouse.get_pressed()[0] == 0:
            self.Clicked = False
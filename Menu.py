import pygame, sys
from pygame import mixer
from Sounds import *

global Volume
global RecordedVolume
Volume = 0.2
RecordedVolume = Volume


def CreateInGameMenu(MenuOffset, Screen):
    menu = Menu('MenuItems/Menu.png', Screen)

    ButtonsToMake = [['ArrowDown',201,182],['ArrowUp',434,182],['Volume',252,189],['Timer',252,240],['Return',259,290],['Exit',281,341]]
    menu.CreateButtons(ButtonsToMake, MenuOffset)

    return menu


class Menu():
    def __init__(self, MenuBackgroundImgPath, Screen):
        # Displaying Menu
        self.image = pygame.image.load(MenuBackgroundImgPath).convert_alpha()
        self.rect = self.image.get_rect()
        self.DisplaySurface = Screen
        self.DisplayingMenu = False

        # Buttons
        self.Buttons = pygame.sprite.Group()

        # Timer
        self.DisableTimer = False

            
    def CreateButtons(self, Buttons, MenuOffset):
        # Set Offset
        self.MenuOffset = MenuOffset

        # Create buttons
        for ButtonNum in range(len(Buttons)):
            ButtonName = Buttons[ButtonNum][0]
            FullPath = "MenuItems/" + str(ButtonName) + ".png"
            ButtonImage = pygame.image.load(FullPath).convert_alpha()
            button = Button(ButtonName, Buttons[ButtonNum][1], Buttons[ButtonNum][2], ButtonImage)
            self.Buttons.add(button)

        # Add offset to buttons
        for button in self.Buttons:
            button.rect.x += MenuOffset[0]
            button.rect.y += MenuOffset[1]

    def update(self):
        self.DisplaySurface.blit(self.image, self.MenuOffset)
        
        # Update each button
        for button in self.Buttons:
            button.update()

            # Check if timer has been disabled
            if button.Name == 'Timer':
                if button.On == False:
                    self.DisableTimer = True
                else:
                    self.DisableTimer = False



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

        # Check if the mouse is colliding with the button, and if they clicked
        if self.rect.collidepoint(MousePos):
            if pygame.mouse.get_pressed()[0] == 1 and self.Clicked == False:
                # Play click sound for anything other the vol up and down buttons (as the user will typically press these multiple times within a short interval)
                if self.Name != 'ArrowDown' and self.Name != 'ArrowUp':
                    PlayClickSound()

                # Get volume and recorded volume
                global Volume
                global RecordedVolume

                # Set each button the attribute 'clicked'
                self.Clicked = True
                
                # Button has been clicked
                if self.Name == 'ArrowDown' and Volume >= 0.1 and Volume != -1:
                    # Turn music down by 0.1
                    Volume -= 0.1
                    RecordedVolume = Volume

                elif self.Name == 'ArrowUp' and Volume <= 0.9 and Volume != -1:
                    # Turn music up by 0.1
                    Volume += 0.1
                    RecordedVolume = Volume
                    
                elif self.Name == 'Volume':
                    # Mute music
                    if self.On:
                        self.image = pygame.image.load("MenuItems/VolumeOff.png").convert_alpha()
                        self.On = False
                        Volume = -1
                    # Unute music
                    else:
                        self.image = pygame.image.load("MenuItems/Volume.png").convert_alpha()
                        self.On = True
                        Volume = RecordedVolume

                elif self.Name == 'Timer':
                    # Hide timer
                    if self.On:
                        self.image = pygame.image.load("MenuItems/TimerOff.png").convert_alpha()
                        self.On = False

                    # Display timer
                    else:
                        self.image = pygame.image.load("MenuItems/Timer.png").convert_alpha()
                        self.On = True

                elif self.Name == 'Return':
                    # Return to level menu
                    print()

                elif self.Name == 'Exit':
                    # Close program
                    sys.exit()

                # Ensure the volume is a float to 1 d.p
                Volume = round(Volume, 1)
                # Check if volume has been set to off
                if Volume == -1:
                    mixer.music.set_volume(0)
                    mixer.music.Channel(1).set_volume(0)
                # Otherwise set volume to new volume
                else:
                    mixer.music.set_volume(Volume)

        # To check if the user has stopped clicking
        if pygame.mouse.get_pressed()[0] == 0:
            self.Clicked = False
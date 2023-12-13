#----------------------#
#--Importing libraris--#           ¤\label{line:sp}¤
#----------------------#
import pygame
from random import uniform
from numpy import argmax
from time import time
from time import sleep
import main


#----------------------#
#--Creating new rooms--#
#----------------------#

# RP's X and Y location on the screen
RP_locs = [[[140,90],[140,140]],
           [[200,90],[200,140]],
           [[260,90],[260,140]],
           [[20,195]],
           [[140,195]],
           [[280,195]]]

# The name of the room
RP_names = ["C2-203","C2-205","C2-207","G222-1","G222-2","G222-3"]

# The required outputs from main to the rooms
RP_inputs = [[1,2],[8,9],[6,7],[5],[3],[4]]


#--------------------#
#--Creating classes--#
#--------------------#

# Text label class
class label:
    def __init__(self, text:str, text_color:str="Black", background_color:str="Grey") -> None:
        """
        __init_(self, text:str, text_color:str="Black", background_color:str="Grey")
         | 
         | Pygames text box with background and colors
         | 
         | Parameters
         | ----------
         | text: A string that is will be the text in the text box
         | 
         | text_color: A string depicting what color the text will be.
         |      By defult is set to "Black"
         | 
         | background_color: A string depicting what color the background behind the text will be.
         |      By defult is set to "Grey"
         | 
        """
        
        # Giving the object it's parameters
        self.text = text
        self.text_color = text_color
        self.background_color = background_color

        # setting up the text box with pygames
        self.item = font.render(self.text, True, self.text_color, self.background_color)
        self.item_rect = self.item.get_rect()
        self.item_center = [self.item_rect.width//2,self.item_rect.height//2]
        
        # Updating to show the text on the screen
        self.update()
    
    def update(self) -> None:
        """
        update(self)
         | 
         | Update the postion of the label on the screen
         | 
         | Parameters
         | ----------
         | None
         | 
        """
        
        # Setting the labels center
        self.item_rect.center = self.item_center
    
    def loc(self, xloc:int, yloc:int) -> None:
        """
        loc(self, xloc:int, yloc:int)
         | 
         | Setting the x and y location for the label on the screen
         | 
         | Parameters
         | ----------
         | xloc: An int depicting the x location for the label
         | 
         | yloc: An int depicting the y location for the label
         | 
        """

        # setting item_center to the xloc and yloc
        self.item_center = [xloc+self.item_rect.width//2,yloc-self.item_rect.height//2]
        
        # updating the position
        self.update()
    
    def content(self, string:str) -> None:
        """
        content(self, string:str)
         | 
         | Setting the content of the label to a new string
         | 
         | Parameters
         | ----------
         | string: A string with the new text
         | 
        """

        # updating self.text and self.item to containt the new text string
        self.text = string
        self.item = font.render(self.text, True, self.text_color, self.background_color)

# Rooms class
class room:
    def __init__(self, RP_loc:list, RP_size:int, RP_name:str, RP_inputs:list) -> None:
        """
        __init__(self, RP_loc:list, RP_size:int, RP_name:str, RP_inputs:list)
         | 
         | A room with RP's and a name
         | 
         | Parameters
         | ----------
         | RP_loc: A list with the RP's that are in a room
         | 
         | RP_size: An int with the size of the RP's on the screen
         | 
         | RP_name: A string with the name of the room
         | 
         | RP_inputs: A list with what outputs from the main library that connect to the room
         | 
        """

        # Giving the object it's parameters
        self.RP_loc = RP_loc
        self.RP_size = RP_size
        self.RP_name = RP_name
        self.RP_inputs = RP_inputs
    
    def inside(self, point:list, edge:int) -> bool:
        """
        inside(self, point:list, edge:int)
         | 
         | Checks of a point is withing one of the RP's location on the screen
         | 
         | Parameters
         | ----------
         | point: A list with the x and y location that are being compared to the location of the RP's
         | 
         | edge: An int depicting how much give there should be on the RP's
         | 
        """

        # Looping the RP's of the room
        for value in self.RP_loc:
            # Cheks if the pint is in the RP area
            if within(value,[self.RP_size+edge]*2,point):
                return True
        return False


# Resseting the devices in rooms and ignore list to only contain zeros
devicesInRoom = [0]*len(RP_names)
ignoreList = [0]*len(RP_names)

# Setting evacuation mode to False
evacuateMode = False


# pygame setup
pygame.init()
width,height = 535,535 # Screen size
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
running = True

font = pygame.font.Font('freesansbold.ttf', 16) # text font

# Setting up the background
bg_img = pygame.image.load('Map-AAU.png')
bg_img = pygame.transform.scale(bg_img,(width,height))


# colors for the RP's
color1 = [254,27,27]
color2 = [220,200,62]
color3 = [60,221,75]

# RP size
crossSize = 7

# initializing all the room
rooms = [room(RP_loc,crossSize, RP_names[index], RP_inputs[index]) for index, RP_loc in enumerate(RP_locs)]

#-------------------------------------------#
#--Definging all the labels for the screen--#
#-------------------------------------------#
header = label("Devices in room X: XX")
header.loc(width//2-header.item_rect.width//2,32)

evacuate_button = label("Evacuate Mode")
evacuate_button.loc(0,height-evacuate_button.item_rect.height//2)

most_label = label("Most deices in room: ")
most_label.loc(0,height-evacuate_button.item_rect.height-most_label.item_rect.height//2)

ignore_button = label("Ignore")
ignore_button.loc(0,height-evacuate_button.item_rect.height-most_label.item_rect.height-ignore_button.item_rect.height//2)




def drawCross(loc:list, size:int, color) -> None:
    """
    drawCross(loc:list, size:int, color:str)
     | 
     | draws a cross on the screen
     | 
     | Parameters
     | ----------
     | loc: A list with the x and y location for the center of the cross
     | 
     | size: An int with the width of the cross
     | 
     | color: A string or list with the RGB colors of the cross
     |
    """

    # Drawing the 2 lines for the cross
    pygame.draw.line(screen, color, [loc[0]-size, loc[1]-size], [loc[0]+size, loc[1]+size], 2)
    pygame.draw.line(screen, color, [loc[0]+size, loc[1]-size], [loc[0]-size, loc[1]+size], 2)

def within(itemloc:list, size:list, mouseloc:list) -> bool:
    """
    within(itemloc:list, size:list, mouseloc:list)
     | 
     | returns a bool based on if the mouseloc is in the item
     |
     | Parameters
     | ----------
     | itemloc: A list with the x and y location of the center of the item
     | 
     | size: A list of the width and height of the item
     |
     | mouseloc: A list with the x and y location of the mouse
     |
    """

    # cheking the mouselocation bassed on the item
    return itemloc[0]-size[0]//2 < mouseloc[0] < itemloc[0]+size[0]//2 and itemloc[1]-size[1]//2 < mouseloc[1] < itemloc[1]+size[1]//2

def evacuate():
    """
    evacuate()
     | 
     | Runs the evacuation procedure by showing the labels for the room
     |      and returns the rooms and background size
     |
    """

    # sets up all the labels for showing how many devices are in each room
    rooms = [font.render(f'{devicesInRoom[index]}', True, "Black", "Grey") for index in range(4)]
    roomRects = [rooms[index].get_rect() for index in range(4)]
    roomCenters = [[140,115],[200,115],[260,115],[200,207]]
    for index in range(4):
        roomRects[index].center = roomCenters[index]

    return rooms, roomRects

def getRP() -> int:
    """
    grtRP()
     |
     | returns the room the device is in from the main library as an int
     | 
    """
    sleep(0.5)
    _, _, winner = main.checkBestMatch()
    return winner

def checkMost(room:int) -> list:
    """
    checkMost(room)
     |
     | returns a color based on if the room have the most amount of devices
     |
     | Parameters
     | ----------
     | room: An int depicting what room is beeing cheked
     |
    """
    
    if argmax(devicesInRoom) == room: #True if the index of the higest value is the samme as the room
        return color1
    else:
        return color3

def ignore(list:list, index:int) -> list:
    """
    ignore(list:list, index:int)
     |
     | returns a list of the updated ignore list
     |
     | Parameters
     | ----------
     | list: A list with the ignore values
     |
     | index: An int with the index of what room should be added to the ignore list
     |
    """
    list[index] = 1
    return list

#-----------------#
#--The main loop--#
#-----------------#
runing = True
while runing:

    # Showing the things on the screen that should always be there
    screen.blits([
        [bg_img,(0,0)],
        [header.item, header.item_rect],
        [evacuate_button.item,evacuate_button.item_rect]
    ])

    #--------------#
    #--Evacuation--#
    #--------------#
    if evacuateMode:
        rp = getRP() # Getting the RP

        # loop all the rooms and cheking if the device is in the room
        for index, value in enumerate(rooms):
            if rp in value.RP_inputs:
                devicesInRoom = [0] * len(rooms)
                devicesInRoom[index] = 1

        room_, rect = evacuate() # Updating the labes for the rooms

        # Showing the amount of devices of each room on the screen
        screen.blits([
        [room_[0],rect[0]],
        [room_[1],rect[1]],
        [room_[2],rect[2]],
        [room_[3],rect[3]],
        [most_label.item,most_label.item_rect], # The label with the most devices
        [ignore_button.item,ignore_button.item_rect] # The ignore button
        ])

    #-----------------#
    #--Pygame events--#
    #-----------------#
    for event in pygame.event.get():
        # Closing the game
        if event.type == pygame.QUIT:
            runing = False
        
        # Clicking on the screen
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_Loc = pygame.mouse.get_pos()

            # Checks if clicking the evacuate button
            if within(evacuate_button.item_center, [evacuate_button.item_rect.width,evacuate_button.item_rect.height], mouse_Loc):
                if evacuateMode:
                    ignoreList = [0]*4
                evacuateMode = not evacuateMode

            # Checks if clicking the ignore button
            elif within(ignore_button.item_center, [ignore_button.item_rect.width,ignore_button.item_rect.height], mouse_Loc):
                ignoreList = ignore(ignoreList, argmax(devicesInRoom))
                most_label.content("Most devices in room: None")
        
        # Moving the mouse
        elif event.type == pygame.MOUSEMOTION:
            mouse_Loc = pygame.mouse.get_pos()

            # checks if hovering over a RP
            for index, values in enumerate(rooms):
                if values.inside(mouse_Loc,4):
                    header.content(f'Devices in room {values.RP_name}: {devicesInRoom[index]}')
            
    #-----------------------------------------------------#
    #--Updating the color of RP's and Most devices label--# 
    #-----------------------------------------------------#
    for index, value in enumerate(rooms):
        color = checkMost(index) # Color is color1 or color3
        # If it's the room with most devices and is not on the ignore list
        if color == color1 and not ignoreList[index]:
            most_label.content(f"Most devices in room: {value.RP_name}")
        # If it's on the ignore list
        elif ignoreList[index]:
            if color == color1:
                most_label.content("Most devices in room: None")
            color = "Grey"
        #Draw the new crosses with the new colors
        for loc in value.RP_loc:
            drawCross(loc, crossSize, color)

    pygame.display.update() # Update the screen
pygame.quit() # Close the program

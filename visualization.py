import pygame
import random
from numpy import argmax
import time

class label:
    def __init__(self, text:str, text_color:str="Black", background_color:str="Grey") -> None:
        self.text = text
        self.text_color = text_color
        self.background_color = background_color

        self.item = font.render(self.text, True, self.text_color, self.background_color)
        self.item_rect = self.item.get_rect()
        self.item_center = [self.item_rect.width//2,self.item_rect.height//2]
        
        self.update()
    
    def update(self) -> None:
        self.item_rect.center = self.item_center
    
    def loc(self, xloc:int, yloc:int) -> None:
        self.item_center = [xloc+self.item_rect.width//2,yloc-self.item_rect.height//2]
        self.update()
    
    def content(self, string:str) -> None:
        self.text = string
        self.item = font.render(self.text, True, self.text_color, self.background_color)
        self.update()



devicesInRoom = [0]*4
ignoreList = [0,0,0,0]

evacuateMode = False

startTime = time.time()

# pygame setup
pygame.init()
width,height = 535,535
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
running = True
dt = 0

font = pygame.font.Font('freesansbold.ttf', 16)

bg_img = pygame.image.load('Self\Code\Python\Random\Map-AAU.png')
bg_img = pygame.transform.scale(bg_img,(width,height))

color1 = [254,27,27]
color2 = [220,200,62]
color3 = [60,221,75]

RP_Loc_room1 = [[140,90],[140,140]]
RP_Loc_room2 = [[200,90],[200,140]]
RP_Loc_room3 = [[260,90],[260,140]]
RP_Loc_G1 = [[140,195],[200,195],[260,195]]

room1_RP = [1,2]
room2_RP = [3,4]
room3_RP = [5,6]
G1_RP = [7,8,9]

crossSize = 7

font = pygame.font.Font('freesansbold.ttf', 16)

header = label("Devices in room X: XX")
header.loc(width//2-header.item_rect.width//2,32)

evacuate_button = label("Evacuate Mode")
evacuate_button.loc(0,height-evacuate_button.item_rect.height//2)

most_label = label("Most deices in room: ")
most_label.loc(0,height-evacuate_button.item_rect.height-most_label.item_rect.height//2)

ignore_button = label("Ignore")
ignore_button.loc(0,height-evacuate_button.item_rect.height-most_label.item_rect.height-ignore_button.item_rect.height//2)




def drawCross(loc, size, color):
    pygame.draw.line(screen, color, [loc[0]-size, loc[1]-size], [loc[0]+size, loc[1]+size], 2)
    pygame.draw.line(screen, color, [loc[0]+size, loc[1]-size], [loc[0]-size, loc[1]+size], 2)

def within(itemloc, size, mouseloc):
    return itemloc[0]-size[0]//2 < mouseloc[0] < itemloc[0]+size[0]//2 and itemloc[1]-size[1]//2 < mouseloc[1] < itemloc[1]+size[1]//2

def evacuate():
    rooms = [font.render(f'{devicesInRoom[index]}', True, "Black", "Grey") for index in range(4)]
    roomRects = [rooms[index].get_rect() for index in range(4)]
    roomCenters = [[140,115],[200,115],[260,115],[200,207]]
    for index in range(4):
        roomRects[index].center = roomCenters[index]

    return rooms, roomRects

def getRP():
    global startTime
    if time.time() - startTime >= 1:
        startTime = time.time()
        return int(random.uniform(1,10))

def checkMost(room):
    if argmax(devicesInRoom) == room:
        return color1
    else:
        return color3

def ignore(list, index):
    list[index] = 1
    return list
    
room = [font.render('', True, "Black", "Grey") for _ in range(4)]
rect = [room[index].get_rect() for index in range(4)]
roomCenter = [[200,200] for _ in range(4)]
for index in range(4):
    rect[index].center = (roomCenter[index])


runing = True
while runing:

    screen.blits([
        [bg_img,(0,0)],
        [header.item, header.item_rect],
        [evacuate_button.item,evacuate_button.item_rect]
    ])

    if evacuateMode:
        rp = getRP()
        if rp in room1_RP:
            devicesInRoom = [1,0,0,0]
        if rp in room2_RP:
            devicesInRoom = [0,1,0,0]
        if rp in room3_RP:
            devicesInRoom = [0,0,1,0]
        if rp in G1_RP:
            devicesInRoom = [0,0,0,1]
        room, rect = evacuate()
        screen.blits([
        [room[0],rect[0]],
        [room[1],rect[1]],
        [room[2],rect[2]],
        [room[3],rect[3]],
        [most_label.item,most_label.item_rect],
        [ignore_button.item,ignore_button.item_rect]
        ])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_Loc = pygame.mouse.get_pos()
            if within(evacuate_button.item_center, [evacuate_button.item_rect.width,evacuate_button.item_rect.height], mouse_Loc):
                if evacuateMode:
                    ignoreList = [0]*4
                evacuateMode = not evacuateMode

            
            elif within(ignore_button.item_center, [ignore_button.item_rect.width,ignore_button.item_rect.height], mouse_Loc):
                ignoreList = ignore(ignoreList, argmax(devicesInRoom))
                most_label.content("Most devices in room: None")
        

        elif event.type == pygame.MOUSEMOTION:
            mouse_Loc = pygame.mouse.get_pos()
            if within(RP_Loc_room1[0],[crossSize+4] * 2,mouse_Loc) or within(RP_Loc_room1[1],[crossSize+4] * 2,mouse_Loc):
                header.content(f'Devices in room 2-203: {devicesInRoom[0]}')

            elif within(RP_Loc_room2[0],[crossSize+4] * 2,mouse_Loc) or within(RP_Loc_room2[1],[crossSize+4] * 2,mouse_Loc):
                header.content(f'Devices in room 2-205: {devicesInRoom[1]}')

            elif within(RP_Loc_room3[0],[crossSize+4] * 2,mouse_Loc) or within(RP_Loc_room3[1],[crossSize+4] * 2,mouse_Loc):
                header.content(f'Devices in room 2-207: {devicesInRoom[2]}')
                
            elif within(RP_Loc_G1[0],[crossSize+4] * 2,mouse_Loc) or within(RP_Loc_G1[1],[crossSize+4] * 2,mouse_Loc) or within(RP_Loc_G1[2],[crossSize+4] * 2,mouse_Loc):
                header.content(f'Devices in room G222: {devicesInRoom[3]}')
            


    color = checkMost(0)
    if color == color1 and not ignoreList[0]:
        most_label.content("Most devices in room: 2-203")
    elif ignoreList[0]:
        if color == color1:
            most_label.content("Most devices in room: None")
        color = "Grey"
    for loc in RP_Loc_room1:
        drawCross(loc, crossSize, color)
    
    color = checkMost(1)
    if color == color1 and not ignoreList[1]:
        most_label.content("Most devices in room: 2-205")
    elif ignoreList[1]:
        if color == color1:
            most_label.content("Most devices in room: None")
        color = "Grey"
    for loc in RP_Loc_room2:
        drawCross(loc, crossSize, color)

    color = checkMost(2)
    if color == color1 and not ignoreList[2]:
        most_label.content("Most devices in room: 2-207")
    elif ignoreList[2]:
        if color == color1:
            most_label.content("Most devices in room: None")
        color = "Grey"
    for loc in RP_Loc_room3:
        drawCross(loc, crossSize, color)

    color = checkMost(3)
    if color == color1 and not ignoreList[3]:
        most_label.content("Most devices in room: G222")
    elif ignoreList[3]:
        if color == color1:
            most_label.content("Most devices in room: None")
        color = "Grey"
    for loc in RP_Loc_G1:
        drawCross(loc, crossSize, color)


    pygame.display.update()
pygame.quit()

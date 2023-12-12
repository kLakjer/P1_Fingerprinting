import pygame
from random import uniform
from numpy import argmax
from time import time

RP_locs = [[[140,90],[140,140]],
           [[200,90],[200,140]],
           [[260,90],[260,140]],
           [[140,195],[200,195],[260,195]]]

RP_names = ["C2-203","C2-205","C2-207","G222"]

RP_inputs = [[1,2],[3,4],[5,6],[7,8,9]]



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

class room:
    def __init__(self, RP_loc, RP_size, RP_name, RP_inputs) -> None:
        self.RP_loc = RP_loc
        self.RP_size = RP_size
        self.RP_name = RP_name
        self.RP_inputs = RP_inputs
    
    def inside(self, point, edge):
        for value in self.RP_loc:
            if within(value,[self.RP_size+edge]*2,point):
                return True
        return False



devicesInRoom = [0]*len(RP_names)
ignoreList = [0]*len(RP_names)

evacuateMode = False

startTime = time()

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


crossSize = 7


rooms = [room(RP_loc,crossSize, RP_names[index], RP_inputs[index]) for index, RP_loc in enumerate(RP_locs)]

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
    if time() - startTime >= 1:
        startTime = time()
        return int(uniform(1,10))

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
        for index, value in enumerate(rooms):
            if rp in value.RP_inputs:
                devicesInRoom = [0] * len(rooms)
                devicesInRoom[index] = 1

        room_, rect = evacuate()
        screen.blits([
        [room_[0],rect[0]],
        [room_[1],rect[1]],
        [room_[2],rect[2]],
        [room_[3],rect[3]],
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

            for index, values in enumerate(rooms):
                if values.inside(mouse_Loc,4):
                    header.content(f'Devices in room {values.RP_name}: {devicesInRoom[index]}')
            

    for index, value in enumerate(rooms):
        color = checkMost(index)
        if color == color1 and not ignoreList[index]:
            most_label.content(f"Most devices in room: {value.RP_name}")
        elif ignoreList[index]:
            if color == color1:
                most_label.content("Most devices in room: None")
            color = "Grey"
        for loc in value.RP_loc:
            drawCross(loc, crossSize, color)

    pygame.display.update()
pygame.quit()

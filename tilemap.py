import pygame as pg
from variables import *

def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

class Map:
    def __init__(self, filename):
        self.data = []
        #opens whatever file has the name passed into the function and calls it f
        with open(filename, "rt") as f:
            #loops through each line in the file and adds it to the data list
            for line in f:
                self.data.append(line)

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

class Camera:
    def __init__(self, width, height):
        #th epurpose of the camrea is to keep track of which section of the
        #map should be drawn on the screen
        self.camera = pg.Rect(0,0, width, height)
        self.width = width
        self.height = height
        
    def apply(self, entity):
        #the move command moves the rect by the cmaera coords
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        #adds half the screensize so the the player remians central
        x = -target.rect.centerx + int(WIDTH/2)
        y = -target.rect.centery + int(HEIGHT/2)
        #limits the scrolling to the size of the map
        #make sure x is never bigeer than 0.
        x = min(0,x) #left side
        y = min(0,y) #top side
        x = max(-(self.width - WIDTH),x)#right
        y = max(-(self.height - HEIGHT),y)#bottom
        
        #updates the camera
        self.camera = pg.Rect(x,y, self.width, self.height)
    
 

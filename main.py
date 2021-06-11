import pygame as pg
from variables import *
from sprites import *
import sys
#allows us to find where the imported files are located
from os import path
from tilemap import *

class Game:
    def __init__(self):
        #initialises pg
        pg.init()
        #allows you to include sound
        pg.mixer.init()
        #create the window
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        #create caption
        pg.display.set_caption(TITLE)
        #clock
        self.clock = pg.time.Clock()
        #makes it so if you hold down a key for 500 milliseconds you dont
        #have to keep pressing that key over and over for that movement to
        # repeat
        pg.key.set_repeat(500,100)
        self.load_data()

    def load_data(self):
        #game_folder is where the map.txt file is
        game_folder = path.dirname(__file__)
        #folder where all the images for the game are stored
        img_folder = path.join(game_folder, "Img")
        #the location of "map.txt" is found and self.map becomes the outcome
        #if the Map class which is in the tilemap file
        self.map = Map(path.join(game_folder, "map2.txt"))
        #player images
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMAGE)).convert_alpha()
        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE))
        
        
                

#GROUPS
    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        #spawns the walls
        #enumerate gives the index and the data stored at that index.
        #this section gives the value as tile, the column as an index and the row as an index
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                #basically if there is a 1 on the map text file then a wall is spawned
                if tile == "1":
                    Wall(self, col, row)
                if tile == "M":
                    Mob(self, col, row)
                if tile == "P":
                    self.player = Player(self, col, row)
        #tells the camera how big the total player area is
        self.camera= Camera(self.map.width, self.map.height)

#GAME LOOP
    def run(self):
        self.running = True
        while self.running:
            #keeps the loop running at the right speed
            self.dt = self.clock.tick(FPS)/1000
            #runs the events, update and draw functions
            self.events()
            self.update()
            self.draw()
    def quit(self):
        #pygame is quit and the window is closed
        pg.quit()
        sys.exit()
    
    #EVENTS
    def events(self):
        for event in pg.event.get():
            #check if the window should be closed
            #if the x button is pressed the quit function is activated
            if event.type == pg.QUIT:
                self.quit()


    #START SCREEN
    def start_screen(self):
        pass

    #END SCREEN
    def end_screen(self):
        pass

    #SETTINGS SCREEN
    def settings_screen(self):
        pass

    #TUTORIAL SCREEN
    def tutorial_screen(self):
        pass

    

    #UPDATE
    def update(self):
        self.all_sprites.update()
        #tells the camera update function that the entity it is following is the player
        self.camera.update(self.player)
        
    
    
    #DRAW
    #draws a grid on the screen
    def draw_grid(self):
        #draws the vertical llines of a grid
        for x in range(0,WIDTH, TILESIZE):
            pg.draw.line(self.screen, BLUE, (x,0), (x,HEIGHT))
        #draws the vertical lines of a grid
        for y in range(0,HEIGHT, TILESIZE):
            pg.draw.line(self.screen, BLUE, (0,y), (WIDTH, y))
    def draw(self):
        self.screen.fill(BG_COLOUR)
        #calls draw grip method
        self.draw_grid()
        #draws all the sprites on the screen which are in the all_sprites group
        
        for sprite in self.all_sprites:
            #takes the camera and applys it to all the sprites
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        #flips the screen to show what youve drawn on the screen
        #always goes last in the draw section
        
        pg.display.flip()

#create the game object which allows the code to actually be run
g = Game()
g.start_screen()
while True:
    g.new()
    g.run()



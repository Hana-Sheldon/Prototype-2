import pygame as pg
from variables import *
from tilemap import collide_hit_rect
vec = pg.math.Vector2
def collide_with_walls(sprite,group, dir):
    #if the direction of the player is along the x axis 
    if dir == "x":
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        #then the code checks if the player sprite is hitting any wall sprites
        if hits:
            #if it is hitting any wall sprites ti checks if the player is moving in the x direction
            if sprite.vel.x >0:
                #if it is then the x becomes the coordinate of the thing its hitting minus the width of the player
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width/2 #/2 so that we are using the center
            if sprite.vel.x<0:
                #if its not then the x becomes the coordinates of the right corner
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width/2
            #x displacememnt becomes 0
            sprite.vel.x = 0
            #the rect x coordinate becomes sprite.x
            sprite.hit_rect.centerx= sprite.pos.x
    #if the direction of the player is along the y axis
    if dir == "y":
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        #then the code checks if the player sprite is hitting any wall sprites
        if hits:
            #if it is hitting any wall sprites ti checks if the player is moving in the y direction
            if sprite.vel.y >0:
                #if it is then the y becomes the coordinate of the thing its hitting minus the height of the player
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height/2
            if sprite.vel.y<0:
                #if its not then the y becomes the coordinates of the bottom
                sprite.pos.y = hits[0].rect.bottom +sprite.hit_rect.height/2
            sprite.vel.y = 0
            #y displacememnt becomes 0
            sprite.hit_rect.centery= sprite.pos.y
            #the rect y coordinate becomes self.y


class Player(pg.sprite.Sprite):
    #player sprite
    def __init__(self, game, x,y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img       
        #the rectangle that encloses the sprite
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        #vectors
        self.vel = vec(0,0)
        self.pos = vec(x,y) *TILESIZE
        #0 degrees means the player will be pointing directly to the right
        self.rot = 0


    def get_keys(self):
        self.rot_speed = 0
        #the velocity of the sprite is the vector (0,0)
        self.vel = vec(0,0)
        keys =pg.key.get_pressed()
        #when the left arrow or the A key is pressed the player rotates to the left
        if keys[pg.K_LEFT] or keys [pg.K_a]:
            self.rot_speed = PLAYER_ROT_SPEED
        #when the right arrow key or D is pressed the player rotates to the right
        if keys[pg.K_RIGHT] or keys [pg.K_d]:
            self.rot_speed = -PLAYER_ROT_SPEED
        #moves the player forwards
        if keys[pg.K_UP] or keys [pg.K_w]:
            #the vec prodecure does trigonometry so that the code is simpler for us
            self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
        #moves the player backwards at half speed.
        if keys[pg.K_DOWN] or keys [pg.K_s]:
            self.vel = vec(-PLAYER_SPEED/2, 0).rotate(-self.rot)



    def update(self):
        self.get_keys()
        #the rotation is the rotation plus (the speed multiplied by the
        #game time step). this value is then divided by 360 and the remainder is obtained.
        self.rot = (self.rot +self.rot_speed * self.game.dt)%360
        #position attribute becomes position + the velocity multiplied
        #by the gmae time step
        #rotates the player sprite
        self.image = pg.transform.rotate(self.game.player_img, self.rot)
        #update the player rect
        self.rect = self.image.get_rect()
        self.pos += self.vel * self.game.dt
        
        
        #sets the centre of the rectangle to the position of the player sprite
        self.rect.center = self.pos
        #sets the rect to the x and y coordinates
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls,"x")
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls,"y")
        self.rect.center = self.hit_rect.center
        
class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        #make it a member of the sprites group and the mobs group
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob_img
        self.rect = self.image.get_rect()
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x,y) * TILESIZE
        self.rect.center = self.pos
        self.rot =0
        self.vel= vec(0,0)
        self.acc = vec(0,0)
        
    def update(self):
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1,0))
        self.image = pg.transform.rotate(self.game.mob_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        #acceleration to be the vector of the mob speed but rotated
        #in the negative direction of the rot value 
        self.acc = vec(MOB_SPEED,0).rotate(-self.rot)
        #then add vel multiplied by -1 so that there is a max speed
        self.acc += self.vel*-1
        #vel = vel+ (acc * game time step)
        self.vel += self.acc * self.game.dt
        #uses s=ut + 1/2at^2
        self.pos += self.vel* self.game.dt + 0.5* self.acc * self.game.dt **2
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, "x")
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, "y")
        self.rect.center = self.hit_rect.center
        


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        #make it a member of the sprites group and the walls group
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        #makes the actual walls
        self.image = game.wall_img

        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        

#Asteroids 1.3
#Zachary Page

#imports
from superwires import games
import random
import math

#global info
games.init(screen_width = 640, screen_height=480 , fps = 60)



#classes
class Asteroid(games.Sprite):
    small = 1
    medium = 2
    large = 3
    images = {small : games.load_image("images2/asteroid3.png"),
              medium : games.load_image("images2/asteroid2.png"),
              large : games.load_image("images2/asteroid1.png")}
    speed = 2
    spawn = 2

    def __init__(self, x , y, size):
        super(Asteroid, self).__init__(image = Asteroid.images[size],
                                       x = x,
                                       y = y,
                                       dx = random.choice([1, -1]) * Asteroid.speed * random.random()/size,
                                       dy = random.choice([-1, 1]) * Asteroid.speed * random.random()/size)
        self.size = size
    def update(self):
        if self.left>games.screen.width:
            self.right = 0
        if self.right<0:
            self.left=games.screen.width
        if self.top > games.screen.height:
            self.bottom = 0

        if self.bottom < 0:
            self.top = games.screen.height

        if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                sprite.die()
            self.die()

    def die(self):
        #if asteroid isn't small, replace with two smaller asteroids
        if self.size != Asteroid.small:
            for i in range(Asteroid.spawn):
                new_asteroid = Asteroid(x = self.x,
                                        y = self.y,
                                        size = self.size - 1)
                games.screen.add(new_asteroid)
        self.destroy()


class Ship(games.Sprite):
    ship_image = games.load_image("images2/ship3.png")
    sound = games.load_sound("sounds/thruster.wav")
    rotation_step = 7
    velocity_step = .03
    missile_delay = 25

    def __init__(self):
        super(Ship, self).__init__(image=Ship.ship_image,
                                   x=games.screen.width / 2,
                                   y=games.screen.height / 2)
        self.missile_wait = 0

    def update(self):
        if games.keyboard.is_pressed(games.K_LEFT) or games.keyboard.is_pressed(games.K_a):
            self.angle -= Ship.rotation_step
        if games.keyboard.is_pressed(games.K_RIGHT) or games.keyboard.is_pressed(games.K_d):
            self.angle += Ship.rotation_step

        if games.keyboard.is_pressed(games.K_UP) or games.keyboard.is_pressed(games.K_w):
            Ship.sound.play()
            angle = self.angle * math.pi/180
            self.dx += Ship.velocity_step * math.sin(angle)
            self.dy += Ship.velocity_step * -math.cos(angle)

        if self.missile_wait > 0:
            self.missile_wait -= 1

        if games.keyboard.is_pressed(games.K_SPACE) and self.missile_wait == 0:
            new_missile = Missile(self.x, self.y, self.angle)
            games.screen.add(new_missile)
            self.missile_wait = Ship.missile_delay




##        #this is copied code to look into better ways of doing it
        if self.left>games.screen.width:
            self.right = 0
        if self.right<0:
            self.left=games.screen.width
        if self.top > games.screen.height:
            self.bottom = 0

        if self.bottom < 0:
            self.top = games.screen.height

        if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                sprite.die()
            self.die()

    def die(self):
        self.destroy()
class Missile(games.Sprite):
    image = games.load_image("images2/laser.png")
    sound = games.load_sound("sounds/laser.wav")
    buffer = 45
    velocity_factor = 7
    lifetime = 40
    def __init__(self, ship_x, ship_y, ship_angle):
        Missile.sound.play()
        angle = ship_angle * math.pi/180

        #calculate missile's starting position
        buffer_x = Missile.buffer * math.sin(angle)
        buffer_y = Missile.buffer * -math.cos(angle)

        x = ship_x + buffer_x
        y = ship_y + buffer_y

        dx = Missile.velocity_factor * math.sin(angle)
        dy = Missile.velocity_factor * -math.cos(angle)
        super(Missile, self).__init__(image = Missile.image,
                                      x = x,
                                      y = y,
                                      dx = dx,
                                      dy = dy)
        self.lifetime  = Missile.lifetime
        self.angle = ship_angle

    def update(self):
        if self.left > games.screen.width:
            self.right = 0
        if self.right < 0:
            self.left = games.screen.width
        if self.top > games.screen.height:
            self.bottom = 0
        if self.bottom < 0:
            self.top = games.screen.height

        self.lifetime -= 1
        if self.lifetime == 0:
            self.destroy()

        #check if missile overlaps any other object
        if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                sprite.die()
            self.die()

    def die(self):
        self.destroy()


#main
def main():

    #load data
    bg_img = games.load_image("images2/Space.jpg")

    #Create objects
    for i in range(8):
        x = random.randrange(games.screen.width)
        y = random.randrange(games.screen.height)
        size = random.choice([Asteroid.small, Asteroid.medium, Asteroid.large])
        new_asteroid = Asteroid(x = x, y = y, size = size)
        games.screen.add(new_asteroid)
    #create ship
    player = Ship()
    #shot = Missile(100,100,0)



    #draw objects
    games.screen.background = bg_img
    games.screen.add(player)
    #games.screen.add(shot)

    #game setup


    #start mainloop
    games.screen.mainloop()

main()




















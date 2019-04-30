#Asteroids 1.0
#Zachary Page

#imports
from superwires import games
import random

#global info
games.init(screen_width = 640, screen_height= 480, fps = 60)





#classes
class Asteroid(games.Sprite):
    small = 1
    medium = 2
    large = 3
    images = {small : games.load_image("images2/asteroid3.png"),
              medium : games.load_image("images2/asteroid2.png"),
              large : games.load_image("images2/asteroid1.png")}
    speed = 2

    def __init__(self, x , y, size):
        super(Asteroid, self).__init__(image = Asteroid.images[size],
                                       x = x,
                                       y = y,
                                       dx = random.choice([1, -1]) * Asteroid.speed * random.random()/size,
                                       dy = random.choice([-1, 1]) * Asteroid.speed * random.random()/size)
        self.size = size
    def update(self):
        if self.left < games.screen.width:
            self.right = 0

        if self.right < 0:
            self.left = games.screen.width

        if self.top > games.screen.height:
            self.bottom = 0

        if self.bottom < 0:
            self.top = games.screen.height

class Ship(games.Sprite):
    ship_image = games.load_image("images2/ship3.png")
    rotation_step = 3

    def __init__(self):
        super(Ship, self).__init__(image=Ship.ship_image,
                                   x=games.screen.width / 2,
                                   y=games.screen.height / 2)


    def update(self):
        if games.keyboard.is_pressed(games.K_LEFT) or games.keyboard.is_pressed(games.K_a):
            self.angle -= Ship.rotation_step
        if games.keyboard.is_pressed(games.K_RIGHT) or games.keyboard.is_pressed(games.K_d):
            self.angle += Ship.rotation_step


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



    #draw objects
    games.screen.background = bg_img
    games.screen.add(player)


    #game setup


    #start mainloop
    games.screen.mainloop()

main()




















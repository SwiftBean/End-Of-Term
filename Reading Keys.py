#Read Key
#Demonstrates reading the keyboard


from superwires import games

games.init(screen_width= 640, screen_height= 480, fps = 50)

class Ship(games.Sprite):
    ship_image = games.load_image("images2/ship3.png")

    def __init__(self):
        super(Ship,self).__init__(image = Ship.ship_image,
                                  x = games.screen.width/2,
                                  y = games.screen.height/2)
    def update(self):
        if games.keyboard.is_pressed(games.K_w) or games.keyboard.is_pressed(games.K_UP):
            self.y-= 1
        if games.keyboard.is_pressed(games.K_s) or games.keyboard.is_pressed(games.K_DOWN):
            self.y+=1
        if games.keyboard.is_pressed(games.K_a) or games.keyboard.is_pressed(games.K_LEFT):
            self.angle-=1
        if games.keyboard.is_pressed(games.K_d) or games.keyboard.is_pressed(games.K_RIGHT):
            self.angle+=1
        if games.keyboard.is_pressed(games.K_1):
            self.angle = 0
        if games.keyboard.is_pressed(games.K_2):
            self.angle = 90
        if games.keyboard.is_pressed(games.K_3):
            self.angle = 180
        if games.keyboard.is_pressed(games.K_4):
            self.angle = 270


def main():

    #load data
    nebula_image = games.load_image("images2/Space.jpg", transparent= False)
    explosion_files = ["images2/e1.jpg",
                       "images2/e2.jpg",
                       "images2/e3.jpg",
                       "images2/e4.jpg",
                       "images2/e5.jpg",
                       "images2/e6.jpg",
                       "images2/e7.jpg",
                       "images2/e8.jpg"]


    #create objects
    the_ship = Ship()
    explosion = games.Animation(images= explosion_files,
                                x = games.screen.width/2,
                                y = games.screen.width/2,
                                n_repeats = 0,
                                repeat_interval = 5)

    #draw objects
    games.screen.background = nebula_image
    games.screen.add(the_ship)
    games.screen.add(explosion)

    #games setup

    #start loop
    games.screen.mainloop()

main()

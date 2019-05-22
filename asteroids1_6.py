#Asteroids 1.6
#Zachary Page

#imports
from superwires import games, color
import random
import math

#global info
games.init(screen_width = 640, screen_height=480 , fps = 50)



#classes
class Game(object):
    def __init__(self):
        #set level
        self.level = 0
        #load sound for level advance
        self.sound = games.load_sound("sounds/level.wav")
        #create score
        self.score = games.Text(value= 0,
                   size = 30,
                   color = color.white,
                   top = 5,
                   right = games.screen.width - 10,
                   is_collideable = False)
        games.screen.add(self.score)

        self.ship = Ship(game = self,
                           x = games.screen.width/2,
                           y = games.screen.height/2)
        games.screen.add(self.ship)

        message1 = games.Message(value = "Use WSD or Up, Left, and Right arrows to move",
                                 size = 35,
                                 color = color.white,
                                 x = games.screen.width/2,
                                 y = games.screen.height/2,
                                 lifetime = 3 * games.screen.fps,
                                 is_collideable = False)

        message2 = games.Message(value = "Press the space bar to fire your laser",
                                 size = 34,
                                 color = color.white,
                                 x = games.screen.width/2,
                                 y = games.screen.height/4,
                                 lifetime = 3 * games.screen.fps,
                                 is_collideable = False)

        games.screen.add(message1)
        games.screen.add(message2)




    def play(self):
        games.music.load("sounds/main_song.wav")
        games.music.play(-1)

        bg_img = games.load_image("images2/Space.jpg")
        games.screen.background = bg_img

        self.advance()

        games.screen.mainloop()


    def advance(self):
        self.level += 1
        #amount of space around ship to preserve when creating asteroids
        buffer = 150
        #create objects
        for i in range(self.level):
            #calculate an x and y at least buffer
            #choose minimum distance along x-axis and y-axis
            x_min = random.randrange(buffer)
            y_min = buffer - x_min
            #choose distance along x-axis and y-axis based on minimum distance
            x_distance = random.randrange(x_min, games.screen.width - x_min)
            y_distance = random.randrange(y_min, games.screen.height - y_min)
            #calculate location based on distance
            x = self.ship.x + x_distance
            y = self.ship.y + y_distance
            #wrap around screen, if necessary
            x %= games.screen.width
            y %= games.screen.height

            #size = random.choice(Asteroid.small, Asteroid.medium, Asteroid.large)

            new_asteroid = Asteroid(game = self, x=x, y=y, size= Asteroid.large)
            games.screen.add(new_asteroid)
            #display level number
        level_message = games.Message(value = "Level" + str(self.level),
                                      size = 40,
                                      color = color.yellow,
                                      x = games.screen.width/2,
                                      y = games.screen.height/10,
                                      lifetime = 3 * games.screen.fps,
                                      is_collideable = False)
        games.screen.add(level_message)

        #play new level sound (except at first level)
        if self.level > 1:
            self.sound.play()

    def end(self):
        """End the game."""
        #show 'Game Over
        end_message = games.Message(value= "Game Over",
                                    size= 90,
                                    color = color.red,
                                    x = games.screen.width/2,
                                    y = games.screen.height/2,
                                    is_collideable= False)

        leave_game = games.Message(value = "(Press Esc to exit)",
                                   size = 45,
                                   color = color.white,
                                   x = games.screen.width/2,
                                   y = games.screen.height/1.75,
                                   is_collideable = False)

        games.screen.add(end_message)
        games.screen.add(leave_game)

    def new_ship(self):
        self.ship = Ship(game = self,
                         x = games.screen.width/2,
                         y = games.screen.height/2)
        games.screen.add(self.ship)


class Wrapper(games.Sprite):
    def update(self):
        if self.left > games.screen.width:
            self.right = 0

        if self.right < 0:
            self.left = games.screen.width

        if self.top > games.screen.height:
            self.bottom = 0

        if self.bottom < 0:
            self.top = games.screen.height
    def die(self):
        self.destroy()

class Collider(Wrapper):
    def update(self):
        """Check for overlapping sprites."""
        super(Collider, self).update()

        if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                sprite.die()
            self.die()

    def die(self):
        #create explosion
        new_explosion = Explosion(obj_x = self.x, obj_y = self.y)
        #add to screen
        games.screen.add(new_explosion)
        self.destroy()


class Asteroid(Wrapper):
    small = 1
    medium = 2
    large = 3
    images = {small : games.load_image("images2/asteroid3.png"),
              medium : games.load_image("images2/asteroid2.png"),
              large : games.load_image("images2/asteroid1.png")}
    speed = 2
    spawn = 2
    points = 30
    total = 0

    def __init__(self, game, x, y, size):
        Asteroid.total += 1
        super(Asteroid, self).__init__(image = Asteroid.images[size],
                                       x = x,
                                       y = y,
                                       dx = random.choice([1, -1]) * Asteroid.speed * random.random()/size,
                                       dy = random.choice([-1, 1]) * Asteroid.speed * random.random()/size)
        self.size = size
        self.game = game

    def die(self):
        #if asteroid isn't small, replace with two smaller asteroids
        Asteroid.total -= 1
        #add to score
        self.game.score.value += int(Asteroid.points / self.size)
        self.game.score.right = games.screen.width - 10


        if self.size != Asteroid.small:
            for i in range(Asteroid.spawn):
                new_asteroid = Asteroid(game = self.game,
                                        x = self.x,
                                        y = self.y,
                                        size = self.size - 1)
                games.screen.add(new_asteroid)
        if Asteroid.total == 0:
            self.game.advance()

        super(Asteroid, self).die()


class Ship(Collider):
    ship_image = games.load_image("images2/ship3.png")
    sound = games.load_sound("sounds/thruster.wav")

    rotation_step = 7
    velocity_step = .03
    missile_delay = 25
    max_velocity = 3
    lives = 3

    def __init__(self,game,x,y):
        super(Ship, self).__init__(image=Ship.ship_image, x = x, y = y)
        self.game = game
        self.missile_wait = 0
        self.lives = games.Text(value="Lives: " + str(Ship.lives), size=25, color=color.white, top=25,
                                right=games.screen.width - 10, is_collideable=False)
        games.screen.add(self.lives)

    def update(self):
        super(Ship,self).update()
        if games.keyboard.is_pressed(games.K_LEFT) or games.keyboard.is_pressed(games.K_a):
            self.angle -= Ship.rotation_step
        if games.keyboard.is_pressed(games.K_RIGHT) or games.keyboard.is_pressed(games.K_d):
            self.angle += Ship.rotation_step

        if games.keyboard.is_pressed(games.K_UP) or games.keyboard.is_pressed(games.K_w):
            Ship.sound.play()
            angle = self.angle * math.pi/180
            self.dx += Ship.velocity_step * math.sin(angle)
            self.dy += Ship.velocity_step * -math.cos(angle)
            self.dx = min(max(self.dx, -Ship.max_velocity), Ship.max_velocity)
            self.dy = min(max(self.dy, -Ship.max_velocity), Ship.max_velocity)

        if self.missile_wait > 0:
            self.missile_wait -= 1

        if games.keyboard.is_pressed(games.K_SPACE) and self.missile_wait == 0:
            new_missile = Missile(self.x, self.y, self.angle)
            games.screen.add(new_missile)
            self.missile_wait = Ship.missile_delay

    def lose_life(self):
        Ship.lives -= 1
        self.lives.destroy()
        if Ship.lives <= 0:
            self.game.end()
        else:
            self.game.new_ship()



    def die(self):
        """Destroy the ship and end the game"""
        super(Ship, self).die()
        self.lose_life()

class Missile(Collider):
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
        super(Missile, self).update()
        self.lifetime -= 1
        if self.lifetime == 0:
            self.destroy()

class Explosion(games.Animation):
    sound = games.load_sound("sounds/explosion.wav")
    exp_images = ["images2/explosion1.bmp",
                       "images2/explosion2.bmp",
                       "images2/explosion3.bmp",
                       "images2/explosion4.bmp",
                       "images2/explosion5.bmp",
                       "images2/explosion6.bmp",
                       "images2/explosion7.bmp",
                       "images2/explosion8.bmp",
                "images2/explosion9.bmp"]
    def __init__(self, obj_x, obj_y):
        super(Explosion, self).__init__(images = Explosion.exp_images,
                                        x = obj_x, y = obj_y,
                                        repeat_interval = 4,
                                        n_repeats = 1,
                                        is_collideable = False)
        Explosion.sound.play()

#main
def main():
    asteroids = Game()
    asteroids.play()

main()
import pygame

class BaseShip:
    def __init__(self):
        self.speed = 3
       


#class EnemyShip(BaseShip):


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)


pygame.init()

width = 700
height = 500

size = (width, height)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Space Invaders")

done = False

clock = pygame.time.Clock()


class EnemyShip(BaseShip):
    def __init__(self):
        self.size_x = 25
        self.size_y = 25
        self.pos_x = width/2
        self.pos_y = 0
        self.x_speed = 5
        self.alive = True
    def Update(self, bullet):
        dead = self.isShot(bullet)
        if self.pos_x < 0:
            self.x_speed = self.x_speed * -1
            self.pos_x = 0
        if self.pos_x > (width - self.size_x):
            self.x_speed = self.x_speed * -1
            self.pos_x = width - self.size_x
        self.pos_x += self.x_speed
        if self.alive:
            pygame.draw.rect(screen, WHITE, [self.pos_x, self.pos_y, self.size_x , self.size_y])
        else:
            pygame.draw.rect(screen, GREEN, [self.pos_x, self.pos_y, self.size_x , self.size_y])
        return dead
    def isShot(self, bullet):
        rect = pygame.Rect(self.pos_x, self.pos_y, self.size_x, self.size_y)
        if rect.colliderect(bullet.getRect()):
            print ("HIT")
            self.alive = False
            bullet.reset()
            return True
    def reverse(self):
        self.x_speed = self.x_speed * -1
    def outOfRightBound(self, bound):
        if self.pos_x > bound.pos_x:
            return true
    def outOfLeftBound(self, bound):
        if self.pos_x < bound.pos_x:
            return true
    def isAlive(self):
        return self.alive


class Fleet:
    def __init__(self):
        self.shipList = []
        self.shipCount = 5
        #self.shipSpeed = 5
        self.pos_x = 50
        self.pos_y = 0
        self.left_bound = None
        self.right_bound = None
        self.max_right = width - 50
        self.max_left = 50
        for i in range(0, self.shipCount):
            # change enemy ship init
            e = EnemyShip()
            print ("made an enemy")
            e.pos_x = self.pos_x
            self.pos_x += 50 # divide by number of ships in row
            self.shipList.append(e)
        self.shipList = sorted(self.shipList, key = lambda ship: ship.pos_x)
        for ship in self.shipList:
            print(ship.pos_x)
        self.left_bound = self.shipList[0]
        self.right_bound = self.shipList[-1]


    def Update(self, bullet):
        # update each ship
        for ship in self.shipList:
            if ship.Update(bullet):
                self.shipList.remove(ship)
        # if the right most ship is too far reverse it
        if self.right_bound.pos_x > self.max_right:
            for ship in self.shipList:
                ship.reverse()
        # same but on the left side
        if self.left_bound.pos_x < self.max_left:
            for ship in self.shipList:
                ship.reverse()
        # check to see if the left and right most are still alive somehow
            # reassign if not (left bound and right bound)
        # step down
        # shoot at you






class HeroShip(BaseShip):
    def __init__(self):
        self.size_x = 50
        self.size_y = 50
        self.pos_x = width/2
        self.pos_y = height - self.size_y - 10
        self.x_speed = 0

    def getPosX(self):
        return self.pos_x

    def getMidPoint(self):
        return self.size_x/2

    def getPosY(self):
        return self.pos_y

    def goLeft(self):
        self.x_speed = -3

    def goRight(self):
        self.x_speed = 3

    def halt(self):
        self.x_speed = 0

    def Update(self):
        if self.pos_x < 0:
            self.x_speed = 0
            self.pos_x = 0
        if self.pos_x > (width - self.size_x):
            self.x_speed = 0
            self.pos_x = width - self.size_x
        self.pos_x += self.x_speed
        pygame.draw.rect(screen, WHITE, [self.pos_x, self.pos_y, self.size_x , self.size_y])

        



class Bullet:
    def __init__(self):
        self.pos_x = -10
        self.pos_y = 0
        self.size_x = 4
        self.size_y = 9
        self.speed = -20
        self.ReadyToShoot = True
        self.Shooting = False

    def reset(self):
        self.Shooting = False
        self.ReadyToShoot = True
        self.pos_x = -10
        self.pos_y = 0
    def isReady(self):
        if (self.ReadyToShoot):
            return True
    def Update(self):
        if (self.Shooting):
            self.pos_y += self.speed
            Bullet = [self.pos_x, self.pos_y, self.size_x, self.size_y]
            pygame.draw.rect(screen, WHITE, Bullet)
        if self.pos_y < 0:
            self.reset()

    def getPosX(self):
        return self.pos_x
    def getPosY(self):
        return self.pos_y

    def getRect(self):
        return [self.pos_x, self.pos_y, self.size_x, self.size_y]

    def shoot(self, ship):
        self.pos_x = ship.getPosX() + ship.getMidPoint()
        self.pos_y = ship.getPosY()
        self.ReadyToShoot = False
        self.Shooting = True


bullet = Bullet()
ship = HeroShip()
#enemy = EnemyShip()
enemyFleet = Fleet()

#BulletShot = False
#ReadyToShoot = True
#Bullet = (screen, WHITE, [bullet_pos_x, bullet_pos_y, Bullet_size_x, Bullet_size_y])



# main loop!

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        # User pressed down on a key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                ship.goLeft()
            if event.key == pygame.K_RIGHT:
                ship.goRight()
            if event.key == pygame.K_SPACE:
                if (bullet.isReady()):
                    bullet.shoot(ship)

     
        # User let up on a key
        if event.type == pygame.KEYUP:
            # If it is an arrow key, reset vector back to zero
            if event.key == pygame.K_LEFT:
                ship.halt()
            if event.key == pygame.K_RIGHT:
                ship.halt()
            

    screen.fill(BLACK)


    bullet.Update()
    ship.Update()
    enemyFleet.Update(bullet)

    #enemy.Update(bullet)
    #pygame.draw.rect(screen, WHITE, [x_coord, y_coord, HeroShip_x, HeroShip_y])

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
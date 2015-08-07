import pygame
import random

class BaseShip:
    def __init__(self):
        self.speed = 3
        self.pos_x = None
        self.pos_y = None
        self.size_x = None
        self.size_y = None
        self.alive = True
    def isAlive(self):
        return self.alive
    def getPosX(self):
        return self.pos_x

    def getMidPoint(self):
        return self.size_x/2

    def getPosY(self):
        return self.pos_y
    def getRect(self):
        return [self.pos_x, self.pos_y, self.size_x, self.size_y]
       


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
        self.x_speed = 1
        self.alive = True

    def __str__(self):
        return ("ship is at: " + str(self.pos_x) + ", " + str(self.pos_y))

    def Update(self, bullet):
        if self.isShot(bullet):
            return True

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
    def moveDown(self):
        self.pos_y += self.size_y


class Fleet:
    # add ship columns in order to find the ship that shoots, might be more efficient than a list of the lowest
    def __init__(self, ship):
        self.shipList = []
        self.shipColumns = []
        self.shipCount = 7
        self.rowCount = 3
        #self.shipSpeed = 5
        self.pos_x = 50
        self.pos_y = 0
        self.left_bound = None
        self.right_bound = None
        self.max_right = width - 50
        self.max_left = 50
        self.recentlyKilled = None
        self.lowestShips = []
        self.oldLowest = None
        self.intervalBetweenShots = 100
        self.timer = 0

        self.bulletList = []
        self.heroShip = ship
        
        # across
        for i in range (0, self.shipCount):
            tempList = []
            # down
            for j in range(0, self.rowCount):
                e = EnemyShip()
                e.pos_x = self.pos_x
                e.pos_y = self.pos_y
                self.pos_y += 50
                self.shipList.append(e)
                tempList.append(e)
            self.shipColumns.append(tempList)
            self.pos_y = 0
            self.pos_x += 50

        self.shipList = sorted(self.shipList, key = lambda ship: ship.pos_x)
        self.setBounds()
        self.setLowest()

    def animateBullets(self):
        doneBullets = []
        for b in self.bulletList:
            if(b.Update(self.heroShip)):
                doneBullets.append(b)
        for b in doneBullets:
            self.bulletList.remove(b)




    def setLowest(self):
        for column in self.shipColumns:
            tempList = sorted(column, key = lambda ship: -ship.pos_y)
            if (tempList):
                if (tempList[0] not in self.lowestShips):
                    self.lowestShips.append(tempList[0])
    
    def resetLowest(self, deadShip):
        if (deadShip in self.lowestShips):
            # walk through the columns
            for i in range(len(self.shipColumns)):
                # for all the ships in the column
                if deadShip in self.shipColumns[i]:
                    # remove it from the lowestShips
                    self.lowestShips.remove(deadShip)
                    # remove it from the temp ships list
                    self.shipColumns[i].remove(deadShip)
                    # reset the lowest ships
                    self.setLowest()
                    
                    break

    def setBounds(self):
        if len(self.shipList) > 1:
            self.shipList = sorted(self.shipList, key = lambda ship: ship.pos_x)
            self.left_bound = self.shipList[0]
            self.right_bound = self.shipList[-1]
        
    def stepDown(self):
        for ship in self.shipList:
            ship.moveDown()

    def reverseFleet(self):
        for ship in self.shipList:
            ship.reverse()


    def shoot(self):

        #for ship in self.lowestShips:
        if (self.timer > self.intervalBetweenShots):
            if (self.lowestShips):
                ship = random.choice(self.lowestShips)
                print(ship)
                b = EnemyBullet()
                b.shoot(ship)

                self.bulletList.append(b)
            self.timer = 0


    def dead(self):
        self.shipList.remove(self.recentlyKilled)
        self.resetLowest(self.recentlyKilled)
        for i in range(len(self.shipColumns)):
                # for all the ships in the column
                if self.recentlyKilled in self.shipColumns[i]:
                    self.shipColumns[i].remove(self.recentlyKilled)
                    break
        self.recentlyKilled = None


    def Update(self, bullet):
        # update timer
        self.timer += 1
        # update each ship
        for ship in self.shipList:
            # if the ship is dead
            if ship.Update(bullet):
                # set it to be removed after all the ships have moved
                self.recentlyKilled = ship
        self.shoot()
        self.animateBullets()
                
        # if there was a ship that died then take it out of the list
        if (self.recentlyKilled):
            self.dead()


        # if the far left or the far right die then reset bounds
        if (not self.left_bound.isAlive()) or (not self.right_bound.isAlive()):
            self.setBounds()

        # if the right most ship or the left most ship is too far reverse it
        if self.right_bound.pos_x > self.max_right or self.left_bound.pos_x < self.max_left:
            self.reverseFleet()
            # step the fleet down
            self.stepDown()
 
        

        # shoot at you






class HeroShip(BaseShip):
    def __init__(self):
        self.size_x = 50
        self.size_y = 50
        self.pos_x = width/2
        self.pos_y = height - self.size_y - 10
        self.x_speed = 0
        self.alive = True

    def shot(self):
        self.alive = False
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
        if (self.isAlive()):
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

class EnemyBullet(Bullet):
    def __init__(self):
        self.pos_x = -10
        self.pos_y = 0
        self.size_x = 4
        self.size_y = 9
        self.speed = 5
        self.ReadyToShoot = True
        self.Shooting = False
        self.done = False
    def Update(self, hero):
        if (self.Shooting):
            self.pos_y += self.speed
            Bullet = [self.pos_x, self.pos_y, self.size_x, self.size_y]
            pygame.draw.rect(screen, WHITE, Bullet)
        if self.pos_y > height:
            self.reset()
            self.done = True

        rect = pygame.Rect(self.pos_x, self.pos_y, self.size_x, self.size_y)
        if rect.colliderect(hero.getRect()):
            print("hero shot!")
            hero.shot()
            self.reset()
            self.done = True
        return self.done

bullet = Bullet()
ship = HeroShip()
#enemy = EnemyShip()
enemyFleet = Fleet(ship)

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

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
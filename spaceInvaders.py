import pygame
import random

#test

""" BaseShip is the primary ship class which returns
the position of each ship and their midpoints.
"""
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
RED = (255, 0, 0)
BLUE = (0, 0, 255)

#block size is the size of each block for the barriers
BLOCK_SIZE = 15


pygame.init()
# the width and height of the gamescreen
width = 700
height = 500
size = (width, height)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Space Invaders")

done = False

clock = pygame.time.Clock()


class BulletManager:
    def __init__(self):
        self.bulletCollection = []
        self.recentlyKilled = None


    def Update:
        for bullet in self.bulletCollection:
            # if the bullet's life ends then it has to be removed later
            if (bullet.Update()):
                self.recentlyKilled = bullet
        self.bulletCollection.remove(self.recentlyKilled)
        

""" The TextManager class handles the text that will be displayed on the screen
"""
class TextManager:
    def __init__(self):
        self.font = pygame.font.SysFont("monospace", 15)
        self.win = False
        self.lose = False
        self.score = 0
        self.lives = 3

    def wonTheGame():
        self.win = True

    def LostTheGame():
        self.lose = True

    def increaseScore(self):
        self.score += 1
        if self.score == 21:
            self.win = True

    def loseLife(self):
        if self.lives > 0:
            self.lives -= 1
        else:
            self.lose = True
            self.haltShips()
        return self.lose

    def Update():
        #reset font
        self.font = pygame.font.SysFont("monospace", 15)
        self.font.set_bold(True)

        # write the score and lives left on the top
        label = self.font.render("Game Score: " + str(self.score), 1, GREEN)
        screen.blit(label, (10,10))
        label = self.font.render("Lives Left: " + str(self.lives), 1, GREEN)
        screen.blit(label, (width - label.get_rect().width - 10, 10))

        # if all the ships are dead (21) then print the win text
        if self.win:
            self.font = pygame.font.SysFont("monospace", 75)
            self.font.set_bold(True)
            label = self.font.render("YOU WIN!", 1, GREEN)
            screen.blit(label, (width/2 - label.get_rect().width/2, height/2 - label.get_rect().height/2))
        if self.lose:
            self.font = pygame.font.SysFont("monospace", 75)
            self.font.set_bold(True)
            label = self.font.render("YOU LOSE!", 1, GREEN)
            screen.blit(label, (width/2 - label.get_rect().width/2, height/2 - label.get_rect().height/2))



class GameManager:
    def __init__(self):
        self.score = 0
        self.font = pygame.font.SysFont("monospace", 15)
        self.font.set_bold(True)
        self.win = False
        self.lives = 3
        self.lose = False
        self.done = False
        self.bonusShip = None

    def Update(self, bullet, ship):
        # handle the bonus ship
        if self.bonusShip:
            self.bonusShip.Update(bullet, ship)

        




    def haltShips(self):
        self.done = True
    def isDone(self):
        return self.done
    def shipLanded(self):
        self.lose = True
        self.haltShips()
    def makeBonusShip(self):
        self.bonusShip = BonusEnemyShip(self)


class BonusEnemyShip(BaseShip):
    def __init__(self, gameManager):
        self.size_x = 25
        self.size_y = 25
        self.gameManager = gameManager
        self.x_speed = 7
        self.alive = True
        self.pos_x = 0
        self.pos_y = 50
        self.bullet = None

    def isShot(self, bullet):
        rect = pygame.Rect(self.pos_x, self.pos_y, self.size_x, self.size_y)
        if rect.colliderect(bullet.getRect()):
            print ("HIT")
            self.alive = False
            bullet.reset()
            return True

    def shoot(self):
        # random number things
        if self.pos_x > 255 and not self.bullet:
            self.bullet = EnemyBullet(self.gameManager)

            self.bullet.shoot(self)



    def Update(self, Bullet, ship):
        self.shoot()
        if self.gameManager.isDone():
            self.x_speed = 0
        if self.isShot(bullet):
            print(self.x_speed)
            self.isAlive = False
            self.gameManager.increaseScore() # more than one later

        self.pos_x += self.x_speed

        if self.pos_x > width:
            self.alive = False

        if self.alive:
            pygame.draw.rect(screen, RED, [self.pos_x, self.pos_y, self.size_x, self.size_y])

        if self.bullet:
            self.bullet.Update(ship)






class EnemyShip(BaseShip):
    def __init__(self, gameManager):
        self.size_x = 25
        self.size_y = 25
        self.pos_x = width/2
        self.pos_y = 0
        self.x_speed = 1
        self.alive = True
        self.gameManager = gameManager

    def __str__(self):
        return "ship is at: " + str(self.pos_x) + ", " + str(self.pos_y)

    # going right, increase speed value
    # going left, decrease speed value (still increases ship speed)
    def increaseSpeed(self):
        if self.x_speed > 0:
            self.x_speed += .25
        else:
            self.x_speed -= .25

    def Update(self, bullet):
        if self.gameManager.isDone():
            self.x_speed = 0


        if self.isShot(bullet):
            print(self.x_speed)
            return True


        if self.pos_x < 0:
            self.x_speed = self.x_speed * -1
            self.pos_x = 0
        if self.pos_x > (width - self.size_x):
            self.x_speed = self.x_speed * -1
            self.pos_x = width - self.size_x

        self.pos_x += self.x_speed

        if self.alive:
            pygame.draw.rect(screen, RED, [self.pos_x, self.pos_y, self.size_x, self.size_y])

        self.landedOnGround()
        #else:
        #    pygame.draw.rect(screen, GREEN, [self.pos_x, self.pos_y, self.size_x, self.size_y])

    


class Fleet:
    # add ship columns in order to find the ship that shoots, might be more efficient than a list of the lowest
    def __init__(self, ship, gameManager):
        self.gameManager = gameManager
        self.shipList = []
        self.shipColumns = []
        # shipStart is the y coordinate of where the ships spawn
        self.shipStart = 30
        self.shipCount = 7
        self.rowCount = 3

        self.pos_x = 50
        self.pos_y = self.shipStart
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

        
        self.steps = 0
        
        # across
        for i in range (0, self.shipCount):
            tempList = []
            # down
            for j in range(0, self.rowCount):
                e = EnemyShip(self.gameManager)
                e.pos_x = self.pos_x
                e.pos_y = self.pos_y
                self.pos_y += 50
                self.shipList.append(e)
                tempList.append(e)
            self.shipColumns.append(tempList)
            self.pos_y = self.shipStart
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
        self.steps += 1

    def reverseFleet(self):
        for ship in self.shipList:
            ship.reverse()


    def shoot(self):
        #for ship in self.lowestShips:
        if (self.timer > self.intervalBetweenShots):
            if (self.lowestShips):
                ship = random.choice(self.lowestShips)
                print(ship)
                b = EnemyBullet(self.gameManager)
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

        #increase the speed of all the ships
        self.increaseFleetSpeed()

    def increaseFleetSpeed(self):
        for ship in self.shipList:
            ship.increaseSpeed()

    def getBullets(self):
        return self.bulletList


    def Update(self, bullet):
        if not self.gameManager.isDone():
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
            # update the score
            if (self.recentlyKilled):
                self.dead()
                self.gameManager.increaseScore()


            # if the far left or the far right die then reset bounds
            if (not self.left_bound.isAlive()) or (not self.right_bound.isAlive()):
                self.setBounds()

            # if the right most ship or the left most ship is too far reverse it
            if self.right_bound.pos_x > self.max_right or self.left_bound.pos_x < self.max_left or self.right_bound.pos_x < self.max_left or self.left_bound.pos_x > self.max_right:
                self.reverseFleet()
                # step the fleet down
                self.stepDown()

            #spawn bonus ship if ready
            if self.steps == 2:
                self.gameManager.makeBonusShip()
                self.steps = 0

        else:
            self.animateBullets()
            for ship in self.shipList:
                # if the ship is dead
                ship.Update(bullet)

    

class HeroShip(BaseShip):
    def __init__(self, gameManager):
        self.size_x = 50
        self.size_y = 50
        self.pos_x = width/2
        self.pos_y = height - self.size_y - 10
        self.x_speed = 0
        self.alive = True
        self.gameManager = gameManager

    def shot(self):
        self.die()
    def goLeft(self):
        self.x_speed = -3

    def goRight(self):
        self.x_speed = 3

    def halt(self):
        self.x_speed = 0

    def die(self):
        # if loseLife returns true, we are out of lives
        if self.gameManager.loseLife():
            self.alive = False

    def Update(self):
        if self.pos_x < 0:
            self.x_speed = 0
            self.pos_x = 0
        if self.pos_x > (width - self.size_x):
            self.x_speed = 0
            self.pos_x = width - self.size_x
        self.pos_x += self.x_speed
        if (self.isAlive()):
            pygame.draw.rect(screen, BLUE, [self.pos_x, self.pos_y, self.size_x , self.size_y])
        if gameManager.isDone():
            self.alive = False
        

class Bullet:
    def __init__(self, gameManager):
        self.pos_x = -10
        self.pos_y = 0
        self.size_x = 4
        self.size_y = 9
        self.speed = -15
        self.ReadyToShoot = True
        self.Shooting = False
        self.gameManager = gameManager

    def reset(self):
        self.Shooting = False
        self.ReadyToShoot = True
        self.pos_x = -10
        self.pos_y = 0
    def isReady(self):
        if (self.ReadyToShoot):
            return True
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

    def Update(self):
        if self.gameManager.isDone():
            self.speed = 0
        if (self.Shooting):
            self.pos_y += self.speed
            Bullet = [self.pos_x, self.pos_y, self.size_x, self.size_y]
            pygame.draw.rect(screen, WHITE, Bullet)
        if self.pos_y < 0:
            self.reset()

    

class EnemyBullet(Bullet):
    def __init__(self, gameManager):
        self.pos_x = -10
        self.pos_y = 0
        self.size_x = 4
        self.size_y = 9
        self.speed = 5
        self.ReadyToShoot = True
        self.Shooting = False
        self.done = False
        self.gameManager = gameManager
    def reset(self):
        self.Shooting = False
        self.ReadyToShoot = True
        self.pos_x = -10
        self.pos_y = 0
        self.done = True

    def Update(self, hero):
        if self.gameManager.isDone():
            self.speed = 0
        if self.Shooting:
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

# maybe for later, to keep track of all projectiles
'''
class BulletManager:
    def __init__(self):
'''

# TODO: drop bullet speeds and up frame rate to get proper collision
class Block:
    def __init__(self, x, y, gameManager):
        self.size_x = BLOCK_SIZE
        self.size_y = BLOCK_SIZE
        self.dead = False
        self.pos_x = x
        self.pos_y = y
        self.gameManager = gameManager

    """ update function, called every frame.
    takes the hero bullet and the entire fleet so the bullets can be retrieved
    """
    def Update(self, heroBullet, EnemyBullets):
        
        blockSize = [self.pos_x, self.pos_y, self.size_x, self.size_y]
        pygame.draw.rect(screen, GREEN, blockSize)

        rect = pygame.Rect(self.pos_x, self.pos_y, self.size_x, self.size_y)
        

        for bullet in EnemyBullets:
            if rect.colliderect(bullet.getRect()):
                print("shot by enemy")
                self.dead = True
                bullet.reset()

        if rect.colliderect(heroBullet.getRect()):
            print("we shot it!")
            self.dead = True
            heroBullet.reset()

        #make the outer ifs into a function in gamemanager
        if gameManager.bonusShip:
            if gameManager.bonusShip.bullet:
                if rect.colliderect(gameManager.bonusShip.bullet.getRect()):
                    self.dead = True
                    gameManager.bonusShip.bullet.reset()

                
        return self.dead

class Barrier(Block):
    def __init__(self, x, gameManager):
        self.pos_x = x
        self.pos_y = height - 125
        self.blockList = []
        self.recentlyKilled = None
        self.size_x = BLOCK_SIZE
        self.size_y = BLOCK_SIZE
        self.offset_x = 0
        self.offset_y = 0
        self.gameManager = gameManager
        for i in range(12):
            i += 1
            if i != 6 and i != 7 and i != 10 and i != 11:
                self.blockList.append(Block(self.pos_x + self.offset_x, self.pos_y + self.offset_y, self.gameManager))
            self.offset_x += self.size_x
            if i % 4 == 0:
                self.offset_y += self.size_y
                self.offset_x = 0

    def Update(self, heroBullet, EnemyBullets):
        for block in self.blockList:
            if block.Update(heroBullet, EnemyBullets):
                self.recentlyKilled = block

        if self.recentlyKilled:
            self.blockList.remove(self.recentlyKilled)
            self.recentlyKilled = None




gameManager = GameManager()
bullet = Bullet(gameManager)
ship = HeroShip(gameManager)
#enemy = EnemyShip()
enemyFleet = Fleet(ship, gameManager)
barrier1 = Barrier(75, gameManager)
barrier2 = Barrier(225, gameManager)
barrier3 = Barrier(375, gameManager)
barrier4 = Barrier(525, gameManager)



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
                if (bullet.isReady() and ship.isAlive()):
                    bullet.shoot(ship)

     
        # User let up on a key
        if event.type == pygame.KEYUP:
            # If it is an arrow key, reset vector back to zero
            if event.key == pygame.K_LEFT:
                ship.halt()
            if event.key == pygame.K_RIGHT:
                ship.halt()
            

    screen.fill(BLACK)
    barrier1.Update(bullet, enemyFleet.getBullets())
    barrier2.Update(bullet, enemyFleet.getBullets())
    barrier3.Update(bullet, enemyFleet.getBullets())
    barrier4.Update(bullet, enemyFleet.getBullets())
    bullet.Update()
    ship.Update()
    
    enemyFleet.Update(bullet)
    gameManager.Update(bullet, ship)
    #block.Update(bullet, enemyFleet.getBullets())

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
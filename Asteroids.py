import pyxel #imports
import random
import json

class Bullet:
    def __init__(self, x, y, direction, speed, screen):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        self.screen = screen

    def update(self):
        if self.direction == 'W':
            self.y -= self.speed
        if self.direction == 'S':
            self.y += self.speed
        if self.direction == 'A':
            self.x -= self.speed
        if self.direction == 'D':
            self.x += self.speed

    def draw(self):
        if self.direction in ['W', 'S']:
            pyxel.blt(self.x, self.y, 0, 49, 21, 2, 3)
        else:
            pyxel.blt(self.x, self.y, 0, 49, 18, 3, 2)

    def checkIfOut(self):
        if self.x > self.screen or self.x < 0 or self.y > self.screen or self.y < 0:
            return True
        else:
            return False


class App: #the whole app
    def __init__(self): #begening
        self.rockRandom = [] #makes game random with random nums on x
        for pixel in range(201):
            self.rockRandom.append(random.randint(1, 20))
        self.screen = 200 #screen size
        pyxel.init(self.screen, self.screen, 'Asteroids') #make screen'
        pyxel.fullscreen(False)
        self.x = self.screen / 2 - 8 #add player x and y in middle
        self.y = self.screen / 2 - 8
        self.speed = 2.5 #speed of player
        self.bulletSpeed = 4 #speed of bullets
        self.flipX = 15 #player sprite
        self.flipY = 16
        self.cornerX = 0
        self.bullets = [] #message from update to draw for bullets
        self.WSAD = 'none' #where the players going
        self.hitboxes = [] #all rock hitboxes
        self.score = 0 #keeps track or player's score
        self.showHitboxesToggle = False #keeps track of if hitboxes are on
        self.removedBig = [] #all the removed rocks
        self.removedSmall = []
        self.startScreen = True #true if youre at the start screen
        self.leaderboardScreen = False #true if youre at the leaderboard
        self.deadScreen = False #true when you win
        self.causeOfDeath = 'Unknown'
        self.lives = 3
        self.timer = False
        self.time = 0
        self.level = 1
        self.keyboard = False
        self.coinsTimeCombined = 0
        self.name = ''
        self.nameDone = False
        self.secondCooldown = 30
        self.livesCooldown = 75
        self.coinsTime = 0
        self.quarters = [random.randint(0, 50),#cords to make the rocks not spawn
                         random.randint(50, 160),#on the player or off the map
                         random.randint(50, 160),
                         random.randint(110, 160),
                         random.randint(110, 160),
                         random.randint(0, 110),
                         random.randint(0, 110),
                         random.randint(0, 50)]

        pyxel.load('Sprites.pyxres') #load the sprites
        pyxel.run(self.update, self.draw) #start game

    def genRock(self, x, y, small): #add a rock and its hitbox

        if [x, y] in self.removedBig:
            self.placeSmallRocks(x, y)
            return

        hitboxEnds = []

        if small == False:
            if self.rockRandom[x] <= 5: #randomly pick from four big rocks
                pyxel.blt(x, y, 0, 1, 17, 37, 31, 7)
            elif self.rockRandom[x] <= 10:
                pyxel.blt(x, y, 0, 2, 50, 36, 31, 7)
            elif self.rockRandom[x] <= 15:
                pyxel.blt(x, y, 0, 57, 17, 40, 31, 7)
            else:
                pyxel.blt(x, y, 0, 58, 50, 40, 31, 7)

            hitboxEnds.append(x + 4) #hitbox
            hitboxEnds.append(x + 35)
            hitboxEnds.append(y - 2)
            hitboxEnds.append(y + 27)
        else:
            if self.rockRandom[x] <= 4: #randomly pick from five small rocks
                pyxel.blt(x, y, 0, 48, 0, 16, 16, 7)
            elif self.rockRandom[x] <= 8:
                pyxel.blt(x, y, 0, 32, 0, 16, 16, 7)
            elif self.rockRandom[x] <= 12:
                pyxel.blt(x, y, 0, 64, 0, 16, 16, 7)
            elif self.rockRandom[x] <= 16:
                pyxel.blt(x, y, 0, 80, 0, 16, 16, 7)
            else:
                pyxel.blt(x, y, 0, 96, 0, 16, 16, 7)

            hitboxEnds.append(x - 2) #hitbox
            hitboxEnds.append(x + 14)
            hitboxEnds.append(y)
            hitboxEnds.append(y + 14)

        if hitboxEnds not in self.hitboxes: #so you cant spam hitboxes and lag
            self.hitboxes.append(hitboxEnds[:])
            hitboxEnds = []

    def placeRocks(self, x, y):
        if x == -1 and y == -1:
            self.genRock(self.quarters[0], self.quarters[1], False)
            self.genRock(self.quarters[2], self.quarters[3], False)
            self.genRock(self.quarters[4], self.quarters[5], False)
            self.genRock(self.quarters[6], self.quarters[7], False)

    def checkRocks(self):
        for hitbox in self.hitboxes[:]: #check all hitboxes
            for bullet in self.bullets[:]: #check all bullets
                if bullet.x >= hitbox[0] and bullet.x <= hitbox[1] and bullet.y >= hitbox[2] and bullet.y <= hitbox[3]:
                    self.bullets.remove(bullet)  # ^^^check if the bullet is inside the hitbox
                    if hitbox[1] - hitbox[0] > 20:
                        remove = [hitbox[0] - 4, hitbox[2] + 2]
                        if remove not in self.removedBig:
                            self.removedBig.append(remove)
                            self.hitboxes.remove(hitbox)
                    else:
                        remove = [hitbox[0] + 2, hitbox[2]]
                        if remove not in self.removedSmall:
                            self.removedSmall.append(remove)
                            self.hitboxes.remove(hitbox)
                    pyxel.playm(0, False)
                    self.score += 10
            for middle in [[self.x+8, self.y], [self.x, self.y+8], [self.x+16, self.y+8], [self.x+8, self.y+16]]: #4 points on the player
                if middle[0] >= hitbox[0] and middle[0] <= hitbox[1] and middle[1] >= hitbox[2] and middle[1] <= hitbox[3]:
                    if self.lives == 1:
                        self.deadScreen = True
                    else:
                        self.lives -= 1
                        self.x = self.screen / 2 - 8
                        self.y = self.screen / 2 - 8
                        self.flipX = 16
                        self.flipY = 16
                        self.livesCooldown = 75
                        self.WSAD = 'none'
    def placeSmallRocks(self, x, y):
        rock1 = [self.minMax(x+self.rockRandom[x], False), self.minMax(y-self.rockRandom[x+1], True)]
        rock2 = [self.minMax(x-self.rockRandom[x+2], True), self.minMax(y+self.rockRandom[x+3], False)]
        for rock in [rock1, rock2]:
            if rock[0] >= 76 and rock[0] <= 108 and rock[1] >= 76 and rock[1] <= 108: #not spawn in the player area
                rock[1] -= 30
        if rock1 not in self.removedSmall:
            self.genRock(rock1[0], rock1[1], True)
        if rock2 not in self.removedSmall:
            self.genRock(rock2[0], rock2[1], True)

    def showHitboxes(self):
        for hitbox in self.hitboxes:
            pyxel.rectb(hitbox[0], hitbox[2], hitbox[1]-hitbox[0], hitbox[3]-hitbox[2], 8)

    def minMax(self, num, leftUp):
        if leftUp == True:
            return max(num, 0)
        else:
            return min(num, 190)

    def restart(self): #restarts the game for a new level
        self.level += 1
        self.speed += 0.2
        self.bulletSpeed += 0.2
        self.rockRandom = [] #makes game random with random nums on x
        for pixel in range(201):
            self.rockRandom.append(random.randint(1, 20))
        self.x = self.screen / 2 - 8 #add player x and y in middle
        self.y = self.screen / 2 - 8
        self.flipX = 15 #player sprite
        self.flipY = 16
        self.cornerX = 0
        self.bullets = [] #message from update to draw for bullets
        self.WSAD = 'none' #where the players going
        self.hitboxes = [] #all rock hitboxes
        self.removedSmall = [] #all the removed rocks
        self.removedBig = []
        self.startScreen = False #true if youre at the start screen
        self.deadScreen = False #keeps track of death
        self.leaderboardScreen = False #true when youre at the leaderboard
        self.timer = False #is the timer on
        self.time = 0 #how long its been
        self.secondCooldown = 30 #30 FPS
        self.keyboard = False
        self.coinsTime = 0
        self.name = ''
        self.livesCooldown = 75 #to flash the ship
        self.quarters = [random.randint(0, 50),#cords to make the rocks not spawn
                         random.randint(50, 160),#on the player or off the map
                         random.randint(50, 160),
                         random.randint(110, 160),
                         random.randint(110, 160),
                         random.randint(0, 110),
                         random.randint(0, 110),
                         random.randint(0, 50)]

    def leaderboard(self):
        pyxel.rectb(20, 30, 160, 140, 5)

        with open('leaderboard.txt', 'r') as file:
            leaderboard = json.load(file)
            leaderboard = list(sorted(leaderboard.items(), key=lambda item: item[1]))
            leaderboard = leaderboard[::-1]
            iter = 1
            for player in leaderboard:
                pyxel.text(30, iter*7+30, f"#{iter}, {player[0]}'s score: {player[1][0]}, level {player[1][1]}", 5)
                iter += 1

    def update(self):
        if self.nameDone == True:
            with open('Leaderboard.txt', 'r') as file:
                leaderboard = json.load(file)
                if self.name in leaderboard and leaderboard[self.name][0] < self.score:
                    leaderboard[self.name] = [self.score, self.level]
                elif self.name not in leaderboard:
                    leaderboard[self.name] = [self.score, self.level]
            with open('Leaderboard.txt', 'w') as file:
                json.dump(leaderboard, file)
            return

        if self.keyboard == True:
            for key in range(ord('a'), ord('z')+1):
                if pyxel.btnp(key):
                    if pyxel.btn(pyxel.KEY_SHIFT):
                        self.name = self.name + (chr(key)).upper()
                    else:
                        self.name = self.name + chr(key)
            for num in range(ord('0'), ord('9')+1):
                if pyxel.btnp(num):
                    self.name = self.name + chr(num)
            if pyxel.btnp(pyxel.KEY_BACKSPACE):
                self.name = self.name[0:len(self.name)-1]
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.name = self.name + ' '


        if self.startScreen == True and pyxel.btn(pyxel.KEY_L):
            self.startScreen = False
            self.leaderboardScreen = True
            return

        if self.leaderboardScreen == True and pyxel.btn(pyxel.KEY_B):
            self.startScreen = True
            self.leaderboardScreen = False
            return

        if pyxel.btnp(pyxel.KEY_RETURN):
            self.startScreen = False

        if self.startScreen == True:
            return

        if self.livesCooldown != 0:
            self.livesCooldown -= 1
            return



        if pyxel.btnp(pyxel.KEY_W): #WSAD controls, flips player and modifys wsad to alert 186
            self.flipX = 16
            self.flipY = 16
            self.cornerX = 0
            if self.WSAD == 'none':
                self.timer = True
            self.WSAD = 'W'
        elif pyxel.btnp(pyxel.KEY_S):
            self.flipX = 16
            self.flipY = -16
            self.cornerX = 0
            if self.WSAD == 'none':
                self.timer = True
            self.WSAD = 'S'
        elif pyxel.btnp(pyxel.KEY_A):
            self.flipX = -16
            self.flipY = 16
            self.cornerX = 16
            if self.WSAD == 'none':
                self.timer = True
            self.WSAD = 'A'
        elif pyxel.btnp(pyxel.KEY_D):
            self.flipX = 16
            self.flipY = 16
            self.cornerX = 16
            if self.WSAD == 'none':
                self.timer = True
            self.WSAD = 'D'

        if self.WSAD == 'W': #keeps the player always moving
            self.y -= self.speed
        if self.WSAD == 'S':
            self.y += self.speed
        if self.WSAD == 'A':
            self.x -= self.speed
        if self.WSAD == 'D':
            self.x += self.speed


        if self.timer == True: #adds to the timer one second every 30 frames, because its 30FPS
            if self.secondCooldown == 0:
                self.time += 1
                self.secondCooldown = 30
            else:
                self.secondCooldown -= 1

        self.checkRocks() #check hitboxes

        if self.x < 0: #for wraparound
            self.x = self.screen-16
        elif self.x > self.screen-16:
            self.x = 0
        elif self.y < 0:
            self.y = self.screen-16
        elif self.y > self.screen-16:
            self.y = 0



        if pyxel.btnp(pyxel.KEY_H): #toggles hitboxes, messager end to 300
            if self.showHitboxesToggle:
                self.showHitboxesToggle = False
            else:
                self.showHitboxesToggle = True

        if len(self.removedBig) + len(self.removedSmall) == 12:
            if self.time < 25:
                self.coinsTime = (25 - self.time) * 10
                self.score += self.coinsTime
                self.coinsTimeCombined += self.coinsTime

            self.restart()

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_SPACE): #shooting logic
            self.bullets.append(Bullet(self.x+7, self.y+7, self.WSAD, self.bulletSpeed, self.screen))

    def draw(self):
        pyxel.cls(0) #clear the screen for the new frame

        if self.deadScreen == True:
            self.timer = False
            text1 = 'Input name for the leaderboard.'
            text2 = 'Saved!'
            self.leaderboard()
            pyxel.rectb(20, 182, 160, 10, 5)
            pyxel.blt(self.screen/2-31, 10, 0, 0, 88, 63, 16)
            pyxel.text(self.screen/2-(len(self.name)+19)*4/2, 185, f"{self.name}'s score: {self.score}, level {self.level}", 5)

            if pyxel.btn(pyxel.KEY_RETURN) or self.nameDone == True:
                self.nameDone = True
                pyxel.text(self.screen/2-len(text2)*4/2, 175, text2, 5)
            elif self.nameDone == False:
                pyxel.text(self.screen/2-len(text1)*4/2, 175, text1, 5)
            self.keyboard = True
            return

        if self.leaderboardScreen == True:
            self.leaderboard()
            text1 = 'Press B to go back.'
            pyxel.blt(self.screen/2-43.5, 10, 0, 0, 120, 87, 16)
            pyxel.text(self.screen/2-len(text1)*4/2, 182, text1, 5)
            return

        if self.startScreen == True:
            text1 = 'Press enter to start.'
            text2 = 'Press H for hitboxes.'
            text3 = 'Press L for leaderboards.'
            pyxel.blt(self.screen/2-36, 50, 0, 0, 104, 72, 16)
            pyxel.text(self.screen/2-len(text1)*4/2, 125, text1, 5)
            pyxel.text(self.screen/2-len(text2)*4/2, 135, text2, 5)
            pyxel.text(self.screen/2-len(text3)*4/2, 145, text3, 5)
            return

        self.placeRocks(-1, -1) #place origanal rocks


        for bullet in self.bullets[:]: #move bullet based on players oriantation
            if bullet.checkIfOut():
                self.bullets.remove(bullet)
            else:
                bullet.update()
                bullet.draw()
            print(self.bullets)

        if self.showHitboxesToggle: #draws hitboxes if q was pressed, recever end of 219
            self.showHitboxes()

        if len(str(self.livesCooldown)) != 1 or self.livesCooldown == 0:
            if int(list(str(self.livesCooldown))[0]) % 2 == 0:
                pyxel.blt(self.x, self.y, 0, self.cornerX, 0, self.flipX, self.flipY, 0) #player

        pyxel.text(1, 1, f'Score: {self.score}', 5) #score counter

        if self.level < 10:
            pyxel.text(168, 17, f'Level: {self.level}', 5)
        elif self.level < 100:
            pyxel.text(163, 17, f'Level: {self.level}', 5)
        if self.timer == True: #timer
            digits = len(str(self.time)) #puts it in the corner every time
            if digits == 1:
                pyxel.text(195, 25, str(self.time), 5)
            elif digits == 2:
                pyxel.text(191, 25, str(self.time), 5)
            elif digits == 3:
                pyxel.text(187, 25, str(self.time), 5)
        pyxel.rect(155, 0, 45, 16, 12) #puts up hearts
        pyxel.rectb(155, 0, 45, 16, 6)
        if self.lives > 2:
            pyxel.blt(157, 2, 0, 41, 60, 13, 12)
        if self.lives > 1:
            pyxel.blt(171, 2, 0, 41, 60, 13, 12)
        if self.lives > 0:
            pyxel.blt(185, 2, 0, 41, 60, 13, 12)

App() #starts the game

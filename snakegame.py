import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

# Cube class represents each segment of the snake or snack item
class cube(object):
    rows = 40
    w = 600

    # Initialize position, direction, and color
    def __init__(self, start, dirnx=1, dirny=0, color=(255,0,0)):
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny
        self.color = color

    # Update position based on direction
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    # Draw the cube on the surface
    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        
         # Draw eyes on the head of the snake
        if eyes:
            centre = dis // 2
            radius = 3
            circleMiddle = (i * dis + centre - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)

# Snake class manages the snake's body and movement
class snake(object):
    body = []
    turns = {}

    # Initialize snake with color, position, and direction
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1
        self.speed_boost = False
        self.boost_timer = 0


    # Handle movement and turn logic
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()
            
             # Set direction based on key press
            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            # Handle turns for each segment
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                # Handle boundary wrapping
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.dirnx, c.dirny)


    # Reset snake after losing
    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1
        self.speed_boost = False
        self.boost_timer = 0


    # Add new cube to the snake's body when it eats a snack
    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    # Draw each segment of the snake on the surface
    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)



# Redraw window for game frame updates
def redrawWindow(surface):
    global width, rows, s, normalSnack, speedSnack, doubleSnack, lightSnack, light_map,light_timer, goldSnack1, goldSnack2, score, font
    # Draw background color and score based on light_map mode
    if light_map == "on":
        surface.fill((255,255,255))
        score_text = font.render(f"Score:{score}", True, (0,0,0))  # score print out on the screen
        light_timer_text=font.render(f"Timer:{light_timer}", True, (0,0,0)) # count down when the game is on light mode
        surface.blit(light_timer_text,(10,30))
    elif light_map == "off":
        surface.fill ((0,0,0))
        score_text = font.render(f"Score: {score}", True, (255,255,255))  # Black text color
    
     # Draw snake and all snacks
    s.draw(surface)
    normalSnack.draw(surface) # draw the green snack

    if speedSnack:
        speedSnack.draw(surface) # draw the blue snack
    if doubleSnack:
        doubleSnack.draw(surface) # draw the red snack
    if lightSnack:
        lightSnack.draw(surface) # draw white snack
    if goldSnack1:
        goldSnack1.draw(surface) # draw gold snack
    if goldSnack2:
        goldSnack2.draw(surface) # draw gold snack
    
    surface.blit(score_text, (10, 10))  # Position the score at the top left corner
    pygame.display.update()

# Generate a random position for snack not overlapping with snake's body
def randomSnack(rows, item):
    positions = item.body
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break
    return (x, y)

# Display message boxes
def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass
# blue: speed snack
# green: normal snack
# red: double snack
# white: turn on the light to find gold snacks
# Main game loop and initialization
def main():
    global width, rows, s, normalSnack, speedSnack, doubleSnack, lightSnack, light_map,light_timer, goldSnack1, goldSnack2, score, font
    
    # Initialize game parameters
    width, rows, score = 600, 40, 0
    timer_special_snack=3
    win = pygame.display.set_mode((width, width))
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 20)  # Font and size

    s = snake((255, 0, 0), (10, 10))
    normalSnack = cube(randomSnack(rows, s), color=(0, 255, 0))
    speedSnack, doubleSnack,lightSnack,goldSnack1, goldSnack2  = None, None, None, None, None
    light_map, light_timer, gold, printMess = "off", 50, 0, True

    clock = pygame.time.Clock()

    # game loop
    while True:
        pygame.time.delay(50)
        s.move()

        # Handle speed boost
        if s.speed_boost: # If boost is active, increase speed for a limited time
            clock.tick(15)  # Boosted speed
            speeding_timer -= 1
            if speeding_timer <= 0:  # Reset boost after a certain time
                s.speed_boost = False
                speeding_timer = 80
                for i in s.body:
                    if i.color != (204, 204, 0):
                        i.color=(255, 0, 0)

        else:
            clock.tick(7)  # Normal speed

        if timer_special_snack == 0: 
            speedSnack = None
            doubleSnack=None
            lightSnack = None
            timer_special_snack=3

        if light_timer <=0 and light_map== "on":
            light_map = "off"
            goldSnack1, goldSnack2 = None, None
            light_timer=50
            print("Score:",score)
        elif light_map == "on" and s.speed_boost == False:
            light_timer-=1
            print("Time:", light_timer)

        
        if s.body[0].pos == normalSnack.pos:
            score +=5
            timer_special_snack=-1
            s.addCube()
            if s.speed_boost: # change color to blue if snake eats speed snack
                for i in s.body:
                    if i.color != (204, 204, 0):
                        i.color=(0, 128,255)
            normalSnack = cube(randomSnack(rows, s), color=(0, 255, 0))

            # Randomly spawn the special snack
            if random.randint(0, 4) == 0: # speed snack
                speedSnack = cube(randomSnack(rows, s), color=(0, 128,255))
            if random.randint(0, 4) == 0: # double snack
                doubleSnack = cube(randomSnack(rows, s), color=(255,51,51))
            if random.randint(0, 10) == 0: # light snack
                if light_map == "off":
                    lightSnack =cube(randomSnack(rows, s), color=(255,255,255))
            print("Score:",score)

        if speedSnack and s.body[0].pos == speedSnack.pos:
            timer_special_snack=-1
            score +=5
            s.addCube()
            s.speed_boost = True  # Activate speed boost
            speedSnack = None  # Remove special snack after eating
            for i in s.body: #change color to blue if snake eats speed snack
                if i.color != (204, 204, 0):
                    i.color=(0, 128,255)
            print("Score:",score)

        if doubleSnack and s.body[0].pos == doubleSnack.pos:
            timer_special_snack=-1
            s.addCube()
            s.addCube()
            if s.speed_boost:
                for i in s.body: #change color to blue if snake eats speed snack
                    if i.color != (204, 204, 0):
                        i.color=(0, 128,255)

            score +=10
            doubleSnack=None
            print("Score:",score)
        if lightSnack and s.body[0].pos == lightSnack.pos:
            goldSnack1=cube(randomSnack(rows, s), color=(204,204,0))
            goldSnack2=cube(randomSnack(rows, s), color=(204,204,0))
            timer_special_snack=-1
            s.addCube()
            lightSnack=None
            light_map="on"
            score +=5
            print("Score:",score)
        if goldSnack1 and s.body[0].pos == goldSnack1.pos:
            s.addCube()
            s.body[-1].color = (204, 204, 0)
            gold+=1
            goldSnack1= None
        elif goldSnack2 and s.body[0].pos == goldSnack2.pos:
            s.addCube()
            s.body[-1].color = (204, 204, 0)
            gold+=1
            goldSnack2= None

        if gold == 4:
            score+=100
            gold=0
            print("Score:",score)

        # Check for snake collision with itself
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):
                print('Score: ', score)
                message_box('You Lost!', 'Play again...')
                speedSnack, doubleSnack,lightSnack,goldSnack1, goldSnack2  = None, None, None, None, None
                score=0
                light_map="off"
                print("Start again!")
                print("Score: ",score)
                s.reset((10, 10))
                break
        redrawWindow(win)
        if printMess:
            message_box('Rule', 'Green: 5pts\nRed: 10pts\nBlue: 5pts + speeding up\nWhite: Turn on the light in limited of time to find Gold\nGold: Only appears when the light is turned on. Collect 4 Golds to get 100 pts\n\nFact: the time will be frozen in ligh on mode when you eat Blue')
            printMess=False

main()

# Author: Nguyen, Cuong Phuc
# Project's name: Snake Game with Enhanced Gameplay Edition 
# Date: 09/07/2024 - Present
# Environment: Visual Studio Code

import random
import pygame
import tkinter as tk
from tkinter import messagebox
from snake_game_Classes import cube, snake
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
    speeding_timer, light_map, light_timer, gold, printMess = 80,"off", 50, 0, True

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
            if random.randint(0, 3) == 0: # speed snack
                speedSnack = cube(randomSnack(rows, s), color=(0, 128,255))
            if random.randint(0, 3) == 0: # double snack
                doubleSnack = cube(randomSnack(rows, s), color=(255,51,51))
            if random.randint(0, 8) == 0: # light snack
                if light_map == "off":
                    lightSnack =cube(randomSnack(rows, s), color=(255,255,255))
            print("Score:",score)

        if speedSnack and s.body[0].pos == speedSnack.pos:
            speeding_timer = 80
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
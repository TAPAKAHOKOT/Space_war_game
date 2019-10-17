# import moduls
import json
import time
import sys,os
import curses
import keyboard as kb
from random import randint as rn
import ctypes

# ste cmd size
size = [40, 21]
os.system("mode con cols={} lines={}".format( size[0] * 2, size[1] + 1))

# function that create field
def create_field(size):

    arr = []
    arr.append("#" * size[0])

    for k in range( (size[1] - 2) ):
        arr.append(" " * (size[0] ) )
    arr.append("#" * size[0])

    return arr

# move function
def check_move():
    return -1 if kb.is_pressed('w') else (
            1 if kb.is_pressed("s") else 0)

# function checking fire coors
def check_fire(coors):
    return [coors[1][0] + 1, coors[1][1]] if kb.is_pressed("space") else 0

# move bullet function
def move_bullet(pos): return [ pos[0] + 1, pos[1] ]

# this fun draws field
def draw_field(stdscr):

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()
    curses.curs_set(0)

    play = True
    size = [40, 21]
    ship_cors = [ [1, 1], [2, 1] ]
    bullets = []
    enemy_coors = []
    help_coors = []

    score = 0
    chanse = 15
    bullets_num = 50
    health = 3

    # GRAPHICS ===========
    ship = ["H", ">"]
    bullet_skin = "="
    enemy_skin = ["0"]
    help_skin = ["+"]
    # GRAPHICS ===========

    arr = create_field(size)

    # Start colors in curses
    curses.start_color()
    for k in range(255):
        curses.init_pair(k + 1, k, curses.COLOR_BLACK)

    # Loop where k is the last character pressed
    while health > 0:
        # Initialization
        stdscr.clear()

        key = check_move()
        if key:
            if ship_cors[0][1] + key > 0 and ship_cors[0][1] + key < size[1] - 1:
                ship_cors[0][1] +=  key
                ship_cors[1] = [ ship_cors[0][0] + 1, ship_cors[0][1] ]

        for k, bullet in enumerate(bullets): 
            bullets[k] = move_bullet(bullet)
        for k, enemy in enumerate(enemy_coors):
            if enemy not in bullets:
                enemy_coors[k] = [ enemy[0] - 1, enemy[1] ]

        fire = check_fire(ship_cors)
        if bullets_num > 0:
            if fire: bullets.append(fire); bullets_num -= 1

        for k, hel in enumerate(help_coors):
            help_coors[k] = [ hel[0] - 1, hel[1] ]

        if rn(1, chanse) == 1:
            enemy_coors.append([size[0]-1, rn(1, size[1]-2)])

        if rn(1, 150) == 1:
            help_coors.append([ size[0] - 1, rn(1, size[1] - 2)])

        for k in enemy_coors:
            if k[0] < 0:
                health -= 1
                enemy_coors.remove(k)


        if score > 100: chanse = 2
        elif score > 40: chanse = 5
        elif score > 20: chanse = 10

        for y_ind, k in enumerate(arr):
            for x_ind, i in enumerate(k):
                if [x_ind, y_ind] == ship_cors[0]:
                    stdscr.addstr(y_ind, x_ind * 2, ship[0] + " ", curses.color_pair(220))
                elif [x_ind, y_ind] == ship_cors[1]:
                    stdscr.addstr(y_ind, x_ind * 2, ship[1] + " ", curses.color_pair(202))
                elif [x_ind, y_ind] in bullets and [x_ind, y_ind] in enemy_coors:
                    bullets.remove([x_ind, y_ind])
                    enemy_coors.remove([x_ind, y_ind])
                    bullets_num += 3
                    score += 1
                    stdscr.addstr(y_ind, x_ind * 2, "| ", curses.color_pair(229))
                elif ship_cors[0] in help_coors:
                    help_coors.remove(ship_cors[0])
                    bullets_num += 20
                elif ship_cors[1] in help_coors:
                    help_coors.remove(ship_cors[1])
                    bullets_num += 20
                elif [x_ind, y_ind] in bullets:
                    stdscr.addstr(y_ind, x_ind * 2, bullet_skin + " ", curses.color_pair(215))
                elif [x_ind, y_ind] in enemy_coors:
                    stdscr.addstr(y_ind, x_ind * 2, enemy_skin[0] + " ", curses.color_pair(197))
                elif [x_ind, y_ind] in help_coors:
                    stdscr.addstr(y_ind, x_ind * 2, help_skin[0] + " ", curses.color_pair(83))
                elif y_ind == ship_cors[0][1] and x_ind % 3 == 0 and x_ind != 0:
                    stdscr.addstr(y_ind, x_ind * 2, "- ", curses.color_pair(238))
                else:
                    if i == "#":
                        stdscr.addstr(y_ind, x_ind * 2, i + " ")
                    else:
                        stdscr.addstr(y_ind, x_ind * 2, i + "-", curses.color_pair(235))
        stdscr.addstr(y_ind + 1, 0, "Score: " + str(score) + "   Ammo: " + str(bullets_num) + "   Health: " + str(health))


            # Refresh the screen
        stdscr.refresh()

        time.sleep(0.05)

    with open("data_war.json", 'a') as f: f.close()
    with open('data_war.json', 'r') as file:
        try:
            data = json.loads(file.read())
        except: data = [0]
    file.close()

    if score > data[0]:
        data = [score]
        with open('data_war.json', 'w') as file:
            json.dump(data, file)
        file.close()
        best = str(score)
    else: 
        best = data[0]
    
    print("Your score is {}".format(score))
    print("Best Score is {}".format(best))

def main():
    curses.wrapper(draw_field)

if __name__ == "__main__":
    main()
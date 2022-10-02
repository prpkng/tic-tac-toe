import pygame as pg
from enum import Enum
from math import *
from time import time;

pg.init()

size = width, height = 1200, 900

screen = pg.display.set_mode(size)
pg.display.set_caption("Tic tac toe")

cross = pg.image.load("cross.png")
circle = pg.image.load("circle.png")

grey = 240, 240, 240
black = 10, 10, 10

class types(Enum):
    BLANK = 0
    CROSS = 1
    CIRCLE = 2

game_map = [[types.BLANK, types.BLANK, types.BLANK], 
    [types.BLANK, types.BLANK, types.BLANK],
    [types.BLANK, types.BLANK, types.BLANK]]

cur_turn = types.CROSS
cur_spr = [None, cross, circle]

t0 = time()
font = pg.font.Font("./font.ttf", 48)
tinyfont = pg.font.Font("./font.ttf", 36)
print("time took for font creation: ", time()-t0)

cross_score = 0
circle_score = 0

ingame = True
istie = False
def main():
    cur_turn = types.CROSS
    cur_spr = [None, cross, circle]
    running = True

    while (running):
        screen.fill(grey)
        global ingame
        
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                running = False
            elif ev.type == pg.KEYDOWN:
                if pg.key.get_pressed()[pg.K_r]:
                    reset()
            elif ev.type == pg.MOUSEBUTTONDOWN:
                if ingame:
                    if not (pg.mouse.get_pressed()[0]):
                        break

                    pos = pg.mouse.get_pos()
                    if pos[0] > 900:
                        break
                    xsel =  ceil(pos[0] / 300)
                    ysel =  ceil(pos[1] / 300)

                    if game_map[xsel - 1][ysel - 1] != types.BLANK:
                        break

                    game_map[xsel - 1][ysel - 1] = cur_turn


                    if cur_turn == types.CROSS:
                        cur_turn = types.CIRCLE
                    elif cur_turn == types.CIRCLE:
                        cur_turn = types.CROSS
                else:
                    for x in range(3):
                        for y in range(3):
                            game_map[x][y] = types.BLANK
                    ingame = True
                    istie = False
           
        draw_map()
        pg.draw.rect(screen, black, (900, 0, 300, 900))
        
        turn_txt = font.render("Current Turn", True, grey)
        score_txt = font.render("Score:", True, grey)
        cross_txt = tinyfont.render("  Cross:  "+ str(cross_score), True, grey)
        circle_txt = tinyfont.render("  Circle:  "+ str(circle_score), True, grey)

        screen.blit(turn_txt, (900 + (300 / 2 - turn_txt.get_width() / 2), 0, 300, 200))
        screen.blit(score_txt, (900 + (300 / 2 - score_txt.get_width() / 2), 500, 300, 200))
        screen.blit(cross_txt, (900, 575, 300, 200))
        screen.blit(circle_txt, (900, 575 + cross_txt.get_height() + 25, 300, 200))
        screen.blit(cur_spr[cur_turn.value], (900, 50, 300, 300))

        if check_win() != types.BLANK and ingame:
            game_over(check_win().value)
        elif check_tie():
            game_over(-1)
        draw_grid()
        
        if not ingame:
            s = pg.Surface((900, 900))
            s.set_alpha(150)
            s.fill((0, 0, 0))
            screen.blit(s, (0, 0))

            rest = font.render("Click any button to restart", True, grey)
            screen.blit(rest, (900 / 2 - rest.get_width() / 2, 400, 300, 300))

            wintext = ""
            match check_win():
                case types.CROSS:
                    wintext = "Cross wins!"
                case types.CIRCLE:
                    wintext = "Circle wins!"
            
            if check_tie():
                wintext = "Tie"
            
            win = font.render(wintext, True, grey)
            screen.blit(win, (900 / 2 - win.get_width() / 2, 200, 300, 300))
        pg.display.update()
    pg.quit()

def reset():
    global game_map
    for x in range(3):
        for y in range(3):
            game_map[x][y] = types.BLANK
    if pg.key.get_pressed()[pg.K_LSHIFT]:
        global cross_score
        global circle_score
        cross_score = 0
        circle_score = 0
    ingame = True
    istie = False

def check_tie():
    tie = True
    for c in game_map:
        for r in c:
            if r == types.BLANK:
                tie = False
    return tie

def game_over(type):
    global istie
    global cross_score
    global circle_score
    if type == 1:
        cross_score += 1
    elif type == 2:
        circle_score += 2
    elif type == -1:
        istie = True
    global ingame 
    ingame = False
        

def check_win():


    #check collumns
    for x in range(3):
        cross_count = 0
        circle_count = 0
        for y in range(3):
            if game_map[x][y] == types.CROSS:
                cross_count += 1
            elif game_map[x][y] == types.CIRCLE:
                circle_count += 1
        if cross_count == 3:
            return types.CROSS
        if circle_count == 3:
            return types.CIRCLE
    #check rows
    for y in range(3):
        cross_count = 0
        circle_count = 0
        for x in range(3):
            if game_map[x][y] == types.CROSS:
                cross_count += 1
            elif game_map[x][y] == types.CIRCLE:
                circle_count += 1
        if cross_count == 3:
            return types.CROSS
        if circle_count == 3:
            return types.CIRCLE

    #check diagonals 1
    def check_diagonals1():
        cross_count = 0
        circle_count = 0

        for x in range(3):
            if game_map[x][x] == types.CROSS:
                cross_count += 1
            elif game_map[x][x] == types.CIRCLE:
                circle_count += 1
        if cross_count == 3:
            return types.CROSS
        elif circle_count == 3:
            return types.CIRCLE   
        else:
            return types.BLANK

    if check_diagonals1() != types.BLANK:
        return check_diagonals1()

    
    #check diagonals 2
    def check_diagonals2():
        cross_count = 0
        circle_count = 0

        for x in range(3):
            if game_map[2-x][x] == types.CROSS:
                cross_count += 1
            elif game_map[2-x][x] == types.CIRCLE:
                circle_count += 1
        if cross_count == 3:
            return types.CROSS
        elif circle_count == 3:
            return types.CIRCLE   
        else:
            return types.BLANK

    if check_diagonals2() != types.BLANK:
        return check_diagonals2()

    return types.BLANK
            

def draw_map():
    for x in range(3):
        for y in range(3):
            if game_map[x][y] != types.BLANK:
                screen.blit(cur_spr[game_map[x][y].value], pg.Rect(x*300, y*300, 300, 300))

def draw_grid():
    line_wid = 3

    for i in range(2):
        pg.draw.line(screen, black, (300 + i * 300, 0), (300 + i * 300, 900), line_wid)
    
    for i in range(2):
        pg.draw.line(screen, black, (0, 300 + i * 300), (900, 300 + i * 300), line_wid)

main()
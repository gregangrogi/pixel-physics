import pygame
import random
import time
import math

sz = 5
sizex = 86#ширина х
sizey = 86#ширина у
sc = pygame.display.set_mode ([sizex*sz, sizey*sz])
livers = []
mode = 0
type = 1
intense = 3
toolsize = 3

cent = [40, 40]
colors = [((230, 205, 131), (214, 173, 103)),
          ((59, 52, 52), (33, 31, 31)),
          ((235, 230, 230), (210, 210, 210)),
          ((138, 134, 134), (117, 113, 113)),
          ((143, 177, 196), (127, 158, 176)),
          ((161, 133, 92), (140, 116, 80)),
          ((235, 117, 77), (214, 134, 73)),
          ((194, 91, 50), (168, 84, 50)),
          ((143, 110, 76), (133, 105, 76)),
          ((73, 153, 72), (71, 138, 70)),
          ((73, 73, 73), (60, 60, 60))]
bg_c = [(127, 92, 133), (112, 80, 120)]

def iff (x, c):
    r = False
    for d in range(0, len(c)):
        if (x == c[d]):
            r = True
    return  r

def create(x, y):
    l = []
    for yy in range(0, y):
        l.append([])
        for xx in range(0, x):
            l[yy].append(0)
    return l

def fill(l, a):
    x = len(l[0])
    y = len(l)
    for yy in range(0, y ):
        for xx in range(0, x):
            if a > 0:
                l[xx][yy] = a*2-1
            else:
                l[xx][yy] = 0

def p(l, x, y, mde):
    if (mde == 1):
        global cent
        xx = 0
        yy = 0
        if (cent[0]>x):
          xx = 1
        else:
            xx = -1
        if (cent[1]>y):
            yy = 1
        else:
            yy = -1
        return [xx, yy]
    else:
        if (l[x][y+1]>0):
            c = 0
            if(random.randint(1, 2) == 1):
                c = 1
            else:
                c =-1
            if (l[x+c][y+1] > 0):
                if (l[x-c][y+1] > 0):
                    if iff(l[x][y],[10, 16]):
                        if (l[x - c][y] > 0):
                            if (l[x + c][y] > 0):
                                return [0, 1]
                            else:
                                return [c, 0]
                        else:
                            return [-c, 0]
                    else:
                        return [0, 1]
                else:
                    return [-c, 1]
            else:
                return [c, 1]
        else:
            return [0, 1]

def fire(l, xx, yy):
    lf = 0
    br = 0
    for x in range(0, 3):
        for y in range(0, 3):
            if iff(l[xx + x - 1][yy + y - 1], [9, 10]):
                lf += 1
    if (lf == 0):
        for x in range(0, 3):
            for y in range(0, 3):
                if iff(l[xx + x - 1][yy + y - 1], [11, 4]):
                    l[xx + x - 1][yy + y - 1] = 13
                    br += 1
                elif(random.randint(0, 10)==0):
                    if iff(l[xx + x - 1][yy + y - 1], [11, 4, 0]):
                        l[xx + x - 1][yy + y - 1] = 13
        if (random.randint(0, 10) == 0)and(br > 0):
            l[xx][yy] = 5
        else:
            l[xx][yy] = 0
    else:
        l[xx][yy] = 0

def lava(l, fx, fy):
    wt = 0
    for x in range(0, 3):
        for y in range(0, 3):
            if iff(l[fx + x - 1][fy + y - 1], [9, 10]):
                wt +=1
                l[fx + x - 1][fy + y - 1] = 7
            if iff(l[fx + x - 1][fy + y - 1], [4, 3, 11]):
                l[fx + x - 1][fy + y - 1] = 13

def dirt(l, xx, yy):
    green = 0
    lv = 0
    wt = 0
    for x in range(0, 3):
        for y in range(0, 2):
            if iff(l[xx+x-1][yy+y-2], [0, 9, 10]):
                green = 1
    for x in range(0, 3):
        for y in range(0, 3):
            if iff(l[xx + x - 1][yy + y - 1], [13, 16, 15]):
                lv = 1
                green = 0
            if iff(l[xx + x - 1][yy + y - 1], [21]):
                green = 0
            if iff(l[xx + x - 1][yy + y - 1], [10, 9]):
                green = 1
                wt = 1
    if green > 0:
        if (l[xx][yy] == 19):
            l[xx][yy] = 19
        else:
            if random.randint(0, 5) == 0:
                l[xx][yy] = 19
            else:
                l[xx][yy] = 17
    elif lv > 0:
        l[xx][yy] = 21
    else:
        if not (l[xx][yy] == 21):
            l[xx][yy] = 17
    if (wt == 1):
        l[xx][yy] = 19

def check1(l):
    x = len(l[0])
    y = len(l)
    for xx in range(1, x-1):
        for yy in range(1, y-1):
            if (l[xx][yy]%2 == 1) and (l[xx][yy] >0) and not (l[xx][yy] == 7) and not (l[xx][yy] == 11):
                if (l[xx][yy] == 13):
                    fire(l, xx, yy)
                elif (l[xx][yy] == 15):
                    lava(l, xx, yy)
                    l[xx][yy] = 16
                elif iff(l[xx][yy], [17, 19, 21]):
                    dirt(l, xx, yy)
                else:
                    l[xx][yy] = l[xx][yy]+1

def check2(l):
    global mode
    x = len(l[0])
    y = len(l)
    for xx in range(1, x-1):
        for yy in range(1, y-1):
            lx = p(livers, xx, yy, mode)[0]
            ly = p(livers, xx, yy, mode)[1]
            if ((l[xx+lx][yy+ly] == 0) or (l[xx+lx][yy+ly] == 10)) and (l[xx][yy]%2 == 0)and (l[xx][yy] >0):
                if ((l[xx + lx][yy + ly] == 10)):
                    l[xx + lx][yy + ly] = l[xx][yy] - 1
                    l[xx][yy] = 10
                elif ((l[xx + lx][yy + ly] == 16)):
                    l[xx + lx][yy + ly] = l[xx][yy] - 1
                    l[xx][yy] = 16
                else:
                    l[xx+lx][yy+ly] = l[xx][yy]-1
                    l[xx][yy] = 0
            if (l[xx][yy] == 16):
                lava(l, xx, yy)
                l[xx][yy] = 16

def rnd(l, tp):
    x = len(l[0])
    y = len(l)
    for yy in range(0, y):
        for xx in range(0, x):
            if(l[xx][yy] == 0):
                if(random.randint(0, 14)==0):
                    if (tp == 0):
                        l[xx][yy] = 0
                    else:
                        l[xx][yy] = tp*2-1

def keys(l):
    global sizey, sizex, cent, type, mode, toolsize, sz
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        cent[0] += 1
    if keys[pygame.K_p]:
        sz += 1
    if keys[pygame.K_o]:
        sz -= 1
    if keys[pygame.K_a]:
        cent[0] -= 1
    if keys[pygame.K_w]:
        cent[1] -= 1
    if keys[pygame.K_s]:
        cent[1] += 1
    if keys[pygame.K_r]:
        rnd(l, type)
    if keys[pygame.K_f]:
        fill(l, type)
    if keys[pygame.K_c]:
        mode = 0
    if keys[pygame.K_v]:
        mode = 1
    if keys[pygame.K_1]:
        type = 1
    elif keys[pygame.K_2]:
        type = 2
    elif keys[pygame.K_3]:
        type = 3
    elif keys[pygame.K_4]:
        type = 4
    elif keys[pygame.K_5]:
        type = 5
    elif keys[pygame.K_6]:
        type = 6
    elif keys[pygame.K_7]:
        type = 7
    elif keys[pygame.K_8]:
        type = 8
    elif keys[pygame.K_9]:
        type = 9
    elif keys[pygame.K_0]:
        type = 0
    if keys[pygame.K_z]:
        l = None
        l = create(sizex, sizey)
        bord(l, sizex-1, sizey-1)
    for i in pygame.event.get():
        if i.type == pygame.MOUSEBUTTONDOWN:
            if i.button == 4:
                toolsize += 1
            if i.button == 5:
                toolsize -= 1

def add(l, pos, sz, type, rnd):
    x = random.randint(-rnd//2, rnd-(rnd//2))
    y = random.randint(-rnd//2, rnd-(rnd//2))
    if (type == 0):
        for xx in range(0, rnd):
            for yy in range(0, rnd):
                l[int(pos[0] / sz) + xx - (rnd // 2)][int(pos[1] / sz) + yy - (rnd // 2)] = 0
    elif iff(type, [4, 6, 9]):
        for xx in range(0, rnd):
            for yy in range(0, rnd):
                if (l[int(pos[0] / sz) + xx - (rnd//2)][int(pos[1] / sz) + yy - (rnd//2)] == 0):
                    l[int(pos[0] / sz) + xx - (rnd//2)][int(pos[1] / sz) + yy - (rnd//2)] = type * 2 - 1
    else:
        if (l[int(pos[0] / sz) + x][int(pos[1] / sz) + y] == 0):
            l[int(pos[0] / sz) + x][int(pos[1] / sz) + y] = type * 2 - 1

def fnt(x, y, c):
    return c[(x+y)%2]

def drw(l, sz):
    x = len(l[0])
    y = len(l)
    for yy in range(0, y):
        for xx in range(0, x):
            global cent
            if (xx == cent[0]) and (yy == cent[1])and(mode == 1):
                pygame.draw.rect(sc, (255, 255, 255), (xx * sz, yy * sz, sz, sz))
            else:
                if (l[xx][yy]>0):
                    color = (l[xx][yy] + l[xx][yy]%2)//2-1
                    if (color>len(colors)-1):
                        color = len(colors)-1
                    pygame.draw.rect(sc, (colors[color][(xx + yy)%2]), (xx*sz,yy*sz, sz, sz))
                else:
                    global bg_c
                    pygame.draw.rect(sc, (fnt(xx, yy, bg_c)), (xx * sz, yy * sz, sz, sz))

def bord(l, sx, sy):
    for x in range(0, sx):
        l[x][0]=-1
        l[x][sy] = -1
    for y in range(0, sy):
        l[0][y]=-1
        l[sx][y] = -1

livers = create(sizex, sizey)
bord(livers, sizex-1, sizey-1)
#rnd(livers)

keep_going = True

while keep_going:
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            keep_going = False
    sc.fill((0, 0, 0))
    if (pygame.mouse.get_pressed()[0]):
        for x in range(0, intense):
            add(livers, pygame.mouse.get_pos(), sz, type, 3)
    keys(livers)
    check1(livers)
    check2(livers)
    drw(livers, sz)
    pygame.draw.rect(sc, (0, 0, 0), (0, 0, sizex*sz, sizey*sz), 10)
    pygame.display.update()
    time.sleep(0.05)
pygame.quit()
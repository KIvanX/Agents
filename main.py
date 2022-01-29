
import pygame as pg
from agent import Agent

w, h = 800, 600

pg.init()
window = pg.display.set_mode((w, h))
clock = pg.time.Clock()


sr_speed, rad = 1, 50
castles = [(200, 200), (300, 500)]
mines = [(w-200, h-200), (500, 500)]

agents = []
for i in range(300):
    agents.append(Agent(window, w, h, sr_speed, rad, castles, mines))


game, move_c, move_m = True, -1, -1
while game:
    clock.tick(0)
    pg.display.set_caption('Роевой интеллект   FPS:'+str(int(clock.get_fps())))
    window.fill((0, 130, 0))

    if move_c != -1:
        castles[move_c] = pg.mouse.get_pos()
    if move_m != -1:
        mines[move_m] = pg.mouse.get_pos()

    for xC, yC in castles:
        pg.draw.circle(window, (200, 200, 200), (xC, yC), 10)
    for xM, yM in mines:
        pg.draw.circle(window, (250, 250, 0), (xM, yM), 10)

    for a in agents:
        a.run()
        a.set_dist()
        a.is_made_task()
        a.voice(agents)
        a.drow()

    pg.display.flip()

    for e in pg.event.get():
        if e.type == pg.QUIT:
            game = False

        if e.type == pg.MOUSEBUTTONDOWN:
            x, y = pg.mouse.get_pos()
            for i in range(len(castles)):
                if (x - castles[i][0]) ** 2 + (y - castles[i][1]) ** 2 < 100:
                    move_c = i
            for i in range(len(mines)):
                if (x - mines[i][0]) ** 2 + (y - mines[i][1]) ** 2 < 100:
                    move_m = i

        if e.type == pg.MOUSEBUTTONUP:
            move_c, move_m = -1, -1


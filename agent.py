from random import randint, random
import pygame as pg
import math


class Agent:
    def __init__(self, window, w, h, sr_speed, rad, castles, mines):
        self.window = window
        self.w, self.h = w, h
        self.sr_speed, self.rad = sr_speed, rad
        self.castles, self.mines = castles, mines

        self.x, self.y = randint(0, self.w), randint(0, self.h)
        self.speed = sr_speed * randint(70, 130) / 100
        self.mission = 1
        self.angle = randint(0, 360)
        self.dist_M, self.dist_C = 1000, 1000

    def run(self):
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y -= math.sin(math.radians(self.angle)) * self.speed
        self.angle += (0.5 - random())*3

        if self.x < 0:
            self.x, self.angle = 0, 180 - self.angle

        if self.x >= self.w:
            self.x, self.angle = self.w - 1, 180 - self.angle

        if self.y < 0:
            self.y, self.angle = 0, -self.angle

        if self.y >= self.h:
            self.y, self.angle = self.h - 1, -self.angle

    def drow(self):
        pg.draw.circle(self.window, (200, 200, 0), (self.x, self.y), 2)

    def voice(self, agents):
        for a in agents:
            if not(self is a) and math.sqrt((self.y - a.y) ** 2 + (self.x - a.x) ** 2) <= self.rad:
                if a.dist_M > self.dist_M + self.rad:
                    pg.draw.line(self.window, (0, 0, 0), (a.x, a.y), (self.x, self.y))
                    a.dist_M = self.dist_M + self.rad
                    if a.mission == 1:
                        a.angle = self._angle_to(a.x, a.y, self.x, self.y)

                if a.dist_C > self.dist_C + self.rad:
                    pg.draw.line(self.window, (0, 0, 0), (a.x, a.y), (self.x, self.y))
                    a.dist_C = self.dist_C + self.rad
                    if a.mission == 2:
                        a.angle = self._angle_to(a.x, a.y, self.x, self.y)

    def is_made_task(self):
        for xC, yC in self.castles:
            if math.sqrt((xC - self.x)**2 + (yC - self.y)**2) <= 12:
                self.dist_C = 0
                if self.mission == 2:
                    self.angle = (self.angle + 180) % 360
                    self.mission = 1

        for xM, yM in self.mines:
            if math.sqrt((xM - self.x)**2 + (yM - self.y)**2) < 10:
                self.dist_M = 0
                if self.mission == 1:
                    self.angle = (self.angle + 180) % 360
                    self.mission = 2

    def set_dist(self):
        self.dist_M += 1
        self.dist_C += 1

    def _angle_to(self, x, y, x1, y1):
        x1 = x1 + 0.001 if x1 == x else x1
        if x < x1:
            if y < y1:
                return -math.degrees(math.atan(abs(y1 - y) / abs(x1 - x)))
            else:
                return math.degrees(math.atan(abs(y1 - y) / abs(x1 - x)))
        else:
            if y < y1:
                return 180 + math.degrees(math.atan(abs(y1 - y) / abs(x1 - x)))
            else:
                return 180 - math.degrees(math.atan(abs(y1 - y) / abs(x1 - x)))

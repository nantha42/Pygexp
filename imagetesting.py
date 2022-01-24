import pygame as py
import time 
import random as rd
import numpy as np
from numpy import array as array
py.init()
screen_width,screen_height = 600,700

class Display:
    def __init__(self):
        self.win = py.display.set_mode((screen_width,screen_height),py.DOUBLEBUF| py.RESIZABLE,32)
        py.display.set_caption("Experimenting")
        self.clock = py.time.Clock()
        self.done = False
        self.planets = []
        self.dt = 1 
        self.dot_surface = py.Surface((2,2)) 
        py.draw.circle(self.dot_surface,(255,255,255),(1,1),1,1)
        print(py.font.get_fonts())
        self.bg = py.Surface((screen_width,screen_height))
        self.bg.fill((30,0,40))
        
        pass
            
    def eventhandler(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                exit()

            if event.type == py.KEYDOWN:
                if event.key == py.K_a:
                    pass

            if event.type == py.KEYUP:
                if event.key == py.K_a:
                    pass

            if event.type == py.MOUSEBUTTONDOWN:
                x,y = py.mouse.get_pos()
                z = rd.randint(-20,20)
                pos = np.array([x,y,z],dtype=np.float32)
                vel = np.array([rd.randint(-1,1)*0.1,rd.randint(-1,1)*0.1,rd.randint(-1,1)*0.1] )
                self.planets.append([pos,vel,len(self.planets)])
                print(len(self.planets))
    
    def update(self):
        dt = self.dt
        for i in range(len(self.planets)):
            p = self.planets[i] 
            for j in range(i,len(self.planets)):
                g = self.planets[j]
                if g[2] != p[2]:
                    p1,p2 = g[0],p[0]                 
                    d = (p1-p2)
                    force = 0.001*d/(np.linalg.norm(d)**2)
                    p[1] += force*dt
                    g[1] -= force*dt 
                    nans = np.isnan(p[1])  
                    p[1][nans] = 0.0
                    nans = np.isnan(g[1])
                    g[1][nans] = 0.0
        for i in self.planets:
            i[0] += i[1]*dt

    def draw(self):
        self.win.blit(self.bg,(0,0))
        for p in self.planets:
            try:
                x,y,_ = p[0]
                self.win.blit(self.dot_surface,[x,y])
#                py.draw.circle(self.win,(255,255,255),[x,y],1,1)
            except:
                print(p[0])

    def run(self):
        while not self.done:
            self.eventhandler()
            self.draw()
            self.update()
            py.display.update()


if __name__=='__main__':
    d = Display()
    d.run()

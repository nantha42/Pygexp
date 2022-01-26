import pygame as py
import time 
import random as rd
import numpy as np
import math
from numpy import array as array
py.init()
screen_width,screen_height = 1500,700

FOV = 90

def camera_view(vector, points):
    """
        the vector pointing direction is the camera angle and the point ends is 
        where the camera capture screen and from that place frustrum starts. Its 
        a triangular ratio. 
    """
    pass

def count_elements(x):
    ans = 1
    for i in range(len(x.shape)):
       ans *= x.shape[i] 
    return ans 

def ptrin(x):
    print(x)
    time.sleep(1)

def project_polygon(polygon):
    projected_points = []
    for point in polygon:
        x_angle = math.atan2(point[0], point[2])
        y_angle = math.atan2(point[1], point[2])
        x = x_angle / math.radians(FOV) * screen_width + screen_height // 2
        y = y_angle / math.radians(FOV) * screen_width + screen_width // 2
        projected_points.append([x, y])
    return projected_points

class Display:
    def __init__(self):
        self.win = py.display.set_mode((screen_width,screen_height),py.DOUBLEBUF| py.RESIZABLE,32)
        py.display.set_caption("Experimenting")
        self.clock = py.time.Clock()
        self.done = False
        self.dt = 0.1 
        r = 64 
        self.rad =  r
        self.dot_surface = py.Surface((r,r)) 
        self.dot_surface1 = py.Surface((r,r))
        py.draw.circle(self.dot_surface,(1,1,1),(r//2,r//2),r//2,r//2)
        py.draw.circle(self.dot_surface,(255,215,0),(r//2,r//2),1,1)
        
        py.draw.circle(self.dot_surface1,(1,1,1),(r//2,r//2),r//2,r//2)
        py.draw.circle(self.dot_surface1,(225,220,225),(r//2,r//2),1,1)
        self.bg = py.Surface((screen_width,screen_height))
        self.bg.fill((30,0,40))
        self.font = py.font.Font("freesansbold.ttf",15)
        self.lasttime = time.time() 
        self.planets = np.array([])
        self.planets_vel= np.array([])
        self.planets_mass = np.array([])
        self.filterstore = None
        self.fps_count = 0
        self.fps = 0
        self.fps_sum = 0
        self.pause = False
        self.index = 0

        pass
            
    def eventhandler(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                exit()

            if event.type == py.KEYDOWN:
                if event.key == py.K_a:
                    self.pause = True
                    pass

            if event.type == py.KEYUP:
                if event.key == py.K_a:
                    self.pause = False
                    pass

            if event.type == py.MOUSEBUTTONDOWN:
                x,y = py.mouse.get_pos()
                ang = np.radians(rd.randint(0,360))
                u,v = np.cos(ang),np.sin(ang) 
                dis = rd.randint(0,30) 
                x += u*dis
                y += v*dis

                x-=self.rad//2
                y-=self.rad//2
                dy = rd.randint(-10,10)
                z = 0
                x,y,z = x*1.0,(y)*1.0,(z+dy)*1.0

                pos = [x,y,z]
                vel = [rd.randint(-2,2)*0.1,rd.randint(-2,2)*0.1,rd.randint(-1,1)*0.1]
                mass = rd.randint(1,10000)

                self.planets = self.planets.tolist()
                self.planets_vel= self.planets_vel.tolist()
                self.planets_mass = self.planets_mass.tolist()

                self.planets.append(pos)
                self.planets_vel.append(vel)
                self.planets_mass.append(mass)

                print(len(self.planets))

                self.planets = np.array(self.planets) 
                self.planets_vel = np.array(self.planets_vel) 
                self.planets_mass= np.array(self.planets_mass) 
    
    
    def update(self):
        dt = self.dt
        G = 0.010
        r = -self.planets.reshape([-1,1,3]) + self.planets.reshape([1,-1,3])
        normed = np.linalg.norm(r,axis=2)
        squared = (normed*normed)
        #triu = np.triu(np.arange(count_elements(squared)).reshape(squared.shape))
        filtered = squared
        nans = np.isnan(filtered)
        filtered[nans] = 0
        filtered[filtered == np.inf] = 0
        filtered[filtered == -np.inf] = 0
        unit = G*(r/filtered[:,:,np.newaxis] )
        unit[np.isnan(unit)] = 0
        unit[unit== np.inf] = 0
        unit[unit == -np.inf] = 0

        self.filterstore = unit.sum(axis=1)
        try:
            self.planets_vel += unit.sum(axis=1)*dt
            self.planets += self.planets_vel*dt
            self.filterstore = self.planets
            #time.sleep(1)
            pass
        except:
            pass

    def update1(self):
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
        plotted = project_polygon(self.planets)
#        for p in plotted:
        for p in self.planets:
            x,y,_ = p 
            if x!= np.nan and y != np.nan: 
                toss = rd.randint(0,1)
                if toss == 1:
                    self.win.blit(self.dot_surface,[x,y],special_flags=py.BLEND_RGB_ADD)
                else:
                    self.win.blit(self.dot_surface1,[x,y],special_flags=py.BLEND_RGB_ADD)
#            py.draw.circle(self.win,(255,255,255),[x,y],1,1)
            pass
        #surf = self.font.render("fps: "+str(1/self.dt),True,(255,255,255),(0,0,0))
        surf = self.font.render("fps: "+str(int(self.clock.get_fps())),True,(255,0,5),(0,0,0))
        self.win.blit(surf,(0,0))

    def run(self):
        while not self.done:
            self.eventhandler()
            self.draw()
            py.display.update()
            if not self.pause:
                self.update()
            nowtime = time.time()
            self.dt = 10*(nowtime - self.lasttime )
            self.lasttime = nowtime
            self.calculate_fps()
            self.clock.tick(120)
            self.index+=1
    
    def calculate_fps(self):
        if self.fps_count ==200:
            self.fps_count = 1
            self.fps_sum = 1/self.dt
        else:
            self.fps_sum += 1/self.dt
            self.fps_count+=1

        self.fps = self.fps_sum/self.fps_count

if __name__=='__main__':
    d = Display()
    d.run()

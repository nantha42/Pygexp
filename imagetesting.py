import pygame as py
import pickle
import time 
import random as rd
import numpy as np
import math
from numpy import array as array
py.init()
screen_width,screen_height = 1500,700

FOV = 90
WHITE = (255,255,255)

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

def norm(x):
    """Returns normal of a nd array""" 
    return x/np.linalg.norm(x)

def arr(x):
    return np.array(x,dtype=np.float32)

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
        self.dot_selected_surface = py.Surface((r,r))
        py.draw.circle(self.dot_surface,(1,1,1),(r//2,r//2),r//2,r//2)
        py.draw.circle(self.dot_surface,(255,215,0),(r//2,r//2),1,1)
        
        py.draw.circle(self.dot_surface1,(1,1,1),(r//2,r//2),r//2,r//2)
        py.draw.circle(self.dot_surface1,(225,220,225),(r//2,r//2),1,1)


        py.draw.circle(self.dot_selected_surface,(1,1,1),(r//2,r//2),r//2,r//2)
        py.draw.circle(self.dot_selected_surface,(225,220,225),(r//2,r//2),2,2)



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
        self.spawn = False
        self.cluster_particles = 50
        self.G = 0.010
        self.mass_selected = 1
        self.dark = False
        self.zoom = 1
        self.camera = np.array([1.0,1.0])
        self.scroll_enabled = False
        self.scroll_start = np.array([screen_width/2,screen_height/2])
        self.center = np.array([0.0,0.0])
        self.origin = np.array([0.0,0.0])
        self.selected_planet = -1

        self.drag = arr([0,0])
        self.trails = []
        self.trails_enabled = False


        self.launch_vector = arr([0,0,0])
        self.launch_enabled = False
        self.launch_point = arr([0,0]) 
        self.center_displacement = arr([0,0])

        pass
            
    def eventhandler(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                exit()

            if event.type == py.KEYDOWN:
                if event.key == py.K_a:
                    self.pause = True
                    pass
                if event.key == py.K_s:
                    self.save_particles()

                if event.key == py.K_l:
                    self.load_particles()
                if event.key == py.K_t:
                    self.trails_enabled = not self.trails_enabled

                if event.key == py.K_1:
                    self.mass_selected = 100

                if event.key == py.K_2:
                    self.mass_selected = 200
                if event.key == py.K_3:
                    self.mass_selected = 300
                if event.key == py.K_4:
                    self.mass_selected = 400
                if event.key == py.K_5:
                    self.mass_selected = 500
                if event.key == py.K_6:
                    self.mass_selected = 600
                if event.key == py.K_7:
                    self.mass_selected = 700
                if event.key == py.K_8:
                    self.mass_selected = 800
                if event.key == py.K_9:
                    self.mass_selected = 900
                if event.key == py.K_0:
                    self.mass_selected = 1 
                if event.key == py.K_d:
                    self.dark = not self.dark
                if len(self.planets) > 0:
                    if event.key == py.K_UP:
                        self.selected_planet += 1
                        self.selected_planet %= len(self.planets)
                    if event.key == py.K_DOWN:
                        self.selected_planet -= 1
                        self.selected_planet %= len(self.planets)

            if event.type == py.KEYUP:
                if event.key == py.K_a:
                    self.pause = False

                if event.key == py.K_s:
                    self.spawn = False
                    pass

            if event.type == py.MOUSEBUTTONDOWN:
                if(event.button == 1):
                    self.spawn_process1()
                    self.launch_enabled = True
                    self.launch_point= arr(py.mouse.get_pos())

                if event.button>=4:
                    x,y = py.mouse.get_pos() 
                    x+= self.rad//2
                    y+= self.rad//2
                    w,h = screen_width,screen_height
                    if np.linalg.norm(self.drag) == 0.0:
                        self.center = np.array([self.origin[0] + x/self.zoom, self.origin[1] + y/self.zoom],dtype=np.float32)
                      
                    if(event.button>= 4 and event.button%2==0):
                        self.zoom *= 2 
                        self.center_displacement = (-arr([x,y]) + arr([w/2,h/2]))/self.zoom
                    elif(event.button >= 4 and event.button):
                        self.zoom *= .5 
                        self.center_displacement = (-arr([x,y]) + arr([w/2,h/2]))/self.zoom
                    else:
                        self.center_displacement = arr([0,0])

                if event.button == 3:
                    self.scroll_enabled = True 
                    self.scroll_start = np.array(py.mouse.get_pos(),dtype=np.float32)
                    self.selected_planet = -1

            if event.type == py.MOUSEBUTTONUP:
                if event.button == 1:
                    self.launch_enabled = False
                    x,y = self.launch_vector
                    self.planets_vel[-1] = arr([x,y,0])/self.zoom
                     
                if event.button == 3:
                    self.scroll_enabled = False
                    x,y = py.mouse.get_pos() 
                    if np.linalg.norm(self.drag) == 0.0:
                        self.center = np.array([self.origin[0] + x/self.zoom, self.origin[1] + y/self.zoom],dtype=np.float32)
                    else:
                        self.center -=  self.drag
            
            if event.type == py.MOUSEMOTION:
                if self.scroll_enabled:
                    cur_pos = np.array(py.mouse.get_pos(),dtype=np.float32)

        
        if self.launch_enabled: 
            cx,cy = py.mouse.get_pos()
            dv = self.launch_point - py.mouse.get_pos()
            self.launch_vector = dv 

        if self.spawn:
            self.spawn_process()

        if self.scroll_enabled:
            cpos = py.mouse.get_pos()
            self.drag = (cpos-self.scroll_start)/self.zoom
        else:
            self.drag = arr([0.0,0.0])

    def update(self):
        dt = self.dt
        r = -self.planets.reshape([-1,1,3]) + self.planets.reshape([1,-1,3])
        normed = np.linalg.norm(r,axis=2)
        squared = (normed*normed)
        quaded = (normed*normed*normed*normed)
        #triu = np.triu(np.arange(count_elements(squared)).reshape(squared.shape))
        filtered = squared
        nans = np.isnan(filtered)
        filtered[nans] = 0
        filtered[filtered == np.inf] = 0
        filtered[filtered == -np.inf] = 0
        unit = self.G*(r/filtered[:,:,np.newaxis] )
        
        #filtered = quaded
        #nans = np.isnan(filtered)
        #filtered[nans] = 0
        #filtered[filtered == np.inf] = 0
        #filtered[filtered == -np.inf] = 0
        #unit1 = -(self.G**2)*(r/filtered[:,:,np.newaxis] )
 
        unit[np.isnan(unit)] = 0
        unit[unit== np.inf] = 0
        unit[unit == -np.inf] = 0
        unit = self.planets_mass.reshape([1,-1,1])*unit 

        #unit1[np.isnan(unit1)] = 0
        #unit1[unit1== np.inf] = 0
        #unit1[unit1 == -np.inf] = 0
        #unit1 = self.planets_mass.reshape([1,-1,1])*unit1
        
        #self.filterstore = unit.sum(axis=1)
        try:
            #self.planets_vel += (unit.sum(axis=1) + unit1.sum(axis=1))*dt
            self.planets_vel += unit.sum(axis=1)*dt
            self.planets += self.planets_vel*dt
            for i in range(len(self.trails)):
                if len(self.trails[i])>10:
                    self.trails[i].pop(0)
                self.trails[i].append(self.planets[i].tolist())
            #self.filterstore = self.planets
            #time.sleep(1)
            pass
        except:
            pass

    def draw(self):
        self.win.blit(self.bg,(0,0))
        plotted = project_polygon(self.planets)
#       for p in plotted:
        index = 0 
        for i in range(len(self.planets)):
            p = self.planets[i]
            x,y,_ = p 
            if x!= np.nan and y != np.nan: 
                toss = rd.randint(0,1)
                x,y = (x-self.origin[0])*self.zoom, (y-self.origin[1])*self.zoom
                #mx,my = self.scroll_start
                #x,y = (screen_width/2)*(1-self.zoom) + x*self.zoom,(screen_height/2)*(1-self.zoom) + y*self.zoom
                #x,y = x+(-self.scroll_start[0]),y+(-self.scroll_start[1])
                if index == self.selected_planet:
                    self.win.blit(self.dot_selected_surface,[x,y],special_flags=py.BLEND_RGB_ADD)
                else:
                    if toss == 1:
                        self.win.blit(self.dot_surface,[x,y],special_flags=py.BLEND_RGB_ADD)
                    else:
                        self.win.blit(self.dot_surface1,[x,y],special_flags=py.BLEND_RGB_ADD)
                if self.launch_enabled and i == len(self.planets)-1:
                    ep = [x+self.rad//2,y+self.rad//2] + self.launch_vector
                    py.draw.line(self.win,WHITE,[x+self.rad//2,y+self.rad//2],ep,1)

            index+=1
            if self.trails_enabled:
                trailed = self.trails[i]
                transformed = []
                for t in trailed:
                    x,y,_ = t
                    x,y = (x-self.origin[0])*self.zoom, (y-self.origin[1])*self.zoom
                    x+=self.rad//2
                    y+=self.rad//2
                    transformed.append([x,y])
                if len(transformed)>1:
                    py.draw.lines(self.win,WHITE,False,transformed,1)


        surf = self.font.render("fps: "+str(int(self.clock.get_fps())),True,(255,0,5),(0,0,0))
        self.win.blit(surf,(0,0))
        surf = self.font.render("Zoom : "+str(self.zoom),True,(255,255,255),(0,0,0))
        self.win.blit(surf,(0,20))
    
    def spawn_process(self):
        center = np.array([screen_width//2, screen_height//2,rd.randint(-10,10)],dtype=np.float32)
        for i in range(2): 
            if i!=0:
                p1 = np.array([rd.randint(-50,50) ,rd.randint(-50,50),1],dtype=np.float32)
            else:
                p1 = np.array([0,0,0],dtype=np.float32)
            vy = -(p1[0] + p1[2])/p1[1] 
            vel = norm(np.array([1,vy,1],dtype=np.float32))
            r = np.linalg.norm(p1) 
            speed = np.sqrt(self.G/r) 
            vel *= speed
            p1 += center
            mass = np.random.randint(1,1000)
            self.append_planet(p1,vel,mass)
    
    def recenter(self,coord):
        cx,cy = coord 
        mx,my = py.mouse.get_pos()
        w,h = screen_width,screen_height
        ox = cx - (w/2)/self.zoom 
        oy = cy - (h/2)/self.zoom
        self.origin = np.array([ox,oy],dtype=np.float32) 

    def recenter1(self,coord):
        cx,cy = coord 
        mx,my = py.mouse.get_pos()
        w,h = screen_width,screen_height
        ox = cx - (w/2)/self.zoom 
        oy = cy - (h/2)/self.zoom
        self.origin = np.array([ox,oy],dtype=np.float32) + self.center_displacement

        

    def spawn_process1(self):
        dx,dy = py.mouse.get_pos()
        dx-=self.rad//2
        dy-=self.rad//2
        dx,dy = dx/self.zoom, dy/self.zoom
        x,y = self.origin[0]+dx,self.origin[1] + dy
        pos = [x,y,rd.randint(-10,10)]
        vel = [0,0,0] 
        sign = -1 if self.dark else 1
        mass = sign*(self.mass_selected + rd.randint(1,10))
        self.append_planet(pos,vel,mass)
        self.trails.append([self.planets[-1]])
 
#    def spawn_process1(self):
#        dx,dy = py.mouse.get_pos()
#        dx-=self.rad//2
#        dy-=self.rad//2
#        x = (dx - (1-self.zoom)*(screen_width/2) )/self.zoom
#        y = (dy - (1-self.zoom)*(screen_height/2) )/self.zoom
#        ang = np.radians(rd.randint(0,360))
#        u,v = np.cos(ang),np.sin(ang) 
#        #if self.first_spawned:
#        #    dis = rd.randint(0,30) 
#        #    x += u*dis
#        #    y += v*dis
#
##        x-=self.rad//2
##        y-=self.rad//2
#        dy = rd.randint(-10,10)
#        z = 0
#        x,y,z = x*1.0,(y)*1.0,(z+dy)*1.0
#
#        pos = [x,y,z]
#        vel = [rd.randint(-2,2)*0.1,rd.randint(-2,2)*0.1,rd.randint(-1,1)*0.1]
#        sign = -1 if self.dark else 1
#        mass = sign*(self.mass_selected + rd.randint(1,10))
#        self.append_planet(pos,vel,mass)
    
    def append_planet(self,p,v,m=1):
        self.planets = self.planets.tolist()
        self.planets_vel= self.planets_vel.tolist()
        self.planets_mass = self.planets_mass.tolist()

        self.planets.append(p)
        self.planets_vel.append(v)
        self.planets_mass.append(m)

        self.planets = np.array(self.planets,dtype=np.float32) 
        self.planets_vel = np.array(self.planets_vel,dtype=np.float32) 
        self.planets_mass= np.array(self.planets_mass,dtype=np.float32) 
    
    def save_particles(self):
        stats = {"pos":self.planets,"vel":self.planets_vel,"mass":self.planets_mass} 
        with open('saved/mypickle.pickle', 'wb') as f:
            pickle.dump(stats, f)

    def load_particles(self):
        with open("saved/mypickle.pickle",'rb') as f:
            stats = pickle.load(f)
            self.planets = stats["pos"]
            self.planets_vel = stats["vel"]
            self.planets_mass = stats["mass"]
            self.trails = [[] for i in range(len(self.planets))]

    def run(self):
        while not self.done:
            self.eventhandler()
            if self.selected_planet > -1:
                starpoint = self.planets[self.selected_planet]
                sx,sy,_ = starpoint
                self.recenter(arr([sx,sy]))
            else:
                self.recenter(self.center - self.drag)
            self.draw()
            py.display.update()
            if not self.pause and not self.launch_enabled:
                self.update()
            nowtime = time.time()
            self.dt = 10*(nowtime - self.lasttime )
            self.lasttime = nowtime
            self.calculate_fps()
            self.clock.tick(60)
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

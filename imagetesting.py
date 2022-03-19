import pygame as py
import pickle
import time 
import random as rd
import numpy as np
import math
from numpy import array as array
from utils import *
from compute_faster import *
from barneshut import *

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

class Display:
    def __init__(self):
        self.win = py.display.set_mode((screen_width,screen_height),py.DOUBLEBUF| py.RESIZABLE,32)
        py.display.set_caption("Experimenting")
        self.clock = py.time.Clock()
        self.done = False
        self.dt = 0.1 
        self.sdt = self.dt


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
        self.zoom = 10.0
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
        self.create_surfaces() 
        self.zoomed_in_point = None
        self.prev_zoom = 1
        self.graph_factor = 1.0
        self.bodies = []
        self.fast_compute= False

        pass

    def create_surfaces(self):
        r = int(max(min(64*self.zoom,512),64))
        sz = int(max(min(self.zoom,64),1))
        self.rad = r
        self.dot_surface = py.Surface((r,r)) 
        self.dot_surface1 = py.Surface((r,r))
        self.x_mark = py.Surface((16,16))

        self.dot_selected_surface = py.Surface((r,r))
        py.draw.circle(self.dot_surface,(1,1,1),(r//2,r//2),r//2,r//2)
        py.draw.circle(self.dot_surface,(255,215,0),(r//2,r//2),sz,sz)
        
        py.draw.circle(self.dot_surface1,(1,1,1),(r//2,r//2),r//2,r//2)
        py.draw.circle(self.dot_surface1,(225,220,225),(r//2,r//2),sz,sz)


        py.draw.circle(self.dot_selected_surface,(1,1,1),(r//2,r//2),r//2,r//2)
        py.draw.circle(self.dot_selected_surface,(225,220,225),(r//2,r//2),sz,sz)
        self.surfaces = {"star":self.dot_surface, "starG":self.dot_surface1, "star_control":self.dot_selected_surface}
        self.recalculated_surface = dict(self.surfaces)
        py.draw.line(self.x_mark,(255,255,255),[0,0],[16,16],1)
        py.draw.line(self.x_mark,(255,255,255),[0,16],[16,0],1)


        self.graph_line_v = py.Surface((1,screen_height))
        self.graph_line_h = py.Surface((screen_width,1)) 
        py.draw.line(self.graph_line_v,(10,10,10),[0,0],[0,screen_height],1)
        py.draw.line(self.graph_line_h,(10,10,10),[0,0],[screen_width,0],1)

            
    def eventhandler(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                exit()

            if event.type == py.KEYDOWN:
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
                if event.key == py.K_a:
                    self.mass_selected = 10000
                if event.key == py.K_b:
                    self.mass_selected = 100000 
                if event.key == py.K_c:
                    self.mass_selected = 10000000000
                if event.key == py.K_f:
                    self.fast_compute = not self.fast_compute

                if event.key == py.K_o:
                    self.center = arr([0,0])
                if event.key == py.K_LEFT:
                    self.sdt *= 0.1 
                if event.key == py.K_RIGHT:
                    self.sdt *= 10 
                    self.sdt = min(0.1,self.sdt)


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
                if event.key == py.K_p:
                    self.pause =  not self.pause 

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
                    self.zoomed_in_point = arr([x,y])
                    w,h = screen_width,screen_height
                    if np.linalg.norm(self.drag) == 0.0:
                        self.center = np.array([self.origin[0] + x/self.zoom, self.origin[1] + y/self.zoom],dtype=np.float32)
                      
                    if(event.button>= 4 and event.button%2==0):
                        self.prev_zoom = self.zoom
                        self.zoom *= 1.2 
                        self.recalculate_surfaces()
                        self.update_graph()
                    elif(event.button >= 4 and event.button):
                        self.prev_zoom = self.zoom
                        #self.zoom *= .9 
                        self.zoom *= 1/(1.2) 
                        self.update_graph()
                        self.recalculate_surfaces()
                    else:
                        self.zoomed_in_point = None
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
    
    def compute_fast(self):
        root_quad = Quad(-5e5,-5e5,1e6)
        root = Barneshut(root_quad)
        timer = Timer("Tree") 
        for b in self.bodies:
            body = Body()
            body.copy(b)
            root.insert(body)

        for i in range(len(self.bodies)):
            b = self.bodies[i]
            b.force = np.array([0.0,0.0,0.0])
            root.update_force(b) 
            self.planets_vel[i] +=  b.force*self.dt

        for i in range(len(self.bodies)):
            b = self.bodies[i]
            b.x += self.planets_vel[i][0] * self.dt
            b.y += self.planets_vel[i][1] * self.dt
            self.planets[i][0] = b.x
            self.planets[i][1] = b.y

#        for i in range(len(self.planets)):
#            p = self.planets[i] 
#            v = self.planets_vel[i]
#            m = self.planets_mass[i]
#            body = Body(p[0],p[1],m)
#            root.insert(body)
#        timer.elapsed()
            
        #computer = Compute_fast(self.planets,self.planets_vel,self.planets_mass) 
        #computer.update() 
        #self.planets = computer.pos
        #self.planets_vel = computer.vel
        #self.planets_masses = computer.masses


    def compute_accurate(self):
        dt = self.sdt
        r = -self.planets.reshape([-1,1,3]) + self.planets.reshape([1,-1,3])
        normed = np.linalg.norm(r,axis=2)
        squared = (normed*normed)
        quaded = (normed*normed*normed*normed)
        filtered = squared
        nans = np.isnan(filtered)
        filtered[nans] = 0
        filtered[filtered == np.inf] = 0
        filtered[filtered == -np.inf] = 0
        unit = self.G*(r/filtered[:,:,np.newaxis] )
        

        unit[np.isnan(unit)] = 0
        unit[unit== np.inf] = 0
        unit[unit == -np.inf] = 0
        unit = self.planets_mass.reshape([1,-1,1])*unit 
       
        try:
            self.planets_vel += unit.sum(axis=1)*dt
            self.planets += self.planets_vel*dt
            for i in range(len(self.trails)):
                self.bodies[i].x = self.planets[i][0]
                self.bodies[i].y = self.planets[i][1]
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
        for i in range(len(self.planets)):
            p = self.planets[i]
            boddy = self.bodies[i]
            x,y = boddy.x,boddy.y
#            x,y,_ = p
            if x!= np.nan and y!= np.nan:
                toss = rd.randint(0,1)
                converted_point = self.space_to_screen(arr([x,y]))
                x,y = converted_point
                if i == self.selected_planet:
                    self.win.blit(self.surfaces["star_control"],[x,y],special_flag=py.BLEND_RGB_ADD)   
                else:
                    x -= self.rad//2
                    y -= self.rad//2
                    if toss == 1:
                        self.win.blit(self.surfaces["star"],[x,y],special_flags=py.BLEND_RGB_ADD)                     
                    else:
                        self.win.blit(self.surfaces["starG"],[x,y],special_flags=py.BLEND_RGB_ADD) 
                if self.launch_enabled and i == len(self.planets)-1:
                    ep = [x+self.rad//2,y+self.rad//2] + self.launch_vector
                    py.draw.line(self.win,WHITE,[x+self.rad//2,y+self.rad//2],ep,1)
            if self.trails_enabled:
                trailed = self.trails[i]
                transformed = []
                for t in trailed:
                    x,y,_ = t
                    x,y = self.space_to_screen(arr([x,y]))
                    transformed.append([x,y])
                if len(transformed)>1:
                    py.draw.lines(self.win,WHITE,False,transformed,1)

        self.draw_texts()
        htimer = Timer("hor")
        self.draw_horizontal_graph()
#        htimer.elapsed()
        vtimer = Timer("ver")
        self.draw_vertical_graph()
#        vtimer.elapsed()
    

    def update_graph(self):
        x,y,_ = self.screen_to_space(arr([screen_width,screen_height])) 
        nlines  = x//self.graph_factor
        if nlines > 70: 
            self.graph_factor*=10
        elif nlines < 60:
            self.graph_factor/=10
    
    def space_dx(self,x):
        return x/self.zoom
        pass
    
    def screen_dx(self, x):
        return x*self.zoom
        pass

    def draw_horizontal_graph(self):
        x,y,_ = self.screen_to_space(arr([0,0])) 
        ex,ey,_ = self.screen_to_space(arr([0,screen_height]))
        dy = int(ey - y)
        grid_height = 20 
        start = int(y - (y % grid_height))
        n = (int(ey) - start)//grid_height
        factor = 1
        while self.screen_dx(grid_height*factor) <= 10:
            factor*= 20 
        sys = []
        for i in range(start,int(ey),grid_height*factor): 
            sx,sy = self.space_to_screen(arr([0,i]))
            self.win.blit(self.graph_line_h,[0,sy],special_flags=py.BLEND_RGB_ADD)
            sys.append(sy)


    def draw_vertical_graph(self):
        x,y,_ = self.screen_to_space(arr([0,0])) 
        ex,ey,_ = self.screen_to_space(arr([screen_width,0]))
        dx = int(ex - x)
        grid_width = 20 
        start = int(x - (x % grid_width))
        n = (int(ex) - start)//grid_width 
        factor = 1
        while self.screen_dx(grid_width*factor) <= 10:
            factor*= 20 
        #print("Screen :", self.screen_dx(grid_width))
        #screen_gap = self.screen_dx(grid_width)
        #if screen_gap

        for i in range(start,int(ex),grid_width*factor): 
            sx,sy = self.space_to_screen(arr([i,0]))
            self.win.blit(self.graph_line_v,[sx,0],special_flags=py.BLEND_RGB_ADD)

    def draw1(self):
        self.win.blit(self.bg,(0,0))
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
                   self.win.blit(self.surfaces["star_control"],[x,y],special_flags=py.BLEND_RGB_ADD)
                else:
                    x -= self.rad//2 
                    y -= self.rad//2
                    if toss == 1:
                        self.win.blit(self.surfaces["star"],[x,y],special_flags=py.BLEND_RGB_ADD)
                    else:
                        self.win.blit(self.surfaces["starG"],[x,y],special_flags=py.BLEND_RGB_ADD)
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
                    x,y = x+self.rad//2, y+self.rad//2
                    transformed.append([x,y])
                if len(transformed)>1:
                    py.draw.lines(self.win,WHITE,False,transformed,1)
        self.draw_texts()


    def draw_texts(self):
        surf = self.font.render("fps: "+str(int(self.clock.get_fps())),True,(255,255,255),(30,0,40))
        self.win.blit(surf,(0,0))
        surf = self.font.render("Zoom : "+str(self.zoom),True,(255,255,255),(0,0,0))
        self.win.blit(surf,(0,20))
        surf = self.font.render("Planets: "+str(len(self.planets)),True,(255,255,255),(30,0,40))
        self.win.blit(surf,(0,40))
        mix,miy = py.mouse.get_pos()
        x = self.origin[0] + mix/self.zoom
        y = self.origin[1] + miy/self.zoom
        surf = self.font.render(f"{int(x)},{int(y)}",True,(255,255,255),(30,0,40))
        self.win.blit(surf,(mix+10,miy))
        self.win.blit(self.x_mark,(screen_width//2-8,screen_height//2-8),special_flags=py.BLEND_RGB_ADD)
   
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
    
    def space_to_screen(self,points):
        if len(points.shape) == 3: 
            screen_points = (points-self.origin)*self.zoom
            return screen_point
        else:
            x,y = points
            screen_point = [(x-self.origin[0])*self.zoom, (y-self.origin[1])*self.zoom]
            return screen_point
            

    def screen_to_space(self,point):
        x,y = point
        space_point = arr([self.origin[0] + x/self.zoom, self.origin[1] + y/self.zoom,0.0])
        return space_point 
    
    def calculate_origin(self,coord):
        x,y = coord
        w,h = screen_width,screen_height
        ox = x - (w/2)/self.zoom 
        oy = y - (h/2)/self.zoom 
        self.origin = np.array([ox,oy])

    def recenter1(self,coord):
        cx,cy = coord 
        mx,my = py.mouse.get_pos()
        w,h = screen_width,screen_height
        w,h = self.center_displacement[0], self.center_displacement[1]
        ox = cx - (w/2)/self.zoom 
        oy = cy - (h/2)/self.zoom
        #ox = cx - mx/self.zoom
        #oy = cy - my/self.zoom
        self.origin = np.array([ox,oy],dtype=np.float32) + self.center_displacement
        

    def spawn_process1(self):
        dx,dy = py.mouse.get_pos()
        #dx-=self.rad//2
        #dy-=self.rad//2
        dx,dy = dx/self.zoom, dy/self.zoom
        x,y = self.origin[0]+dx,self.origin[1] + dy
        pos = [x,y,rd.randint(-10,10)]
        vel = [0,0,0] 
        sign = -1 if self.dark else 1
        mass = sign*(self.mass_selected + rd.randint(1,10))
        self.append_planet(pos,vel,mass)
        self.trails.append([self.planets[-1]])
        body = Body(x,y,mass)
        body.id = len(self.bodies)
        self.bodies.append(body)
 
   
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
    
    def resize_surface(self,surf):
        if self.zoom>=8:
            size = [2*(self.zoom-7),(self.zoom-7)*2]
            dest_surf = py.transform.scale(surf,size)
            return surf
        else:
            return surf

    def recalculate_surfaces(self):
        self.create_surfaces()

    def run(self):
        while not self.done:
            self.eventhandler()
            self.calculate_origin(self.center - self.drag)
            self.draw()
            py.display.update()
            if not self.pause and not self.launch_enabled:
                if self.fast_compute:
                    self.compute_fast()
                else:
                    self.compute_accurate()

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

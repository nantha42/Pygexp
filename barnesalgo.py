from utils import *
import time 
from config import *

def add_bodies(b1,b2):
    tm = b1.mass + b2.mass
    ret = Body()
    com = array([0.0,0.0,0.0])
    ret.set(com,None,tm,-1)
    return ret
 
def compute_mass(root):
    if root is None:
        return 0
    elif root.body.id != -1:
        return root.body.mass
    else:
        root.body.mass = 0
        for hut in root.subhuts:
            root.body.mass += compute_mass(hut)
        
        return root.body.mass

def compute_com(root):
    if root is None:
        return array([0.0,0.0,0.0])

    elif root.body.id != -1:
        return root.body.pos
    else:
        position = array([0.0,0.0,0.0])
        tm = 0.0
        for hut in root.subhuts:
            if hut is not None:
                position += compute_com(hut)*hut.body.mass
                tm += hut.body.mass
        root.pos = position/tm
        return root.pos
 
class Body:
    def __init__(self):
        self.pos =None 
        self.vel = array([0.0,0.0,0.0])
        self.mass = 0.0
        self.id =-1
        self.force = array([0.0,0.0,0.0]) 
        self.quad_start = None
        self.activated = True

    def reset_force(self):
        self.force = array([0.0,0.0,0.0]) 

    def stats(self):
        print("Msss: ",self.mass," ID: ",self.id)

    def set(self,pos,vel,mass,idd=-1):
        self.pos = pos
        self.vel = vel
        self.mass = mass
        self.id = idd

    def copy(self,b):
        self.pos = b.pos
        self.vel = b.vel
        self.mass = b.mass
        self.id = b.id

    def isempty(self): 
        if self.pos is not None:
            return False 
        return True 

class Quad:
    def __init__(self,start=None,length=0):
        self.start = start
        self.l = length 
        self.subquads = [None,None,None,None]


    def contain(self, pos):
        if self.start[0] <= pos[0]  <= self.start[0] + self.l and self.start[1] <= pos[1]  <= self.start[1] + self.l :
            return True  

    def get_quad(self,i):
        if i==0:
            return self.NW()
        elif i==1:
            return self.NE()
        elif i==2:
            return self.SW()
        elif i==3:
            return self.SE()


    def get_correct_quad(self,pos):
        dpos = array(pos - self.start,dtype=float32)
        ddpos = dpos/(self.l/2.0)
#        print("dividng: ",dpos,self.l/2.0,ddpos)
        try:
            ind = int(int(ddpos[0]) + int(ddpos[1])*2)
            if 0 <= ind <= 3:
                return ind
            else:
                print("outside range of quad",ind,pos,self.start)
                return -1
        except:
            print("Exception outside range of quad",pos,self.start,ddpos,self.l/2.0)
            return -1

 
    def __get_sx_sy(self): 
        return self.start[0],self.start[1]

    def NW(self):
        s = self.l/2
        sx,sy = self.__get_sx_sy()
        return Quad(array([sx,sy,0.0]),s)
    
    def NE(self):
        s = self.l/2
        sx,sy = self.__get_sx_sy()
        return  Quad(array([sx + s,sy,0.0]),s)
    
    def SW(self):
        s = self.l/2
        sx,sy = self.__get_sx_sy()
        return Quad(array([sx ,sy + s,0.0]),s)
    
    def SE(self):
        s = self.l/2
        sx,sy = self.__get_sx_sy()
        return Quad(array([sx + s,sy + s,0.0]),s)


class BarnesHut:
    def __init__(self,quad):
        self.quad = quad 
        self.body = Body()
        self.subhuts = [None,None,None,None]
        self.theta = theta
        self.count = 0
        pass
    
    def get_all_childs(self):
        subhuts = True
        childs = []
        for hut in self.subhuts:
            if hut is not None :
                childs.extend(hut.get_all_childs())
                subhuts = False 
        if subhuts: 
            childs.append(self.body.id)
        return childs

    def insert(self,b):
        """should not pass an copied object"""
        if self.body.isempty():
            """empty hut node"""
            self.body = b
            self.body.quad_start = self.quad.start
        
        elif self.body.id == -1:
            """internal node, just add with current body and insert
            into appropriate sub huts"""
            self.body = add_bodies(self.body,b)
            x = self.insert_into_quad(b)
            self.count = x+1 
            
        else:
            """leaf node,should be handle with care"""
            new_body = add_bodies(self.body,b)
            current_body = self.body
            self.body = new_body

            u1 = self.insert_into_quad(b)
            u2 = self.insert_into_quad(current_body)
            self.count = max(u1,u2) + 1
        return self.count 
    
    def insert_into_quad(self,b):
        i = self.quad.get_correct_quad(b.pos) 
        i = int(i)
        if i != -1:
            Q = self.quad.get_quad(int(i))
            print("next quad",self.quad.l,Q.l)
            if self.subhuts[i] is None:
                self.subhuts[i] = BarnesHut(Q)
                self.subhuts[i].count = 0 
            return self.subhuts[i].insert(b) 
        else:
            exit()
            pass

    def update_force(self,b,G): 
        if self.body.id!= -1 and b.id != self.body.id:
            b.force += compute_gravity_vector(b.pos,b.mass,self.body.pos,self.body.mass,G)
            print(b.id,b.mass,self.get_all_childs(),self.body.mass, b.force)
            return
        d = norm(self.body.pos-b.pos) 
        if self.quad.l/d < self.theta:
            force = compute_gravity_vector(b.pos,b.mass,self.body.pos,self.body.mass,G)
            b.force += force
            print(b.id,b.mass,self.get_all_childs() ,self.body.mass,force)
            return
        else:
            for hut in self.subhuts:
                if hut is not None:
                    hut.update_force(b,G)

    def update_positions(self,dt):
        if self.body.id != -1:
            self.body.vel += self.body.force * dt 
            self.body.pos += self.body.vel* dt
        else:
            for hut in self.subhuts:
                if hut is not None:
                    hut.update_positions(dt)

    def draw_tree(self,string):
        string += str(self.body.id) + " "
        for hut in self.subhuts:
            if hut is not None:
                string += hut.draw_tree(string)
        return string



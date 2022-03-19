from utils import *
import time 

def add_bodies(b1,b2):
    tm = b1.mass + b2.mass
    com = (b1.pos*b1.mass + b2.pos*b2.mass)/tm
    ret = Body()
    ret.set(com,None,mass)
    return ret
 

class Body:
    def __init__(self):
        self.pos =None 
        self.vel =None 
        self.mass =None 
        self.id =-1
        self.force = np.array([0.0,0.0,0.0]) 



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
        if self.pos == None:
            return True
        return False

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
        dpos = np.array(pos - self.start,dtype=np.int)
        dpos /= self.l/2
        ind = dpos[0] + dpos[1]*2 
        if 0 <= ind <= 3:
            return ind
        else:
            print("outside range of quad")
            return -1

 
    def __get_sx_sy(self): 
        return self.pos[0],self.pos[1]

    def NW(self):
        s = self.l//2
        sx,sy = self.__get_sx_sy()
        return Quad(np.array([sx,sy]),,s)
    
    def NE(self):
        s = self.l//2
        sx,sy = self.__get_sx_sy()
        return  Quad(np.array([sx + s,sy]),s)
    
    def SW(self):
        s = self.l//2
        sx,sy = self.__get_sx_sy()
        return Quad(np.array([sx ,sy + s]),s)
    
    def SE(self):
        s = self.l//2
        sx,sy = self.__get_sx_sy()
        return Quad(np.array([sx + s,sy + s]),s)


class BarnesHut:
    def __init__(self,quad):
        self.quad = quad 
        self.body = Body()
        self.subhuts = [None,None,None,None]
        self.theta = 0.1
        pass
 

    def insert(self,b):
        """should not pass an copied object"""
        if self.body.isempty():
            """empty hut node"""
            self.body = b
        
        elif self.body.id == -1:
            """internal node, just add with current body and insert
            into appropriate sub huts"""
            self.body = add_bodies(self.body,b)
            self.insert_into_quad(b)
            
        else:
            """leaf node,should be handle with care"""
           new_body = add_body.add(self.body,b)
           current_body = self.body
           self.body = new_body

           self.insert_into_quad(b)
           self.insert_into_quad(current_body)
    
    def insert_into_quad(self,b):
        i = self.quad.get_correct_quad(b.pos) 
        if i != -1:
            Q = self.quad.get_quad(i)
            if self.subhuts[i] == None:
                self.subhuts[i] = BarnesHut(Q)
            self.subhuts[i].insert(b)

    def update_force(self,b): 
        if self.body!= -1 and b.id != self.body.id:
            b.force += compute_gravity(b.pos,b.body.mass,self.body.pos,self.body.mass)
            return
        d = np.linalg.norm(self.body.pos-b.pos) 
        if self.quad.l/d < self.theta:
            force = compute_gravity(b.pos,b.mass,self.body.pos,self.body.mass)
            b.force += force
        else:
            for hut in self.subhuts:
                if hut is not None:
                    hut.update_force(b)

    def update_positions(self,dt):
        if self.body.id != -1:
            self.body.vel += self.body.force * dt 
            self.body.pos += self.body.vel* dt
        else:
            for hut in self.subhuts:
                if hut is not None:
                    hut.update_positions(dt)

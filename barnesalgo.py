from utils import *
import time 

def add_bodies(b1,b2):
    tm = b1.mass + b2.mass
    com = (b1.pos*b1.mass + b2.pos*b2.mass)/tm
    ret = Body()
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
        return np.array([0.0,0.0,0.0])

    elif root.body.id != -1:
        return root.body.pos
    else:
        position = np.array([0.0,0.0,0.0])
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
        self.vel = np.array([0.0,0.0,0.0])
        self.mass = 0.0
        self.id =-1
        self.force = np.array([0.0,0.0,0.0]) 
        self.quad_start = None

    def reset_force(self):
        self.force = np.array([0.0,0.0,0.0]) 

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
        dpos = np.array(pos - self.start,dtype=np.float32)
        dpos = dpos/(self.l/2.0)
        try:
            ind = int(int(dpos[0]) + int(dpos[1])*2)
            if 0 <= ind <= 3:
                return ind
            else:
#                print("outside range of quad",ind)
                return -1
        except:
            print(dpos)
            return -1

 
    def __get_sx_sy(self): 
        return self.start[0],self.start[1]

    def NW(self):
        s = self.l/2
        sx,sy = self.__get_sx_sy()
        return Quad(np.array([sx,sy,0.0]),s)
    
    def NE(self):
        s = self.l/2
        sx,sy = self.__get_sx_sy()
        return  Quad(np.array([sx + s,sy,0.0]),s)
    
    def SW(self):
        s = self.l/2
        sx,sy = self.__get_sx_sy()
        return Quad(np.array([sx ,sy + s,0.0]),s)
    
    def SE(self):
        s = self.l/2
        sx,sy = self.__get_sx_sy()
        return Quad(np.array([sx + s,sy + s,0.0]),s)


class BarnesHut:
    def __init__(self,quad):
        self.quad = quad 
        self.body = Body()
        self.subhuts = [None,None,None,None]
        self.theta = 0.5
        self.count = 0
        pass
 

    def insert(self,b):
        self.count+=1
        """should not pass an copied object"""
        if self.body.isempty():
            """empty hut node"""
            self.body = b
            self.body.quad_start = self.quad.start
        
        elif self.body.id == -1:
            """internal node, just add with current body and insert
            into appropriate sub huts"""
            self.body = add_bodies(self.body,b)
            self.insert_into_quad(b)
            
        else:
            """leaf node,should be handle with care"""
            new_body = add_bodies(self.body,b)
            current_body = self.body
            self.body = new_body

            self.insert_into_quad(b)
            self.insert_into_quad(current_body)
        return self.count 
    
    def insert_into_quad(self,b):
        i = self.quad.get_correct_quad(b.pos) 
        i = int(i)
        if i != -1:
            Q = self.quad.get_quad(int(i))
            if self.subhuts[i] is None:
                self.subhuts[i] = BarnesHut(Q)
                self.subhuts[i].count = self.count
            self.count = self.subhuts[i].insert(b) + 1
        else:
            print("insertion failed")
            pass

    def update_force(self,b,G): 
        if self.body.id!= -1 and b.id != self.body.id:
            b.force += compute_gravity_vector(b.pos,b.mass,self.body.pos,self.body.mass,G)
            return
        d = np.linalg.norm(self.body.pos-b.pos) 
        if self.quad.l/d < self.theta:
            force = compute_gravity_vector(b.pos,b.mass,self.body.pos,self.body.mass,G)
            b.force += force
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

           



from utils import *
import time 



class Body:
    def __init__(self,pos,vel,mass,idd=-1):
        self.pos = pos
        self.vel = vel
        self.mass = mass
        self.id = idd

    def copy(self,b):
        self.pos = b.pos
        self.vel = b.vel
        self.mass = b.mass
        self.id = b.id

    def presentin(self,quad):
        xp = False
        yp = False


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


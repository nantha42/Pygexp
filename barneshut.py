from utils import *
import time 


class Body:
    def __init__(self,x=0,y=0,mass=0):
        self.x = x
        self.y = y
        self.mass = mass

    def in(self,quad);
        xpres = False 
        ypres = False
        if quad.x <= self.x  <= quad.x+quad.l:
            xpres = True
        if quad.y <= self.y  <= quad.y+quad.l:
            ypres = True
        return xpres and ypres
    
    def add(self,b1,b2):
        tm = b1.mass + b2.mass
        x = (b1.x*b1.mass + b2.x*b2.mass)/tm
        y = (b1.y*b1.mass + b2.y*b2.mass)/tm
        return Body(x,y,tm)
    
    def isempty(self):
        if self.x==0 and self.y == 0 and self.mass == 0:
            return True

class Quad:
    def __init__(self,x,y,length):
        self.sx = x 
        self.sy = y
        self.l = length
        self.subquads = [None,None,None,None]

    
    def contains(self,x,y):
        ypres, xpres = False,False
        if self.sx <=  x <= self.sx + self.l:
            xpres = True
        if self.sy <=  y <= self.sy + self.l:
            ypres = True
        return (xpres and ypres)
    
    def get_quad(self,i):
        if i==0:
            return self.NW()
        elif i==1:
            return self.NE()
        elif i==2:
            return self.SW()
        elif i==3:
            return self.SE()

    def NW(self):
        s = self.l//2
        return Quad(self.sx,self.sy,s)
    
    def NE(self):
        s = self.l//2
        return  Quad(self.sx + s,self.sy,s)
    
    def SW(self):
        s = self.l//2
        return Quad(self.sx ,self.sy + s,s)
    
    def SE(self):
        s = self.l//2
        return Quad(self.sx + s,self.sy + s,s)

class Barneshut:
    def __init__(self,quad):
        self.quad = quad 
        self.body = Body()
        self.subhuts = [None,None,None,None]
        pass

    def insert(self,b):
        """inserts a body"""
        if self.body.isempty():
            self.body = self.body.add(self.body,b)
        else: 
            for i in range(len(4)):
                Q = self.quad.get_quad(i)
                if b.in(Q):
                    if self.subhuts[i] == None:
                        self.subhuts[i] = Barneshut(Q)
                        self.subhuts[i].insert(b)
                    else:
                        self.subhuts[i].insert(b)
                        
                    hut.insert(b) 
                    break



from utils import *
import time 


class Body:
    def __init__(self,x=0,y=0,mass=0):
        self.x = x
        self.y = y
        self.mass = mass
        self.force = np.array([0.0,0.0])
        self.id = -1 


    def copy(self,b):
        self.x = b.x
        self.y = b.y
        self.mass= b.mass
        self.id = b.id

    def presentin(self,quad):
        xpres = False 
        ypres = False
        if quad.sx <= self.x  <= quad.sx+quad.l:
            xpres = True
        if quad.sy <= self.y  <= quad.sy+quad.l:
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
    
    def get_correct_quad(self,x,y):
        dx = x-self.sx
        dy = y-self.sy
        index = (dx//(self.l/2)) + 2*(dy//(self.l/2))
        if 0 <= index <= 3: 
            return int(index)
        else:
            print("impossible")
            return -1
        pass

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
        if self.body.isempty() and self.quad.contains(b.x,b.y):
            copy_body = Body()
            copy_body.copy(b)
            self.body = copy_body
        elif self.body.id==-1:
            # if internal node
            i = self.quad.get_correct_quad(b.x,b.y)
            if i == -1: return
            if 0 <= i <= 3: 
                Q = self.quad.get_quad(i)
                if self.subhuts[i] == None:
                    self.subhuts[i] = Barneshut(Q)
                    self.subhuts[i].insert(b)
                else:
                    self.subhuts[i].insert(b)
                self.body = self.body.add(b,self.body)
        else: 
            i = self.quad.get_correct_quad(b.x,b.y)
            ci = self.quad.get_correct_quad(self.body.x,self.body.y)#current body id
            if i == -1 or ci == -1: return
            if 0 <= i <= 3: 
                Q = self.quad.get_quad(i)
                if self.subhuts[i] == None:
                    self.subhuts[i] = Barneshut(Q)
                    self.subhuts[i].insert(b)
                else:
                    self.subhuts[i].insert(b)

            if 0 <= ci <= 3:
                Q = self.quad.get_quad(ci)
                if self.subhuts[ci] == None:
                    self.subhuts[ci] = Barneshut(Q)
                    self.subhuts[ci].insert(self.body)
                else:
                    self.subhuts[ci].insert(self.body)

                self.body = self.body.add(b,self.body)
            else:
                print("not present")
    
    def update_force(self,b):
        #self.body.id == -1 means it is a internal node
        if self.body.id != -1 and b.id != self.body.id:
            force = compute_gravity(b.x,b.y,b.mass,self.body.x,self.body.y,self.body.mass)
            b.force += force
            return 
        
        d = np.array([self.body.x - b.x,self.body.y - b.y] )
        d = np.linalg.norm(d) 
        if self.quad.l/d < 0.5:
            force = compute_gravity(b.x,b.y,b.mass,self.body.x,self.body.y,self.body.mass)    
            b.force += force
            return
        else:
            for hut in self.subhuts:
                if hut is not None:
                    hut.update_force(b)



















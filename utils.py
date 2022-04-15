from numpy.linalg import norm 
from numpy import float32
from numpy import triu 
from numpy import inf 
from numpy import nan 
from numpy import isnan 
from numpy import newaxis
from numpy import array
from numpy import sqrt, deg2rad,cos,sin
from numpy.linalg import norm
from numpy.random import randint
from math import atan2, radians
from time import time, sleep
print_enabled = True 


def camera_view(vector, points):
    """
        the vector pointing direction is the camera angle and the point ends is 
        where the camera capture screen and from that place frustrum starts. Its 
        a triangular ratio. 
    """
    pass


def printt(*args):
    if print_enabled:
        sti =""
        for arg in args:
            sti += str(arg)+" "
        print(sti)
    pass
            
def count_elements(x):
    ans = 1
    for i in range(len(x.shape)):
       ans *= x.shape[i] 
    return ans 

def generate_name():
    alphabets = "abcedfghijklmnopqrstuvwxyz"
    consonants = "bcdfghjklmnpqrstvwxyz"
    vowels = "aeiou" 
    l = randint(4,8) 
    name = "" + alphabets[randint(0,26)] 
    def isvowel(x):
        if x in vowels:
            return True
        return False

    for i in range(l):
        if isvowel(name[-1]):
            name += consonants[randint(0,21)] 
        else:
            name += vowels[randint(0,5)]
    return name

def ptrin(x):
    printt(x)
    sleep(1)

def arr(x):
    return array(x,dtype=float32)

def project_polygon(polygon):
    projected_points = []
    for point in polygon:
        x_angle =  atan2(point[0], point[2])
        y_angle =  atan2(point[1], point[2])
        x = x_angle / radians(FOV) * screen_width + screen_height // 2
        y = y_angle / radians(FOV) * screen_width + screen_width // 2
        projected_points.append([x, y])
    return projected_points

def compute_gravity_vector(p1,m1,p2,m2,G):
    """returns a f1,f2 which are ndarray"""
    r = norm(p2-p1)
    unit_vec = (p2-p1)/norm(p2-p1)
    f1 = m2*m1/(r+1)**2
    return f1*unit_vec

def compute_gravity(x1,y1,m1,x2,y2,m2):
    """returns a f1,f2 which are ndarray"""
    v = array([x2-x1,y2-y1,0])
    r = linalg.norm(v)
    nv = v/r
    f = nv*m2/(r**2)
    printt("mag: ",m2/(r**2))
    return f
    


class Timer:
    def __init__(self,name):
        self.start = time()
        self.name = name

    def elapsed(self):
        printt(self.name + " Elapsed: ",time()-self.start)

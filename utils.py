import numpy as np
import math

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

def compute_gravity(p1,m1,p2,m2):
    """returns a f1,f2 which are ndarray"""
    r = np.linalg.norm(p2-p1)
    f1 = m2/r**2
    f2 = m1/r**2
    return [f1,f2]




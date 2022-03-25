from utils import *
import time 
class Cluster:
    def __init__(self,p):
        """ p is a nd array"""
        self.planets = [p]
        self.center = p.pos
        self.center_velocity = p.vel 
        self.mass = p.mass 
        self.g = None
        self.sector = None

    def get_sector(self,level=1):
        """call after computing center"""
        x = int(self.center[0]//level)
        y = int(self.center[1]//level)
        self.sector = [x,y]
        return self.sector
    
    def merge_clusters(self,clusters):
        t = time.time() 
        for c in clusters:
            self.planets.extend(c.planets)
            self.mass += c.mass
        self.compute_center() 
        print("cluster merging",time.time()-t)

    def merge(self,cluster):
        self.planets.extend(cluster.planets)
        self.compute_center()
        self.mass += cluster.mass
    
    def compute_center(self):
        """Call before get_sector"""
        sx = 0.0
        sy = 0.0
        sz = 0.0
        vx = 0.0
        vy = 0.0
        vz = 0.0
        t= time.time()
        for planet in self.planets:
            sx += planet.pos[0] 
            sy += planet.pos[1]
            sz += planet.pos[2]
            vx += planet.vel[0]
            vy += planet.vel[1]
            vz += planet.pos[2]

        sx/= len(self.planets)
        sy/= len(self.planets)
        sz/= len(self.planets)
        vx/= len(self.planets)
        vy/= len(self.planets)
        vz/= len(self.planets)

        self.center = arr([sx,sy,sz])
        self.center_velocity = arr([vx,vy,vz])

        print("time for center: ",time.time()-t)
    
    def get_mass_sum(self):
        mass = 0
        for p in self.planets:
            mass += p.mass
    
    def update_velocity(self,acceleration,dt=0.01):
        print("updating velocity")
        for p in self.planets:
            p.vel += acceleration*dt

    def update_positions(self,dt):
        print("updating position")
        for p in self.planets:
            p.position += p.velocity*dt

#    def update_velocity(self,cluster):
#        """this is obsolete method"""
#        p1 = self.center
#        p2 = cluster.center
#        m1 = self.mass
#        m2 = cluster.mass
#        forces = compute_gravity(p1,m1,p2,m2)
#        for p in self.planets:
#            p.velocity += forces[0] 
#        for p in cluster.planets:
#            p.velocity += forces[1]

class Planet:
    def __init__(self, p, v, m,index):
        #params are numpy vars
        self.i = index
        self.pos =  p
        self.vel =  v
        self.mass =  m
        self.sector = p/10.0 


#start from size 1
#increase size multiplied by 2
#current_mapp = {} sector : planet_list
#for each size
#    for each key in the map:
#        if any key contains two clusters:
#            compute gravity between the two clusters and update the velocities of the planets in those clusters
#            merge the two clsuters
#    


class Compute_fast:
    def __init__(self,planets,velocities,masses):
        self.clusters = []
        for i in range(len(planets)):
            print("adding ",planets[i])
            p = Planet(planets[i],velocities[i],masses[i],i)
            self.clusters.append(Cluster(p)) 
            self.clusters[-1].get_sector()
        self.pos = planets
        self.vel = velocities
        self.masses = masses
    
    def __construct_key(self,s):
        return str(int(s[0])) + " " + str(int(s[1]))

    def compute_sector_map(self,clusters,level):
        """maps each cluster to the sector""" 
        sector_map = {}
        for cluster in clusters:
            sector = cluster.get_sector(level)
            key =self.__construct_key(sector)
            if key in sector_map.keys():
                sector_map[key].append(cluster)
            else:
                sector_map[key] = [cluster]
        return sector_map 

    def update(self):
        level = 1
        dt = 0.01
        t_clusters = list(self.clusters)
        if len(t_clusters) == 0:
            return
        c_sector_map = self.compute_sector_map(t_clusters,level)
        next_sector = {}
        while len(c_sector_map.keys())>1:
            print("Length of secs",len(c_sector_map.keys()))
            level *= 2 
            for key in c_sector_map.keys():
                print("another loop 1")
                cluster_groups = c_sector_map[key]
                if len(cluster_groups) > 1:
                    positions = []
                    velocities = []
                    masses = []
                    for c in cluster_groups:
                        print("copying 2")
                        positions.append(c.center)
                        velocities.append(c.center_velocity)
                        masses.append(c.mass)
                    positions = np.array(positions)
                    velocities = np.array(velocities)
                    masses = np.array(masses)
                    print('calculate before')
                    computed_accel = self.compute_accurate(positions,velocities,masses)
                    print('calculate after')
                    for i in range(len(computed_accel)): 
                        print("updating velocity ")
                        cluster_groups[i].update_velocity(computed_accel[i],dt)
                    print("computed_accel", len(computed_accel))
                print('merging')
                first_one = cluster_groups[0] 
                first_one.merge_clusters(cluster_groups[1:])
                cluster_sector_key = self.__construct_key(first_one.get_sector())
                if cluster_sector_key in  next_sector.keys():
                    next_sector[cluster_sector_key].append(first_one)
                else:
                    next_sector[cluster_sector_key] = [first_one]
                print('merged')
            c_sector_map = next_sector
        last_key = list(c_sector_map.keys())[0] 
        now_planets = c_sector_map[last_key][0].planets
        now_planets.sort(key=lambda x: x.i,reverse=True)
        npos,nvel,nmass = [],[],[]
        self.clusters = []
        for i in range(len(now_planets)):
            self.clusters.append(Cluster(now_planets[i]) )
            npos.append(now_planets[i].pos)
            nvel.append(now_planets[i].vel)
            nmass.append(now_planets[i].mass)

        self.pos,self.vel,self.masses = np.array(npos),np.array(nvel),np.array(nmass)


    def compute_accurate(self,planets, planets_vel,planets_mass, dt=0.01):
        print(planets.shape)
        print(planets)
        t1 = time.time()
        x1 = -planets.reshape([-1,1,3])
        x2 = planets.reshape([1,-1,3])
        r = x1 + x2 
        G = 1
        normed = np.linalg.norm(r,axis=2)
        squared = (normed*normed)
        quaded = (normed*normed*normed*normed)
        filtered = squared
        nans = np.isnan(filtered)
        filtered[nans] = 0
        filtered[filtered == np.inf] = 0
        filtered[filtered == -np.inf] = 0
        unit = G*(r/filtered[:,:,np.newaxis] )
        

        unit[np.isnan(unit)] = 0
        unit[unit== np.inf] = 0
        unit[unit == -np.inf] = 0
        unit = planets_mass.reshape([1,-1,1])*unit 
       
#        try:
#            planets_vel += unit.sum(axis=1)*dt
#            planets += planets_vel*dt
#            #for i in range(len(self.trails)):
#            #    if len(self.trails[i])>10:
#            #        self.trails[i].pop(0)
#            #    self.trails[i].append(self.planets[i].tolist())
#            #self.filterstore = self.planets
#            #time.sleep(1)
#            pass
#        except:
#            pass
        print("time taken",time.time()-t1)
        return unit.sum(axis=1) 






        

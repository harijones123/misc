import random
import math as m
import numpy as np
from matplotlib import pyplot as plt

G = 6.67408E-4

def calc_distance(pos1,pos2):
    return m.sqrt((pos1[0]-pos2[0])**2+(pos1[1]-pos2[1])**2)
class Body():
    def __init__(self,m,pos0,v0):
        self.pos = pos0
        self.v = v0
        self.m = m
        self.rad = 0.02*m**0.5  #multiplied by a radius factor
        
class Planet(Body):
    def __init__(self,m,pos0,system,v0=(random.uniform(-1,1),random.uniform(-1,1))):
        super().__init__(m,pos0,v0)
        self.system = system

    def get_total_acc(self):
        a = self.get_acc(self.system.star,calc_distance(self.pos,self.system.star.pos))
        for planet in self.system.planets:
            if planet == self:
                continue
            r_tgt = calc_distance(self.pos,planet.pos)
            if r_tgt <= self.rad+planet.rad:
                self.system.collision(self,planet)
            a = tuple(map(sum,zip(a,self.get_acc(planet,r_tgt))))
        self.a = a

    def get_acc(self,target,r_tgt):
        a_mag_tgt = (-1)*G*target.m/r_tgt**2
        return ((a_mag_tgt/r_tgt)*(self.pos[0]-target.pos[0]),(a_mag_tgt/r_tgt)*(self.pos[1]-target.pos[1]))
        
    def make_timestep(self,dt):
        self.get_total_acc()
        self.v = (self.v[0]+self.a[0]*dt,self.v[1]+self.a[1]*dt)
        self.pos = (self.pos[0]+self.v[0]*dt, self.pos[1]+self.v[1]*dt)

        

class Star(Body):
    def __init__(self,m=100,pos0=(0,0)):
        super().__init__(m,pos0,0)

class System():
    def __init__(self,star,posns,ms,v0s):
        self.star = star
        self.planets = [Planet(mass,pos0,self,v0=v) for mass,pos0,v in zip(ms,posns,v0s)]
        #setup plotting
        plt.ion()
        self.fig, self.ax = plt.subplots()
    def simulate(self,T,dt):
        t=0
        self.historyx = []
        self.historyy = []
        while t<=T:
            self.make_timestep(dt)
            self.plotting()
            t = t+dt

    def make_timestep(self,dt):
        for planet in self.planets:
            planet.make_timestep(dt)
    
    def plotting(self):
        x = [planet.pos[0] for planet in self.planets]
        y = [planet.pos[1] for planet in self.planets]
        mass = [planet.m**0.5 for planet in self.planets]
        #self.historyx.append(x)
        #self.historyy.append(y)
        #self.historyx = self.historyx[len(self.historyx)-10:]
        #self.historyy = self.historyy[len(self.historyy)-10:]
        #self.ax.plot(self.historyx,self.historyy,"b")
        self.ax.plot(self.star.pos[0],self.star.pos[1],"k+")
        self.ax.scatter(x,y,s=mass)
        L=20
        plt.xlim(-L,L)
        plt.ylim(-L,L)
        #self.sc.set_offsets(np.c_[x,y])
        #self.fig.canvas.draw_idle()
        plt.pause(0.01)
        plt.draw()
        plt.cla()

    def collision(self,p1,p2):
        if p2.m > p1.m:
            p1,p2 = p2,p1
        #velocity calculated based on cons of momentum
        sum_m = p1.m + p2.m
        p1.v = ((p1.v[0]*p1.m + p2.v[0]*p2.m)/sum_m, (p1.v[1]*p1.m + p2.v[1]*p2.m)/sum_m) 
        p1.m = sum_m 
        #drop planet 2 as it's been engulfed by planet 1
        self.planets.remove(p2)

        


star1 = Star(m=5000,pos0=(0,0))
"""
posns = [(0,5),(0,-6)]
ms = [100,10]
v0s = [(0.3,0),(-0.3,0)]
"""
posns = []
ms = []
v0s = []
posrange = np.linspace(-10,10,10)
for i in np.linspace(-10,10,10):
    for j in np.linspace(-10,10,10):
        posns.append((i,j))
        ms.append(10)
        #v0s.append((random.uniform(-0.1,0.1),random.uniform(-0.1,0.1)))
        V = 1
        vy = m.copysign(j/i, V*((j/i)**2 + 1)**-0.5)
        vx = vy*j/i
        print(f"{vx},{vy}")
        v0s.append((vx,vy))
    


system1 = System(star1,posns,ms,v0s)
system1.simulate(100,0.05)
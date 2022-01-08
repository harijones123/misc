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
        
class Planet(Body):
    def __init__(self,m,pos0,system,v0=(random.uniform(-1,1),random.uniform(-1,1))):
        super().__init__(m,pos0,v0)
        self.system = system

    def get_acc(self):
        r_star = calc_distance(self.pos,self.system.star.pos)
        a_mag_star = (-1)*G*self.system.star.m/r_star**2
        self.a = ((a_mag_star/r_star)*(self.pos[0]-self.system.star.pos[0]),(a_mag_star/r_star)*(self.pos[1]-self.system.star.pos[1]))
        
    def make_timestep(self,dt):
        self.get_acc()
        self.v = (self.v[0]+self.a[0]*dt,self.v[1]+self.a[1]*dt)
        self.pos = (self.pos[0]+self.v[0]*dt, self.pos[1]+self.v[1]*dt)
        #print(f"pos={self.pos}")
        #print(f"v={self.v}")
        #print(f"a={self.a}")
        

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
        x,y = [],[]
        self.sc = self.ax.scatter(x,y)
        L = 10
        plt.xlim(-L,L)
        plt.ylim(-L,L)
        plt.draw()
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
        self.historyx.append(x)
        self.historyy.append(y)
        self.ax.plot(self.historyx,self.historyy,"b")
        self.ax.plot(self.star.pos[0],self.star.pos[1],"k+")
        self.sc.set_offsets(np.c_[x,y])
        self.fig.canvas.draw_idle()
        plt.pause(0.01)
        plt.draw()

star1 = Star(m=2E3)
posns = []
ms = []
v0s = []
for i in range(5):
    posns.append((0,random.uniform(3,7)))
    ms.append(100)
    V = 0.5
    v0s.append((0.5,0))


system1 = System(star1,posns,ms,v0s)
system1.simulate(500,1)
import random
import math as m
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from IPython import display
import time

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
            if (r_tgt <= self.rad+planet.rad) and (self.system.collision==True):
                self.system.collision_event(self,planet)
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
    def __init__(self,star,posns,ms,v0s,do_plot=True,collision=True):
        self.star = star
        self.do_plot = do_plot
        self.planets = [Planet(mass,pos0,self,v0=v) for mass,pos0,v in zip(ms,posns,v0s)]
        self.collision = collision
        self.do_plot = do_plot
        self.init_plotting()
        
    def init_plotting(self):
        #setup plotting and animation saving
        if self.do_plot==True:
            plt.ion()
        self.fig = plt.figure()
        self.L=20
        self.ax = plt.axes(xlim=(-self.L,self.L), ylim=(-self.L,self.L))
        self.ax.set_axis_off()
        self.scat = self.ax.scatter([], [])
        self.historyx = []
        self.historyy = []


    def simulate(self,T,dt):
        t=0
        self.historyx = []
        self.historyy = []
        while t<=T:
            self.make_timestep(dt)
            self.plotting(t)
            t = t+dt

    def make_timestep(self,dt):
        for planet in self.planets:
            planet.make_timestep(dt)
        mass = [planet.m**0.5 for planet in self.planets]
        xpos = [planet.pos[0] for planet in self.planets]
        ypos = [planet.pos[1] for planet in self.planets]

    def animate(self,i,dt):
        print(f"frame:{i}")
        for planet in self.planets:
            planet.make_timestep(dt)
        mass = [planet.m**0.5 for planet in self.planets]
        xpos = [planet.pos[0] for planet in self.planets]
        ypos = [planet.pos[1] for planet in self.planets]
        self.scat.set_offsets(np.column_stack((xpos, ypos)))
        self.scat.set_sizes(mass)
        return self.scat
        
    def plotting(self,t):
        x = [planet.pos[0] for planet in self.planets]
        y = [planet.pos[1] for planet in self.planets]
        mass = [planet.m**0.5 for planet in self.planets]

        if self.do_plot==True:
            self.scat.set_offsets(np.c_[x,y])
            self.scat.set_sizes(mass)
            self.fig.canvas.draw_idle()
            #self.ax.plot(self.star.pos[0],self.star.pos[1],"k+")
            #if t>=T/10:
            #    self.historyx.append(x)
            #    self.historyy.append(y)
            #    self.ax.plot(self.historyx,self.historyy,"b")
            plt.xlim(-self.L,self.L)
            plt.ylim(-self.L,self.L)
            plt.pause(0.01)
            plt.draw()

    def collision_event(self,p1,p2):
        if p2.m > p1.m:
            p1,p2 = p2,p1
        #velocity calculated based on cons of momentum
        sum_m = p1.m + p2.m
        p1.v = ((p1.v[0]*p1.m + p2.v[0]*p2.m)/sum_m, (p1.v[1]*p1.m + p2.v[1]*p2.m)/sum_m) 
        p1.m = sum_m 
        #drop planet 2 as it's been engulfed by planet 1
        if p2 in self.planets:
            self.planets.remove(p2)
    
    def create_animation(self,dt,frames):
        self.anim = FuncAnimation(self.fig, self.animate,fargs=(dt,),frames=frames)

        
def generate_tangential_vector(input_vector,scale=1):
    """generates unit vector in direction of circular motion in x,y coords"""
    a,b = input_vector
    K = -b/a 
    if a>=0:
        scale = -scale
    return (scale*K/(K**2 + 1)**0.5,scale*1/(K**2 + 1)**0.5)



star1 = Star(m=5000,pos0=(0,0))
"""
posns = [(0,5),(0,-6)]
ms = [100,10]
v0s = [(0.3,0),(-0.3,0)]
"""

#starting conditions
NN = 10
dt = 0.05
frames = 20000
T = frames*dt
posns = []
ms = []
v0s = []
masses = 20
for i in np.linspace(-10,10,NN):
    for j in np.linspace(-10,10,NN):
        posns.append((i,j))
        ms.append(masses)
        #v0s.append((random.uniform(-0.1,0.1),random.uniform(-0.1,0.1)))
        r = m.sqrt(i**2 + j**2)
        v = m.sqrt(G*(star1.m + ((r**2)/100)*masses*NN**2)/r)
        v0s.append(generate_tangential_vector((i,j),scale=v))

#simulate
system1 = System(star1,posns,ms,v0s,do_plot=True)

system1.simulate(T,dt)
#system1.create_animation(dt,frames)
#system1.anim.save('gravity.gif', writer=PillowWriter(fps=30) )
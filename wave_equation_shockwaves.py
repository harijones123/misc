import numpy as np
import matplotlib.pyplot as plt
import time
import math
import random

import pylab as plt
from mpl_toolkits.mplot3d import Axes3D  
from matplotlib import cm

#equation d2u/dx2 = c2*d2u/dx2
#CD approx solution
def splash(u_current,u_last,loc,h=1):
    u_current[loc[0]+1,loc[1]] += h/4
    u_current[loc[0]-1,loc[1]] += h/4
    u_current[loc[0],loc[1]+1] += h/4
    u_current[loc[0],loc[1]-1] += h/4
    u_last[loc[0],loc[1]] += h
    return u_current,u_last


r = 1  #r = c*dt/dx
c = 20
L = 10
dx = 0.2
h0 = 4
plotting = True
C=1
E=1000

dt = r*dx/c
NN = int(L/dx)
r2 = r**2
#total simulation time
T = 10
Ms = np.linspace(0.1,2,int(T/dt))

#define the space
x0 = np.linspace(0,NN*dx,NN)
u0 = np.zeros((NN,NN))

u_current = u0
u_last = np.zeros((NN,NN))
u_next = np.zeros((NN,NN))
t=0
ii=0
r = c*dt/dx

#plotting
if plotting:
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
X, Y = np.meshgrid(x0, x0)
d=0
print(Ms)
for M in Ms:   

    #variable speed for simulation
    n_ind = c*M*dt/dx
    if n_ind>=1:
        n_ind = int(n_ind)
        freq = 1
        freq_frame = 1
    else:
        freq = int(1 / n_ind) + (1 % n_ind > 0)
        freq_frame = int(1 / r) + (1 % r > 0)
        n_ind = 1


    #stationary emitter
    if ii%freq==0:
        u_current[:NN-n_ind],u_last[:NN-n_ind]  = u_current[n_ind:],u_last[n_ind:] 
        u_current[NN-n_ind:] = 0
        u_last[NN-n_ind:] = 0
    #u_current,u_last = splash(u_current,u_last,(int(NN*0.5),int(NN*0.5)),h=0.5)
    u_current[int(NN*0.5),int(NN*0.5)] = 1
    #if ii%freq_frame==0:
    #    u_current,u_last = splash(u_current,u_last,(int(NN*0.5),int(NN*0.5)),h=0.5)

    for i in range(1,NN-1):
        for j in range(1,NN-1):
            u_next[i,j] = (2*u_current[i,j] - u_last[i,j] + 0.5*r2 * (u_current[i+1,j] + u_current[i-1,j] + u_current[i,j-1] + u_current[i,j+1] - 4*u_current[i,j] ))

    
    u_dy = u_next - u_current
    #account for damping
    u_next = u_next - 0.5*C*dt*u_dy

    #account for surface tension
    u_next1 = u_next
    for i in range(1,NN-1):
        for j in range(1,NN-1):
            ys = [u_next1[i-1,j],u_next1[i+1,j],u_next1[i,j-1],u_next1[i,j+1]]
            y0 = u_next1[i,j]
            Ts = [math.copysign(E*((dx**2 + (y0-y)**2)**0.5 - dx),y-y0) for y in ys]
            u_next[i,j] = u_next1[i,j] + 0.5*sum(Ts)*dt**2

    #boundaries
    u_next[0] = 0
    u_next[NN-1] = 0

    #reassign variables
    u_last[:], u_current[:] = u_current, u_next 
    t=t+dt
    ii=ii+1
    

    if plotting:
        #ax.plot_surface(X,Y, u_current,cmap=cm.coolwarm)
        ax.plot_surface(X,Y, u_current,cmap=cm.coolwarm)
        ax.set_zlim(-1, 1.)
        plt.title(f"M={M}")
        plt.draw()
        plt.pause(0.02)
        ax.cla()
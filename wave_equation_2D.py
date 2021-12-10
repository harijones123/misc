import numpy as np
import matplotlib.pyplot as plt
import time
import math

import pylab as plt

#equation d2u/dx2 = c2*d2u/dx2
#CD approx solution
def get_u_next(u_i,u_iplus,u_iminus,u_jminus,r):
    r2 = r**2
    return 2*(1-r2)*u_i + r2*(u_iplus+u_iminus) - u_jminus

r = 1   #r = c*dt/dx
c = 1
L = 10
dx = 0.1
h0 = 1
plotting = True

dt = r*dx/c
NN = int(L/dx)
r2 = r**2
#total simulation time
T = 60

#define the space
x0 = np.linspace(0,NN*dx,NN)
u0 = np.zeros(NN)
u0[int(NN/2)] = h0

u_current = u0
u_last = np.zeros(NN)
u_last[int(NN/2)+1] = h0/2
u_last[int(NN/2)-1] = h0/2
u_next = np.zeros(NN)
t=0
r = c*dt/dx

#plotting
if plotting:
    plt.ion()
    figure, ax = plt.subplots(figsize=(10, 8))
    ax.set_xlim([0, L])
    ax.set_ylim([(-2*h0), 2*h0])
    line1, = ax.plot(x0,u_current)



while t<=T: 
    #print(u_current)
    for i in range(1,NN-1):
        u_next[i] = 2*u_current[i] - u_last[i] + r2 * (u_current[i+1] - 2*u_current[i] + u_current[i-1])
    #boundaries
    u_next[0] = 0
    u_next[NN-1] = 0

    #reassign variables
    u_last[:], u_current[:] = u_current, u_next 
    t=t+dt

    if plotting:
        line1.set_xdata(x0)
        line1.set_ydata(u_current)
        figure.canvas.draw()
        figure.canvas.flush_events()

    time.sleep(0.001)
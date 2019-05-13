# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 23:02:57 2019

@author: Anuar
"""

import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import imageio
import glob, os

# optional: use fancy color schemes
plt.style.use('Solarize_Light2')
#print current color schemes
color = plt.rcParams['axes.prop_cycle'].by_key()['color']
grey ='#657b83' # colour value

# define physical parameters
A, H = 10, 5 # tank dimensions, A = cross-sectional area (m^2), H = total height (m)
rho, g = 1000, 10 # fluid, rho = density (kg/m^3), gravity acceleration (m/s^2)
valve_k = 0.04 # valve conductance

# define integration settings
t_end = 500 # simulation end time (s)
dt = 0.5 # timestep size (s)
n_step = int(t_end / dt) # no. of timestep

# initialise arrays
time = np.arange(0,t_end,dt) # time
sp = np.zeros(n_step) # setpoint
op = np.zeros(n_step) # valve operating point / opening
error = np.zeros(n_step) # error = deviation between actual level and setpoint
error_I = np.zeros(n_step) # accumulation of error i.e. the integral part in PID
level = np.zeros(n_step) # current tank level
dlevel = np.zeros(n_step) # change in level
Qin = np.zeros(n_step) # flow in
Qout = np.full((n_step), np.nan) # flow out
 
# set flow in 
Qin[:] = 1

# controller settings
sp[:int(200/dt):] = 1.5 # set setpoint at t < 200 to 1.5 m
sp[int(200/dt):] = 3 # change setpoint at t = 200
Kc = 0.05 # proportional gain
tau_I = 5 # integral reset time

# image settings
freq = 10 # frequency of of the saved images
images = [] # initialise placeholder for images to be converted to video

for t in range(1,n_step):
        
    # calculate level and error from previous time step    
    level[t] = level[t-1] + dlevel[t-1] 
    error[t] = level[t-1] - sp[t-1] 
    error_I[t] = error_I[t-1] + error[t-1]*dt 
    
    op[t] = Kc * (error[t] + error_I[t]/tau_I) # we only use PI control here                               
    op[t] = np.clip(op[t],0,1)  # make sure op is between 0-100%

    # at current timestep 
    Qout[t] = op[t] * valve_k * np.sqrt(rho*g*level[t]) # this models the flow across the valve
    # above we use flow out = opening * valve conductance * sqrt(delta P)
    # delta P = P at valve inlet - P at valve outlet = ( rho*g*h + P at valve outlet) - P at valve outlet) = rho*g*h
    dlevel[t] = ((Qin[t] - Qout[t]) / A ) * dt # this models the change in level
    
    if (t==1) or (t%freq == 0): # perform this only for the first time step and the specified frequency

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8,5))

        # manually draw the tank diagram
        ax1.plot([0,3],[0,0],'k',alpha=1,lw=2)
        ax1.plot([0,3],[H,H],'k',alpha=1,lw=2)
        ax1.plot([0,0],[0,H],'k',alpha=1,lw=2)
        ax1.plot([3,3],[0.1*H,H],'k',alpha=1,lw=2)
        ax1.plot([3,4],[0,0.1*H],'k',alpha=1,lw=2)
        ax1.plot([3,4],[0.1*H,0],'k',alpha=1,lw=2)
        ax1.plot([4,4],[0,0.1*H],'k',alpha=1,lw=2)
        ax1.plot([-1,0],[0.95*H,0.95*H],'k',alpha=0.5,lw=16)
        ax1.plot([4,6],[0.05*H,0.05*H],'k',alpha=0.5,lw=16)
        # plot tank level and set point
        ax1.add_patch(patches.Rectangle((0, 0), 3, level[t], alpha=0.5))
        ax1.plot([0,3],[sp[t],sp[t]],':r',label='Set point')
        # annotate the diagram
        ax1.text(3.1,1.1*H,'Time='+str(np.round(time[t],2))+' $s$',fontsize=11,color=grey)
        ax1.text(-1,1.1*H,'Flow in='+str(np.round(Qin[t],2))+' $m^3s^{-1}$',fontsize=11,color=grey)
        ax1.text(3,-0.1*H,'Flow out='+str(np.round(Qout[t],2))+' $m^3s^{-1}$',fontsize=11,color=grey)
        ax1.text(3.1,0.15*H,'Valve opening='+str(np.round(op[t]*100,1))+'$\%$',fontsize=11,color=grey)
        ax1.text(3.1,sp[t],'Set point='+str(np.round(sp[t],1))+'$m$',fontsize=11,color=grey)
        ax1.arrow(-1,1.05*H,1,0, head_width=0.2, head_length=0.2,color=grey)
        ax1.arrow(3,-0.15*H,1,0, head_width=0.2, head_length=0.2,color=grey)
        # format the plot
        ax1.set_xlim(-1,7)
        ax1.set_ylim(-1,H+1)
        ax1.axis('off')

        # plot level and setpoint on the graph
        ax2.plot(time[:t],level[:t],label='Tank level')
        ax2.plot(time[:t],sp[:t],':r',label='Set point')
        # format the plot
        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('Tank level (m)')
        ax2.set_xlim(0,t_end)
        ax2.set_ylim(0,H)
        ax2.legend()
        plt.suptitle('Water tank level PID control',color='#657b83',fontsize=15)
                     
        # save the figures
        plt.subplots_adjust(left=0.02, bottom=0.1, right=0.98, top=0.9, wspace=0.02, hspace=0.02)
        file_name = 'level_control_'+str(t)+'.png'
        plt.savefig(file_name,facecolor=fig.get_facecolor(),pad_inches=-1)
        plt.close('all')
        
        # load figure into images
        images.append(imageio.imread(file_name))

# save images as gif   
imageio.mimsave('level_control.gif', images)

# delete the redundant images used to create the gif
for f in glob.glob("level_control_*.png"):
    os.remove(f)      
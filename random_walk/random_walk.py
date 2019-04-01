#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 14:45:16 2019

@author: anuar
"""

"""
Random walk exercise
====================

Plot distance as a function of time for a random walk
together with the theoretical result

"""
import matplotlib.pyplot as plt
import numpy as np
import imageio
import glob, os
np.random.seed(4000)

# optional: use fancy color schemes
plt.style.use('Solarize_Light2')
#print current color schemes
color = plt.rcParams['axes.prop_cycle'].by_key()['color']

#-----------------------------------------------------------------------------
# Random walk overview

# Define no. of particles for each time step and max. time
n = 1000
t_max = 500
freq = 50 # frequency of of the saved images

# generate 1 or -1 to represent (left, right) and (up,down)
steps_x = (np.random.randint(0, 2, (n, t_max))*2 - 1)
steps_y = (np.random.randint(0, 2, (n, t_max))*2 - 1)

# Sum up the steps to keep track their positions at a given time 
positions_x = np.cumsum(steps_x, axis=1)
positions_y = np.cumsum(steps_y, axis=1)

# We need this to generate the square locust of the random walk
positions_x_repeat = np.repeat(positions_x[-1,:],2)
positions_y_repeat = np.repeat(positions_y[-1,:],2)

# initialise placeholder for images to be converted to video
images = []

for j in range(1, t_max):
    if (j==1) or (j%freq == 0): # perform this only for the first time step and the specified frequency

        # initialise all the axes we need
        fig = plt.figure(figsize=(8,4.5))
        ax0 = plt.subplot2grid((3, 5), (1, 0), rowspan=2, colspan=2)
        ax1 = plt.subplot2grid((3, 5), (1, 2), rowspan=2, colspan=2)
        ax2 = plt.subplot2grid((3, 5), (0, 2), colspan=2,
                               sharex=ax1)
        ax3 = plt.subplot2grid((3, 5), (1, 4), rowspan=2,
                               sharey=ax1)
        
        # plot for 1 particle
        ax0.scatter(positions_x[-1,j],positions_y[-1,j],c=color[4], marker='o')
        ax0.plot(positions_x_repeat[1:j*2],positions_y_repeat[:(j*2)-1],'-k',lw=0.5)
        
        # plot for multiple particles
        ax1.scatter(positions_x[-1,j],positions_y[-1,j],c=color[4], marker='o')
        ax1.scatter(positions_x[:,j],positions_y[:,j], alpha=0.2,marker='o')

        # plot the distribution of the particles        
        ax2.hist(positions_x[:,j],bins=10, alpha=0.5)
        ax3.hist(positions_y[:,j],bins=10, orientation='horizontal', alpha=0.5)
        
        # format the plot
        plt.suptitle('Modelling diffusion using random walk',color='#657b83',fontsize=15)
        ax0.text(-40,-40,'1 particle', color='#657b83',fontsize=12)
        ax1.text(-40,-40,str(n)+' particles', color='#657b83',fontsize=12)
        ax0.set_xlim(-40,40)
        ax0.set_ylim(-40,40)
        ax1.set_xlim(-40,40)
        ax1.set_ylim(-40,40)
        ax0.set_xticks([])
        ax0.set_yticks([])
        ax1.set_xticks([])
        ax1.set_yticks([])
        ax2.set_ylim(0,n/2)
        ax3.set_xlim(0,n/2)
        ax2.axis('off')
        ax3.axis('off')

        # save the figures
        plt.subplots_adjust(left=0.02, bottom=0.05, right=0.98, top=0.98, wspace=0.02, hspace=0.02)
        file_name = 'random_walk_00_'+str(j+1)+'.png'
        plt.savefig(file_name,facecolor=fig.get_facecolor(),pad_inches=-1)
        plt.close('all')
        
        # load figure into images
        images.append(imageio.imread(file_name))

#-----------------------------------------------------------------------------------------------
# Pollutant dispersion
# Define no. of particles for each time step and max. time
n = 5
t_max = 5001
freq = 500

# generate 1 or -1 to represent (left, right) and (up,down)
# note that we need a 3D array here to represent the newly genererated particles at the source at each time step
steps_x = (np.random.randint(0, 2, (n, t_max, t_max))*2 - 1)
steps_y = (np.random.randint(0, 2, (n, t_max, t_max))*2 - 1)

# Sum up the steps to keep track their positions at a given time 
positions_x = np.cumsum(steps_x, axis=1)
positions_y = np.cumsum(steps_y, axis=1)
   

for j in range(1, t_max):
    if (j==1) or (j%freq == 0): # perform this only for the first time step and the specified frequency
        fig, ax = plt.subplots(figsize=(8,4.5))

        # add a chimney/flare stack simple line figure
        ax.plot([0,0],[-500,0],'k',lw=10, alpha=0.5)

        # plot the position of the particles
        for k in range(j): # at the current time, keep track the position of the particles released at each time step
            x_shift = k # the average location of the particles 
            ax.scatter(positions_x[:,k,j-k]+x_shift,positions_y[:,k,j-k], alpha=0.01,marker='.', c='k')
       
         # format the plot
        ax.annotate('wind direction', xy=(2500,-200), xytext=(1000,-200),
            arrowprops={'arrowstyle': '->'}, va='center', color='#657b83',fontsize=12)
        ax.text(-200,100,'Point source emission', color='#657b83',fontsize=12)
        ax.set_xlim(-500,5000)
        ax.set_ylim(-500,300)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title('Air pollutant plume (Gaussian model using random walk)', color='#657b83',fontsize=15)

        # save the figures
        plt.subplots_adjust(left=0.02, bottom=0.05, right=0.98, top=0.9, wspace=0.02, hspace=0.02)
        file_name = 'random_walk_01_'+str(j+1)+'.png'
        plt.savefig(file_name,facecolor=fig.get_facecolor(),pad_inches=-1)
        plt.close('all')
        
        # load figure into images
        images.append(imageio.imread(file_name))

# save images as gif   
imageio.mimsave('random_walk.gif', images)   

# delete the redundant images used to create the gif
for f in glob.glob("random_walk_*.png"):
    os.remove(f)        

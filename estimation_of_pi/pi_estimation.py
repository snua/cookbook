# -*- coding: utf-8 -*-
"""
Created on Fri Mar 14 10:07:39 2019

@author: Anuar
"""


import matplotlib.pyplot as plt
import numpy as np
import imageio
np.random.seed(seed=14400)

# optional: use fancy color schemes
plt.style.use('Solarize_Light2')
#print current color schemes
color = plt.rcParams['axes.prop_cycle'].by_key()['color']

# initialise arrays
points = np.arange(50,5050,50)
pi_estimate = np.full((len(points)), np.nan)
images = []

for i, n in enumerate(points):

    fig = plt.figure(figsize=(8,4.8))
    plt.subplot(1,2,1)
    
    # populate coordinates with random values between (-1,1)
    x_coord = np.random.uniform(-1,1,n)
    y_coord = np.random.uniform(-1,1,n)
    
    # compute the distances from origin for all points
    distance = np.sqrt(x_coord**2+y_coord**2)
    
    # plot the points with distance < 1, use masked array to filter these points
    plt.scatter(x_coord, np.ma.masked_where(distance < 1, y_coord),alpha=0.5)
    # plot the points with distance > 1, use masked array to filter these points
    plt.scatter(x_coord, np.ma.masked_where(distance > 1, y_coord),alpha=0.5)
    
    # plot a circle for reference
    x_circle = np.linspace(-1,1,200)
    y_circle = np.sqrt(1-x_circle**2)
    plt.plot(x_circle,y_circle,'-k',alpha=0.5,lw=1)
    plt.plot(x_circle,-y_circle,'-k',alpha=0.5,lw=1)
    
    # format the plot
    plt.text(-1,1.1,'No. of of points='+str(n), color='#657b83',fontsize=12)
    plt.xlim(-1,1)
    plt.ylim(-1,1)
    plt.xticks([-1,0,1])
    plt.yticks([-1,0,1])
             
    plt.subplot(1,2,2)
      
    # area under curve
    pi_estimate[i] = (sum(distance<1)/n) * 4 # 4 is the total area
    plt.plot(points[:i+1],pi_estimate[:i+1], c=color[4],marker='o') 
    
    # plot real pi value for reference
    plt.plot([0,max(points)],[np.pi,np.pi],'k',alpha=0.5)

    # format the plot
    plt.xlabel('No. of points')
    plt.ylabel('Estimation of $\pi$')
    plt.xlim(0,max(points))
    plt.ylim(2.9,3.5)
    plt.suptitle('Estimation of $\pi$ using Monte-Carlo method',color='#657b83',fontsize=15)
    
    # save the figure. facecolor required to make sure the saved image uses the same color
    plt.tight_layout(rect=[0, 0.03, 1, 0.93])
    file_name = 'pi_estimation_'+str(i+1)+'.png'   
    plt.savefig(file_name,facecolor=fig.get_facecolor()) 

    # load figure into images
    images.append(imageio.imread(file_name))

# save images as gif   
imageio.mimsave('pi_estimation.gif', images)

# delete the redundant images used to create the gif
import glob, os
for f in glob.glob("pi_estimation_*.png"):
    os.remove(f)

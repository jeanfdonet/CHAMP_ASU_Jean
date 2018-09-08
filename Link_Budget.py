
# coding: utf-8

# In[61]:


import matplotlib.pyplot as plt
import numpy as np
import math as math
get_ipython().magic(u'matplotlib notebook')


# In[62]:


c       = 299792458.0    #Speed of light
f       = 144e6          #Frequency of interest
lamb    = c/f            #Wavelength of transmission
d       = 384.4e6        #Distance to the moon in m
r       = 1.737e6        #Radius of the moon in m
eta     = 0.7            #Moon's reflection coefficient
p_t     = 500            #Power transmitted in Watts
eff_a   = 93             #Effective collecting area per dish
ant_num = 47             #Number of antennas
A       = eff_a*ant_num  #Total collecting area
ch_w    = 97656.25       #Channel Width


# In[63]:


g_r  = (4.0*np.pi*eff_a)/(lamb**2)
g_t  = 10.0**(2.1)
loss = (eta*(r*lamb)**2)/(64*np.pi**2*d**4)
p_r  = p_t*g_t*g_r*loss
# p_r = 1.0e-19
jy = (p_r*1.0e26)/(eff_a*ch_w)


# In[64]:


print 'Power Transmitted:',p_t,'W\n','Power Received:',p_r,'W (',jy,'JY ) \n\nTransmitting Antenna Gain:', g_t,'\nReceiving Antenna Gain:',g_r,'\nPath Loss:',loss



# coding: utf-8

# In[4]:


import numpy as np
import matplotlib.pyplot as plt
from astropy.time import Time
from astropy.coordinates import Angle, EarthLocation, get_moon, get_sun
from astropy.units import deg
from MoonLSTs import zenithra, zenithdec
import os
import string
import pandas
get_ipython().magic(u'matplotlib notebook')


# In[47]:


path55 = "/data6/HERA/data/2458055/"
path42 = "/data6/HERA/data/2458042/"


# In[48]:


def get_julian_dates(path):
    alpha_low  = list(string.ascii_lowercase)      #Setting lower-case alphabet
    alpha_high = list(string.ascii_uppercase)      #Setting upper-case alphabet
    jd_list = []                                   #Instantiating list for JDs
    for file in os.listdir(path):                  #Iterating over data directory
        if ".xx" in file:
            jd = ""                                #Setting empty string for individual date
            for char in file:                      #Iterating over the file name itself
                if char in alpha_low:
                    file = file.replace(char, "")  
                if char in alpha_high:
                    file = file.replace(char, "")
                if char in ".":
                    file = file.replace(char, "")  #Checking for other usual name chars
                if char in "_":
                    file = file.replace(char, "")
            file = list(file)                      #Date string to list to mutate JD
            file.insert(7,".")                     #Inserting delimiter for JD format
            file = ''.join(file)                   #Joining list into string
            jd   = jd + file                       #Assigning JD string to empty var
            jd_list.append(float(jd))              #Appending float version of JD to JD list


    jd_list = np.unique(jd_list)                   #Selecting unique values in case of repeat
    return jd_list                                 #Returning desired JD list


# In[88]:


jd55 = get_julian_dates(path55) #Creating JD lists for different datasets
print jd55
jd42 = get_julian_dates(path42)
#print jd42


# In[89]:


for jd in range(len(jd55)):
    jd55[jd] += 2428.0

# print jd55
# jd55 = np.linspace(2460676.5,2460780.5,20000) #From JAN 1, 2025 to APR 15, 2025
# jd55 = np.linspace(2458340.5,2460780.5,20000) #From JAN 1, 2025 to APR 15, 2025
# jd55 = np.linspace(2458331.5,2458787.5,6000) #From today to OCT 31, 2019
# jd55 = np.linspace(2453887.5,2458326.5,15000) #From last Major Standstill to today
moon_times = jd55                  #Setting moon_times list from JD list
t = Time(moon_times, format='jd')  #Creating a Time object for get_moon


# In[9]:


zenithra_deg = np.rad2deg(zenithra)
zenithdec_deg = np.rad2deg(zenithdec)

print zenithra_deg
print zenithdec_deg


# In[10]:


#Setting HERA Latitude and Longitude
hera_lat = Angle((-30,43,17), unit=deg) 
hera_lon = Angle((21,35,42), unit=deg)

#Creating an EarthLocation object for HERA
HERA = EarthLocation(lat=hera_lat, lon=hera_lon)


# In[90]:


#Creating get_moon object at HERA's location
moonpath = get_moon(t,location=HERA) #Returns RA, DEC, Dist in (deg,deg,km)
# print moonpath


# In[56]:


#Formatting the RA and dec to more familiar formats
ra_list  = []
dec_list = []

#Retrieving RA in HH:mm:ss format
for h,m,s in zip(moonpath.ra.hms[0],moonpath.ra.hms[1],moonpath.ra.hms[2]):
    ra = str(int(h))+"h "+str(int(m))+"m "+str(s)+"s"
    ra_list.append(ra)

#Retrievving Dec in dd:mm:ss format
for d,m,s in zip(moonpath.dec.dms[0],moonpath.dec.dms[1],moonpath.dec.dms[2]):
    dec = str(int(d))+"d "+str(int(m))+"m "+str(s)+"s"
    dec_list.append(dec)

#Casting JD list of floats into strings due to approximation
jd55 = list(jd55)
for i in range(len(jd55)):
    jd55[i] = str(jd55[i])

#Creating Pandas Data Frame for organized reading of the data
coords = {"JD":jd55, "Moon R.A.":ra_list, "Moon Dec":dec_list}
cols   = ["JD", "Moon R.A.", "Moon Dec"]
frame  = pandas.DataFrame(data=coords)
frame  = frame[cols]
frame


# In[15]:


#Casting to string for datasets w/o moon due to Pandas approximation
jd42 = list(jd42)
for i in range(len(jd42)):
    jd42[i] = str(jd42[i])

coords42 = {"JD": jd42}
pandas.DataFrame(data=coords42)


# In[91]:


sunpath = get_sun(t)
# print sunpath


# In[92]:


print t.isot[1], t.isot[-1], moonpath.dec.deg[-1], zenithdec_deg, np.abs(moonpath.dec.deg[1]-zenithdec_deg)
# type(float(t[1]))


# In[98]:


zenithra_deg = np.rad2deg(zenithra)
zenithdec_deg = np.rad2deg(zenithdec)
dec_in   = []
dec_out  = []
adj_jds  = []
jds_out  = []
dec_opt  = []
ra_opt   = []
jds_opt  = []
dec_opt2 = []
ra_opt2  = []
jds_opt2 = []

fig1 = plt.figure(figsize=(9.5,6.0), facecolor="black", edgecolor="white")
axes = plt.subplot(111)
axes.patch.set_facecolor("black")
plt.grid(True, color="white")
plt.yticks(color="white")
plt.xticks(color="white")


for spine in axes.spines.values():
    spine.set_color("white")

for i in range(len(jd55)):
    rel_ra = np.abs(moonpath.ra.deg[i]-sunpath.ra.deg[i])
#     declist.append(moonpath.dec.deg[i])
#     adj_jds.append(jd55[i])
    if rel_ra>=90.0 and rel_ra<=270.0:
        if rel_ra>180.0:
            rel_ra = 360.0-rel_ra
#         print "JDate", jd55[i], "Moon RA:",moonpath.ra.deg[i], "Sun RA:",sunpath.ra.deg[i], "Diff:", np.abs(moonpath.ra.deg[i]-sunpath.ra.deg[i])
        if np.abs(moonpath.dec.deg[i]-zenithdec_deg)<=8.2215:
            dec_opt.append(moonpath.dec.deg[i])
            ra_opt.append(moonpath.ra.deg[i])
            jds_opt.append(jd55[i])
#             print jd55[i], t.isot[i], moonpath.ra.deg[i], moonpath.dec.deg[i]
            if rel_ra>=178.0 and rel_ra<=182.0:
                print jd55[i], t.isot[i], moonpath.ra.deg[i], moonpath.dec.deg[i]
                plt.plot(jd55[i],rel_ra,"o", c = "#0af00a", markersize=8.0
                        ,markeredgewidth=0.9,markeredgecolor="black")
            else:
                plt.plot(jd55[i],rel_ra,"o", c = "#0af00a", markersize=4.0
                        ,markeredgewidth=0.9,markeredgecolor="black")
        else:
            dec_in.append(moonpath.dec.deg[i])
            adj_jds.append(jd55[i])
            if rel_ra>=178.0 and rel_ra<=182.0:
                plt.plot(jd55[i],rel_ra,"o", c="#d2d2d2", markersize=8.0
                        ,markeredgewidth=0.9,markeredgecolor="black")
            else:
                plt.plot(jd55[i],rel_ra,"o", c="#838383", markersize=4.0
                        ,markeredgewidth=0.9,markeredgecolor="black")
    else:
        dec_out.append(moonpath.dec.deg[i])
        jds_out.append(jd55[i])
#     if rel_ra<177.0:
#         plt.plot(rel_ra,jd55[-i-1],"bo", markersize=4.0)
#     if rel_ra>183.0:
#         plt.plot(rel_ra,jd55[-i-1],"ro", markersize=4.0)
    
#     plt.plot(moonpath.dec.deg[-i-1],jd55[-i-1],"bo", markersize=4.0)
#     plt.plot(sunpath.dec.deg[-i-1],jd55[-i-1],"o",c="#ffce00", markersize=4.0)

plt.ylabel("Shortest Relative RA of the Sun snd Moon [$deg$]", color="white")
plt.xlabel("JDate [$J2000$]", color="white")
plt.title("Lunar Trajectory Over Time", fontweight="bold", color="white")
# plt.background_patch.set_fill(False)
# plt.yticks(jd55,fontsize=3)


# In[99]:


fig2 = plt.figure(figsize=(9.5,6.0), facecolor="black", edgecolor="white")
axes = plt.subplot(111)
axes.patch.set_facecolor("black")
plt.grid(True, color="white")
plt.yticks(color="white")
plt.xticks(color="white")
for spine in axes.spines.values():
    spine.set_color("white")


plt.plot(adj_jds,dec_in,"wo", label=">90$^{\circ}$ from Sun", markersize=1.0)
plt.plot(jds_out,dec_out,"ro", label="<90$^{\circ}$ from Sun", markersize=1.0)
plt.plot(jds_opt,dec_opt,"x", c="#2ef900",label="Optimal", markersize=5.0)
plt.legend(loc="upper left")

plt.ylabel("Moon Declination", color="white")
plt.xlabel("JDate [$J2000$]", color="white")
plt.title("Lunar Declination Over Time", fontweight="bold", color="white")


# In[21]:


x = [1,2,3,4,5]
for i in range(len(x)):
    x[i] += 1
print x


# In[22]:


len(jd55)


# In[23]:


zenithdec_deg


# In[95]:


len(t.isot)


# In[96]:


print jds_opt


# In[100]:


ra_opt, dec_opt


# In[37]:


print range(100,201)


# In[74]:


type(1.0)


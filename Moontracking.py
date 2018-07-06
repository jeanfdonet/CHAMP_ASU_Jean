import numpy as np
import matplotlib.pyplot as plt
from astropy.time import Time
from astropy.coordinates import Angle, EarthLocation, get_moon
from astropy.units import deg
import os
import string
import pandas

#Setting paths to appropriate data directories
path55 = "/data6/HERA/data/2458055/"
path42 = "/data6/HERA/data/2458042/"


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


jd55 = get_julian_dates(path55) #Creating JD lists for different datasets
#print jd55
jd42 = get_julian_dates(path42)
#print jd42


moon_times = jd55                  #Setting moon_times list from JD list
t = Time(moon_times, format='jd')  #Creating a Time object for get_moon


#Get time in GTM/UTC
#print t.isot

#Setting HERA Latitude and Longitude
hera_lat = Angle((-30,43,17), unit=deg) 
hera_lon = Angle((21,35,42), unit=deg)

#Creating an EarthLocation object for HERA
HERA = EarthLocation(lat=hera_lat, lon=hera_lon)

#Creating get_moon object at HERA's location
moonpath = get_moon(t,location=HERA) #Returns RA, DEC, Dist in (deg,deg,km)
#print moonpath


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

#Casting to string for datasets w/o moon due to Pandas approximation
jd42 = list(jd42)
for i in range(len(jd42)):
    jd42[i] = str(jd42[i])

coords42 = {"JD": jd42}
pandas.DataFrame(data=coords42)


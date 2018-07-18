from pyuvdata import UVData
import numpy as np
from itertools import compress
import ephem


#Specifying path to the Moon location file
path55 = '/data6/HERA/data/2458055/zen.2458055.20754.xx.HH.uv'
uvd = UVData()
uvd.read_miriad(path55)

#Storing LSTSs in list for easy access
lst55 = uvd.lst_array
#print len(np.unique(uvd.time_array))

#Checking LSTSs and length of list
#print "The LSTs for 2458055.20754 are:", lst55
#print len(lst55)



#Specifying path to a file w/o the Moon with matching LSTs
path42 = '/data6/HERA/data/2458042/zen.2458042.16280.xx.HH.uv'
uvd2 = UVData()
uvd2.read_miriad(path42)

#Checking LSTSs and length of list
lst42 = uvd2.lst_array
#print len(lst42)

#print "The LSTs for 2458028 are:", lst42

#Setting up for loops for boolean selection list
bool_list55 = []
for i in lst55:
    if i <= lst42[0]:
        bool_list55.append(False)
    else:
        bool_list55.append(True)
        
bool_list42 =[]
for j in lst42:
    if j > lst55[-1]:
        bool_list42.append(False)
    else:
        bool_list42.append(True)

#print bool_list55
#print bool_list42


#Selecting out data from LST list
selection55 = list(compress(lst55, bool_list55))
selection42 = list(compress(lst42, bool_list42))

#print "First entry of lst55:", selection55[0], "Last entry of lst55:", selection55[-1], "with length of:", len(selection55)
#print "First entry of lst42:", selection42[0], "Last entry of lst42:", selection42[-1], "with length of:", len(selection42)


#Selecting times from time array ussing the boolean list
selecttime55 = list(compress(uvd.time_array, bool_list55))
selecttime42 = list(compress(uvd2.time_array, bool_list42))

#Checking selections and their length
#print "First entry of selecttime55:", selecttime55[0], "Last entry of selecttime55:", selecttime55[-1], "with length of:", len(selecttime55)
#print "First entry of selecttime42:", selecttime42[0], "Last entry of selecttime42:", selecttime42[-1], "with length of:", len(selecttime42)
#print len(np.unique(selecttime55))



#print "Before selection, the length of uvd time array is:",len(uvd.time_array)
#print "Before selection, the length of uvd2 time array is:",len(uvd2.time_array)

selecttime55 = np.unique(selecttime55)
selecttime42 = np.unique(selecttime42)

#Editing the uvd times with our time selection list
#uvd.select(times=selecttime55)
#uvd2.select(times=selecttime42)

#print "After selection, the length of uvd time array is:",len(uvd.time_array)
#print "After selection, the length of uvd2 time array is:",len(uvd2.time_array)
#print len(np.unique(uvd.time_array))


#Finding zenith RA and dec for file w/ Moon
zenithdec = uvd.zenith_dec[len(selecttime55)/2]
zenithra = uvd.zenith_ra[len(selecttime55)/2]
print "Zenith Dec:", zenithdec, "Zenith RA", zenithra

#Phasing files to the same zenith RA and dec
#uvd.phase(zenithra,zenithdec,ephem.J2000)
#uvd2.phase(zenithra,zenithdec,ephem.J2000)

#Changing to appropriate directory
#cd /data6/HERA/HERA_imaging/jeanimport/

#Writing out the updated files to uvfits
#uvd.write_uvfits("805512552.uvfits", spoof_nonessential=True)
#uvd2.write_uvfits("804216280.uvfits", spoof_nonessential=True)


from __future__ import print_function, absolute_import, unicode_literals
import numpy as np
import glob
import os
import sys
import subprocess
import pdb
from astropy.io import fits


# This script assumes you have run photometry using pydolphot

# this function makes symbolic links of all revelant image files needed to allow DOLPHOT to run in parallel
def rename(base, nimages, nfakeruns):
	for i in range(1,nfakeruns):
		for j in range(1,nimages):	
			subprocess.call("ln -s " +base+"."+np.str(j)+".res.fits", base+"_"+np.str(i)+"."+np.str(j)+".res.fits", shell=True)
			subprocess.call("ln -s " +base+"."+np.str(j)+".psf.fits", base+"_"+np.str(i)+"."+np.str(j)+".psf.fits", shell=True)
		subprocess.call("ln -s " +base+".info", base+"_"+np.str(i)+".info", shell=True)
		subprocess.call("ln -s " +base+".psfs", base+"_"+np.str(i)+".psfs", shell=True)
		subprocess.call("ln -s " +base+".info", base+"_"+np.str(i)+".columns", shell=True)
		subprocess.call("ln -s " +base, base+"_"+np.str(i), shell=True)

# uses DOLPHOT utility fakelist to generate lists of ASTs for nimages
# color and magnitude limits are currently hardcoded
def makefakelist(base, nimages, filter1='ACS_F606W', filter2='ACS_F814W', min_mag=18., max_mag=29., min_color=-1, max_color=3., nstar=10000):
	for i in range(1, nimages):
		subprocess.call("fakelist " +base+" "filter1+" "+filter2+" "+np.str(mag_min)+" "+np.str(mag_max)+" "+np.str(cmin)+" "+np.str(cmax)+" -nstar="+np.str(nstar)+" > fake.list_"+np.str(i)


# assume current directory is where ASTs will be exectued
astdir = os.getcwd()

# name of raw photometry file
rawphotname = sys.argv[1]

# name of photometry parameter file
photparamname = sys.argv[2]

# define number of parallel fake star runs
nfakeruns = np.int(sys.argv[3])

# define number of fakestars per file
nast = np.int(sys.argv[4])

# number of images on which photometry was run (would be nice to automatically detect this)
nimages = np.int(sys.argv[5])


#use DOLPHOT naming convention, e.g., ACS_F606W, WFPC2_F555W
# only works for 2 filters at the moment
# should be in the form 'ACS_F606W ACS_F814W'
filters = sys.argv([5]).split()


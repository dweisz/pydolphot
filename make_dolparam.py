import numpy as np
import glob
import os
import sys
import subprocess
import pdb
from astropy.io import fits


def gen_params(paramfile):
	params = {'photsec': '',
		'RCentroid': 1,
		'SigFind': 2.5,
		'SigFindMult': 0.85,
		'SigFinal': 3.5,
		'MaxIT': 25,
		'PSFPhot': 1,
		'PSFPhotIt': 1,
		'FitSky': 2,
		'SkipSky': 2,
		'SkySig': 2,
		'NegSky': 0,
		'NoiseMult': 0.1,
		'Fsat': 0.999,
		'PosStep': 0.1,
		'dPosMax': 2.5,
		'RCombine': 1.415,
		'SigPSF': 3.0,
		'UseWCS': 1,
		'Align': 2,
		'AlignIter': 2,
		'AlignTol': 0,
		'AlignStep': 2,
		'AlignOnly': 0,
		'Rotate': 1,
		'SubResRef': 1,
		'SecondPass': 5,
		'SearchMode': 1,
		'Force1': 0,
		'PSFres': 1,
		'psfstars': '',
		'psfoff': 0.0,
		'ApCor': 1,
		'UsePhot': '',
		'DiagPlotType': 'PS',
		'xytfile': '',
		'xytpsf': '',
		'VerboseData': 0
		}

	param_comments = {'photsec': '#section: group, chip, (X,Y)0, (X,Y)',
		'RCentroid': '#centroid box size (int>0)',
		'SigFind': '#sigma detection threshold (flt)',
		'SigFindMult': '#Multiple for quick-and-dirty photometry (flt>0)',
		'SigFinal': '#sigma output threshold (flt)',
		'MaxIT': '#maximum iterations (int>0)',
		'PSFPhot': '#photometry type (int/0=aper,1=psf,2=wtd-psf)',
		'PSFPhotIt': '#number of iterations in PSF-fitting photometry (int>=0)',
		'FitSky': '#fit sky? (int/0=no,1=yes,2=small,3=with-phot)',
		'SkipSky': '#spacing for sky measurement (int>0)',
		'SkySig': '#sigma clipping for sky (flt>=1)',
		'NegSky': '#allow negative sky values? (0=no,1=yes)',
		'NoiseMult': '#noise multiple in imgadd (flt)',
		'Fsat': '#fraction of saturate limit (flt)',
		'PosStep': '#search step for position iterations (flt)',
		'dPosMax': '#maximum single-step in position iterations (flt)',
		'RCombine': '#minimum separation for two stars for cleaning (flt)',
		'SigPSF': '#min S/N for psf parameter fits (flt)',
		'UseWCS': '#use WCS info in alignment (int 0=no, 1=shift/rotate/scale, 2=full)',
		'Align': '#align images? (int 0=no,1=const,2=lin,3=cube)',
		'AlignIter': '#number of iterations on alignment? (int>0)',
		'AlignTol': '#number of pixels to search in preliminary alignment (flt>=0)',
		'AlignStep': '#stepsize for preliminary alignment search (flt>0)',
		'AlignOnly': '#exit after alignment',
		'Rotate': '#allow cross terms in alignment? (int 0=no, 1=yes)',
		'SubResRef': '#subpixel resolution for reference image (int>0)',
		'SecondPass': '#second pass finding stars (int 0=no,1=yes)',
		'SearchMode': '#algorithm for astrometry (0=max SNR/chi, 1=max SNR)',
		'Force1': '#force type 1/2 (stars)? (int 0=no,1=yes)',
		'PSFres': '#make PSF residual image? (int 0=no,1=yes)',
		'psfstars': '#Coordinates of PSF stars',
		'psfoff': '#coordinate offset (PSF system - dolphot system)',
		'ApCor': '#find/make aperture corrections? (int 0=no,1=yes)',
		'UsePhot': '#if defined, use alignment, PSF, and aperture corr from photometry',
		'DiagPlotType': '#format to generate diagnostic plots (PNG, GIF, PS)',
		'xytfile': '#position file for warmstart (str)',
		'xytpsf': '#reference PSF for image subtraction',
		'VerboseData': '#to write all displayed numbers to a .data file'
		}

	file = open(paramfile, 'a')

	file.write("\n")

	for i, j in enumerate(params.keys()):
		file.write(j + " = " + np.str(params[j]) + "\t \t" + param_comments[j] + "\n")

	file.close()



def fake_params(paramfile):

	params = {'FakeStars': '',
					'FakeOut=': '',
					'FakeMatch': 3.0,
					'FakePSF': 2.0,
					'FakeStarPSF': 1,
					'RandomFake': 1,
					'FakePad': 0,
					}

	param_comments = {'FakeStars': '#file with fake star input data',
					'FakeOut=': '#file with fake star output data (default=phot.fake)',
					'FakeMatch': '#maximum separation between input and recovered star (flt>0)',
					'FakePSF': '#assumed PSF FWHM for fake star matching',
					'FakeStarPSF': '#use PSF residuals in fake star tests? (int 0=no,1=yes)',
					'RandomFake': '#apply Poisson noise to fake stars? (int 0=no,1=yes)',
					'FakePad': '#minimum distance of fake star from any chip edge to be used',
					}
	file = open(paramfile, 'a')

	file.write("\n")

	for i, j in enumerate(params.keys()):
		file.write(j + " = " + np.str(params[j]) + "\t \t" + param_comments[j] + "\n")

	file.close()


def hst_params(paramfile):
	params = {'ForceSameMag': 0,
					'FlagMask': 4,
					'WFPC2useCTE': 0,
					'ACSuseCTE': 0,
					'WFC3useCTE': 0,
					'ACSpsfType': 1,
					'WFC3UVISpsfType': 1,
					'WFC3IRpsfType': 1,
					'InterpPSFlib': 1
					}

	param_comments = {'ForceSameMag': '#force same count rate in images with same filter? (int 0=no, 1=yes)',
					'FlagMask': '#photometry quality flags to reject when combining magnitudes',
					'WFPC2useCTE': '#apply CTE corrections on WFPC2 data? (int 0=no, 1=yes)',
					'ACSuseCTE': '#apply CTE corrections on ACS data? (int 0=no, 1=yes)',
					'WFC3useCTE': '#apply CTE corrections on WFC3 data? (int 0=no, 1=yes)',
					'ACSpsfType': '#use Anderson PSF cores? (int 0=no, 1=yes)',
					'WFC3UVISpsfType': '#use Anderson PSF cores? (int 0=no, 1=yes)',
					'WFC3IRpsfType': '#use Anderson PSF cores? (int 0=no, 1=yes)',
					'InterpPSFlib': '#interpolate PSF library spatially'
					}
	file = open(paramfile, 'a')

	file.write("\n")

	for i, j in enumerate(params.keys()):
		file.write(j + " = " + np.str(params[j]) + "\t \t" + param_comments[j] + "\n")

	file.close()

def rename_acs_fits(files):
	newname_store = []
	f1_store = []
	f2_store = []
	for i in range(len(files)):
		hdu = fits.open(files[i])
		f1 = hdu[0].header['filter1']
		f2 = hdu[0].header['filter2']
		name = files[i].split('_')
		if ((f1 == 'CLEAR1L') | (f1 == 'CLEAR1S') ):
			filter2 = f2.swapcase()
			newname = name[0]+'_'+filter2+'_'+name[1]
			f2_store.append(filter2)
		elif ((f2 == 'CLEAR2L') | (f2 == 'CLEAR2S')):
			filter1 = f1.swapcase()
			newname = name[0]+'_'+filter1+'_'+name[1]
			f1_store.append(filter1)
		newname_store.append(newname)
		hdu.writeto(newname)
	# only works for 2 filters for right now
	return f1_store[0], f2_store[0], newname_store


def rename_uvis_fits(files):
	newname_store = []
	f1_store = []
	for i in range(len(files)):
		hdu = fits.open(files[i])
		f1 = hdu[0].header['filter']
		name = files[i].split('_')
		filter = f1.swapcase()
		newname = name[0]+'_'+filter+'_'+name[1]
		f1_store.append(filter)
		newname_store.append(newname)
		hdu.writeto(newname)
	# only works for 2 filters for right now
	return f1_store[0], newname_store



def makesky(files):
	for i in files:
		subprocess.call("calcsky "+ i.replace('.fits', '') +"  15 35 -128 2.25 2.00 >> " + log_file, shell=True)

def img_param(reference, images, paramfile):
	file = open(paramfile, 'w')
	# number of total images
	file.write("Nimg = " + np.str(len(images)) + "\n")

	# reference image
	file.write("img0_file = " + reference[0].split('.fits')[0] + "\n")
	file.write("img0_shift = " + "0 0"  + "\n" )
	file.write("img0_xform = " + "1 0 0" + "\n")
	file.write("img0_raper = " + "3"  + "\n" )
	file.write("img0_rchi = " + "2.0" + "\n")
	file.write("img0_rsky0 = " + "15" + "\n")
	file.write("img0_rsky1 = " + "35" + "\n")
	file.write("img0_rpsf = " + "10" + "\n")

	# individual image information
	for k,j in enumerate(images):
		file.write("img"+np.str(k+1)+'_file = ' + j.split('.fits')[0]  + "\n")
		file.write("img"+np.str(k+1)+'_shift = ' + "0 0"  + "\n")
		file.write("img"+np.str(k+1)+'_xform = ' + "1 0 0"  + "\n")	
		file.write("img"+np.str(k+1)+'_raper = ' + "3"  + "\n")
		file.write("img"+np.str(k+1)+'_rchi = ' + "2.0"  + "\n")	
		file.write("img"+np.str(k+1)+'_rsky0 = ' + "15"  + "\n")
		file.write("img"+np.str(k+1)+'_rsky1 = ' + "35"  + "\n")
		file.write("img"+np.str(k+1)+'_rpsf = ' + "10"  + "\n")	
	file.close()

'''
def make_param(files, paramfile_name='phot.param'):
	name = np.loadtxt('temp1', dtype="string")

	newname = np.chararray(len(name), itemsize=40)

	for i in range(len(name)):
		newname[i] = name[i].replace('.fits', '')

	print "Nimg =", len(name)-1

	for i in range(len(name)):
		print "img"+np.str(i)+"_file = ", newname[i]
		print "img"+np.str(i)+"_shift = 0 0"
		print "img"+np.str(i)+"_xform = 1 0 0"
'''

# current working directory
# this is where we will run DOLPHOT

current_dir = os.getcwd()

# assume all images are kept in cwd/raw
raw_dir = current_dir+'/raw/'


# define reference file
ref_file = sys.argv[1]
log_file = 'phot.log'
param_file = 'phot.param'
camera = sys.argv[2]

# remove old files
subprocess.call("rm -rf *.fits " + param_file+" "+log_file, shell=True)

# reference image type
ref_extension = ['drc', 'drz']

for i, j in enumerate(ref_extension):
	rawfiles = glob.glob(raw_dir+'*'+j+'*')
	if not rawfiles:
		pass
	else:
		ref_ext = j
		break


# ACS files that we want in order of preference
file_extentions = ['crc', 'flc', 'crj', 'flt']

# check directory for various possible ACS image types in order of preference
for i, j in enumerate(file_extentions):
	rawfiles = glob.glob(raw_dir+'*'+j+'*')
	if not rawfiles:
		pass
	else:
		file_ext = j
		break

# if no files are found, quit
if not rawfiles:
	raise IOError('No ACS images found')



# copy reference and indivudal ACS images with file_ext to current directory
subprocess.call("cp " + raw_dir+ref_file+" "+current_dir, shell=True)
subprocess.call("cp " + raw_dir+"*"+file_ext+"* "+current_dir, shell=True)

filenames = [j.replace(raw_dir, "") for j in rawfiles] 


# check to see if the files are gzipped
if ref_file.split(".")[-1] == 'gz':
	subprocess.call("gunzip " + ref_file, shell=True)
for i in filenames:
	if i.split(".")[-1] == 'gz':
		subprocess.call("gunzip " + i, shell=True)
# remove any old log file
subprocess.call("rm -rf " + log_file, shell=True)

# run acsmask on all fits files and create dolphot logfile
if camera == 'acs':
	subprocess.call("acsmask *.fits > " + log_file, shell=True)

if camera =='uvis':
	subprocess.call("wfc3mask *.fits > " + log_file, shell=True)

# run splitgroups on all fits files and append to dolphot logfile
subprocess.call("splitgroups *.fits > " + log_file, shell=True)


# gets files run through acsmask / splitgroups -- assumes all went OK
currentfiles = glob.glob("*chip?*")

# add filternames to files

if camera == 'acs':
	f1, f2, newfilenames = rename_acs_fits(currentfiles)

if camera == 'uvis':
	f1, newfilenames = rename_uvis_fits(currentfiles)

# separate reference image and other images

# run calcsky

makesky(newfilenames)

ref_name = [x for x in newfilenames if ref_ext in x]
img_names = [x for x in newfilenames if not ref_ext in x]

img_param(ref_name, img_names, param_file)
gen_params(param_file)
hst_params(param_file)













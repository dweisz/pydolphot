from __future__ import print_function, absolute_import, unicode_literals
import numpy as np
import glob
import os
import sys
import subprocess
import pdb
from astropy.io import fits



# currently assumes *all* relevant fits files are in the same raw directory
def load_files(ref_file,rawdir='raw/', log_file='phot.log', param_file='phot.param'):

	# remove old fits, parameter files
	subprocess.call("rm -rf *.fits " + param_file+" "+log_file, shell=True)

	rawfiles = glob.glob(rawdir+'/*fits*')
	filenames = [j.replace(rawdir, "") for j in rawfiles]

	# get rid of drz or drc files from rawlist
	img_names = [x for x in filenames if not 'drc' in x]
	img_names = [x for x in img_names if not 'drz' in x]
	
	if not rawfiles:
		raise IOError('No images found')

	#copy images from raw into working directory
	for i in img_names:
		subprocess.call("cp " +rawdir+i+" "+ os.getcwd(), shell=True)

	# copy reference files from raw into working directory
	subprocess.call("cp " +rawdir+ref_file+" "+ os.getcwd(), shell=True)

	# check if they're zipped, and if so, unzip them
	if ref_file.split(".")[-1] == 'gz':
		subprocess.call("gunzip " + ref_file, shell=True)
		ref_file = ref_file.strip(".gz")
	for i,j in enumerate(img_names):
		if j.split(".")[-1] == 'gz':
			subprocess.call("gunzip " + j, shell=True)
			img_names[i] = j.strip(".gz")

	acs_list, wfc3_list, wfpc2_list = [], [], []

	# read 
	for i,j in enumerate(img_names):
		hdu = fits.open(j)
		temp = hdu[0].header['INSTRUME']
		if temp == 'WFC3':
			wfc3_list.append(j)
		if temp == 'ACS':
			acs_list.append(j)
		if temp == 'WFPC2':
			wfpc2_list.append(j)

	return acs_list, wfc3_list, wfpc2_list, [ref_file]


def proc_acs(files, log_file='phot.log', ref=False):

	# rename files to include filter name
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
		hdu.writeto(newname, clobber=True)


	# run acsmask on all ACS files
	splitnames = []
	for j in newname_store:
		subprocess.call("acsmask " + j + " > " + log_file, shell=True)
		subprocess.call("splitgroups " + j + " > " + log_file, shell=True)
		if ref == True:
			subprocess.call("calcsky "+ j.replace('.fits', '.chip1') +"  15 35 -128 2.25 2.00 >> " + log_file, shell=True)
			splitnames.append(j.replace('.fits', '.chip1.fits'))
		elif ref == False:
			subprocess.call("calcsky "+ j.replace('.fits', '.chip1') +"  15 35 -128 2.25 2.00 >> " + log_file, shell=True)
			splitnames.append(j.replace('.fits', '.chip1.fits'))
			subprocess.call("calcsky "+ j.replace('.fits', '.chip2') +"  15 35 -128 2.25 2.00 >> " + log_file, shell=True)
			splitnames.append(j.replace('.fits', '.chip2.fits'))
	# only works for 2 filters for right now
	return splitnames



def proc_wfc3(files, log_file='phot.log', ref=False):

	# rename files to include filter name
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
		hdu.writeto(newname, clobber=True)

	# run wfc3mask on all WFC3 files
	splitnames = []
	for j in newname_store:
		subprocess.call("wfc3mask " + j + " > " + log_file, shell=True)
		subprocess.call("splitgroups " + j + " > " + log_file, shell=True)
		if ref == True:
			subprocess.call("calcsky "+ j.replace('.fits', '.chip1') +"  15 35 -128 2.25 2.00 >> " + log_file, shell=True)
			splitnames.append(j.replace('.fits', '.chip1.fits'))
		elif ref == False:
			subprocess.call("calcsky "+ j.replace('.fits', '.chip1') +"  15 35 -128 2.25 2.00 >> " + log_file, shell=True)
			splitnames.append(j.replace('.fits', '.chip1.fits'))
			subprocess.call("calcsky "+ j.replace('.fits', '.chip2') +"  15 35 -128 2.25 2.00 >> " + log_file, shell=True)
			splitnames.append(j.replace('.fits', '.chip2.fits'))
	# only works for 2 filters for right now
	return splitnames

def proc_wfpc2(files, log_file='phot.log'):
	newname_store = []
	f1_store = []
	f2_store = []
	for i in range(len(files)):
		hdu = fits.open(files[i])
		f1 = hdu[0].header['FILTNAM1']
		f2 = hdu[0].header['FILTNAM2']
		name = files[i].split('_')
		if (f1 != ''):
			filter1 = f1.swapcase()
			newname = name[0]+'_'+filter1+'_'+name[1]
			f1_store.append(filter1)
		elif (f2 != ''):
			filter2 = f2.swapcase()
			newname = name[0]+'_'+filter2+'_'+name[1]
			f2_store.append(filter2)
		newname_store.append(newname)
		hdu.writeto(newname, clobber=True)
	# only works for 2 filters for right now

	# run acsmask on all WFPC2 files
	splitnames = []
	for j in newname_store:
		subprocess.call("wfpc2mask " + j + " > " + log_file, shell=True)
		subprocess.call("splitgroups " + j + " > " + log_file, shell=True)
		subprocess.call("calcsky "+ j.replace('.fits', '.chip1') +"  15 35 -128 2.25 2.00 >> " + log_file, shell=True)
		subprocess.call("calcsky "+ j.replace('.fits', '.chip2') +"  15 35 -128 2.25 2.00 >> " + log_file, shell=True)
		splitnames.append(j.replace('.fits', '.chip1.fits'))
		splitnames.append(j.replace('.fits', '.chip2.fits'))
	# only works for 2 filters for right now
	return splitnames


# write out DOLPHOT params for reference image

def ref_params(reference, paramfile):

	file = open(paramfile, 'a')
	file.write("img0_file = " + reference[0].split('.fits')[0] + "\n")
	file.write("img0_shift = " + "0 0"  + "\n" )
	file.write("img0_xform = " + "1 0 0" + "\n")
	file.close()


# write out DOLPHOT parameters for individual images
def image_params(images, img_num, camera, paramfile):
	k = img_num

	acs_params = {
		'raper': '3',
		'rchi': '1.0',
		'rsky0': '15',
		'rsky1': '35',
		'rpsf': '10',
		'apsky': '15 25',
		'shift': '0 0',
		'xform': '1 0 0'
		}

	uvis_params = { 
		'raper': '3',
		'rchi': '1.0',
		'rsky0': '15',
		'rsky1': '35',
		'rpsf': '10',
		'apsky': '15 25',
		'shift': '0 0',
		'xform': '1 0 0'
		}

	ir_params = {
		'raper': '2',
		'rchi': '1.5',
		'rsky0': '8',
		'rsky1': '20',
		'rpsf': '10',
		'apsky': '15 25',
		'shift': '0 0',
		'xform': '1 0 0'
		}

	wfpc2_params = {
		'raper': '2',
		'rchi': '1.5',
		'rsky0': '8',
		'rsky1': '20',
		'rpsf': '10',
		'apsky': '15 25',
		'shift': '0 0',
		'xform': '1 0 0'
		}

	if camera.lower() == 'acs':
		params = acs_params
	if camera.lower() == 'uvis':
		params = uvis_params
	if camera.lower() == 'ir':
		params = ir_params
	if camera.lower() == 'wfpc2':
		params = wfpc2_params

	file = open(paramfile, 'a')

	for j in images:
		file.write("img"+np.str(k)+'_file = ' + j.split('.fits')[0]  + "\n")
		k+=1
	file.write("\n")
	file.close()
	file = open(paramfile, 'a')
	k=1 # reset image counter
        for j in images:
                file.write("img"+np.str(k)+'_shift = ' + params['shift'] + "\n")
                file.write("img"+np.str(k)+'_xform = ' + params['xform']  + "\n")
                file.write("img"+np.str(k)+'_raper = ' + params['raper'] + "\n")
                file.write("img"+np.str(k)+'_rchi = ' + params['rchi']  + "\n")
                file.write("img"+np.str(k)+'_rsky0 = ' + params['rsky0']  + "\n")
                file.write("img"+np.str(k)+'_rsky1 = ' + params['rsky1']  + "\n")
                file.write("img"+np.str(k)+'_rpsf = ' + params['rpsf']  + "\n")
                file.write("img"+np.str(k)+'_apsky = ' + params['apsky']  + "\n")
                k+=1
	file.write("\n")
        file.close()
	

def dolparams(paramfile):
	# need to add WFPC2 data
	# should automatically adjust values according to image types
	dolphot_params = {
	'RAper': 3,
	'Rchi': 3.0,
	'PSFPhot': 1,
	'FitSky': 2,
	'RSky0': 15,
	'RSky1': 35,
	'SkipSky': 2,
	'SkySig': 2.25,
	'SecondPass': 5,
	'SearchMode': 1,
	'SigFind': 2.5,
	'SigFindMult':0.85,
	'SigFinal': 3.5,
	'SubResRef': 1,
	'MaxIT': 25,
	'NoiseMult': 0.10,
	'FSat': 0.999,
	'FlagMask': 4,
	'ApCor': 1,
	'Force1': 1,
	'Align': 2,
	'Rotate': 1,
	'RCentroid': 1,
	'PosStep': 0.25,
	'dPosMax': 2.5,
	'RCombine': 3.0,
	'RPSF': 10,
	'SigPSF': 5.0,
	'PSFres': 1,
	'psfoff': 0.0,
	'DiagPlotType': 'PS',
	'UseWCS': 1,
	'ACSpsfType': 0,
	'ACSuseCTE': 0,
	'WFC3UVISpsfType': 0,
	'WFC3IRpsfType': 0,
	'WFC3useCTE': 0,
	'CombineChi': 1,
	'#FakeStars': 'fake.list',
	'#FakeMatch': 3.0,
	'#FakeStarPSF': 1.5,
	'#RandomFake':1
	}

	file = open(paramfile, 'a')
	for i in dolphot_params.keys():
    		file.write(i+ ' = ' +np.str(dolphot_params[i])+"\n")
    file.close()



ref = sys.argv[1]
log_file = 'phot.log'
param_file = 'phot.param'

# load in HST images
acs_list, wfc3_list, wfpc2_list, ref_list = load_files(ref)


# process acs, wfc3, and wfpc2 files
acs_files = proc_acs(acs_list)

wfc3_files = proc_wfc3(wfc3_list)
wfpc2_files = proc_wfpc2(wfpc2_list)

# separate wfc3_ir and wfc3_uvis
wfc3_ir_files, wfc3_uvis_files = [], []
if wfc3_files:
	for i in wfc3_files:
		hdu = fits.open(i)
		temp = hdu[0].header['DETECTOR']
		if temp == 'UVIS':
			wfc3_uvis_files.append(i)
		if temp == 'IR':
			wfc3_ir_files.append(i)



# process reference file
hdu = fits.open(ref_list[0])
temp = hdu[0].header['INSTRUME']
if temp == 'WFC3':
	ref_file = proc_wfc3(ref_list, ref=True)
if temp == 'ACS':
	ref_file = proc_acs(ref_list, ref=True)
if temp == 'WFPC2':
	ref_file = proc_wfpc2(ref_list)


'''  write out paramter file '''

number_images = len(acs_files) + len(wfc3_files) + len(wfpc2_files)


# write number of images
file = open(param_file, 'w')
file.write("Nimg = " + np.str(number_images) + "\n")
file.close()

# add reference file info

ref_params(ref_file, param_file)

# start counter for image numbers
k=1

if acs_files:
	image_params(acs_files, k, 'acs', param_file)
	k += len(acs_files)
	

if wfc3_uvis_files:
	image_params(wfc3_uvis_files, k, 'uvis', param_file)
	k += len(wfc3_uvis_files)
	

if wfc3_ir_files:
	image_params(wfc3_ir_files, k, 'ir', param_file)
	k += len(wfc3_ir_files)
	

if wfpc2_files:
	image_params(wfpc2_files, k, 'wfpc2', param_file)
	k += len(wfpc2_files)
	

# add gloal dolphot parameters

dolparams(paramfile)




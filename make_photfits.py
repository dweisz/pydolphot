import numpy as np
import sys
import astropy.table
from astropy import units as u
from astropy.io import fits
from astropy import wcs
import pdb
import pylab as plt

''' Uses astropy tables to translate raw DOLPHOT photometric catalogs into summary .fits files '''

def syntax():
	print("make_photfits.py <raw dolphot photometry file>, <output filename>,  'filter1 fitler2, ...', <reference .fits filename>")


def make_phot(datafile, refname, filters, outname, full=False, summary=True, gst=True):
	
	# no functionality for full photometry output yet
	# currently assumes only 2 filters present

	# relevant output labels
	global_labels = ['Number', 'RA', 'DEC', 'X', 'Y', 'OBJECT_TYPE']
	filter_labels = ['_VEGA', '_ERR', '_SNR', '_SHARP', '_ROUND', '_CROWD', '_FLAG']
	formats = ['f8', 'f8', 'f8', 'f8', 'f8', 'f8', 'f8'] 
	
	filters = filters.split()
	nfilters = len(filters)

	# load raw DOLPHOT photometry
	print('Loading raw DOLPHOT file...')
	data = np.loadtxt(datafile)
	print('Loaded {0} objects'.format(len(data[:,0])))


	# number of objects
	num = np.arange(len(data[:,0])) + 1

	# Load the FITS hdulist using astropy.io.fits
	hdulist = fits.open(refname)

	# Parse the WCS keywords in the primary HDU
	w = wcs.WCS(hdulist[1].header)

	# convert x and y to RA and DEC using WCS from reference image
	world = w.wcs_pix2world(data[:,2], data[:,3], 1)

	if summary == True:
		t = astropy.table.Table()
		t.add_column(astropy.table.Column(name=global_labels[0], data=num)) # star number
		t.add_column(astropy.table.Column(name=global_labels[1], data=world[0])) # RA
		t.add_column(astropy.table.Column(name=global_labels[2], data=world[1])) # DEC
		t.add_column(astropy.table.Column(name=global_labels[3], data=data[:,2])) # X
		t.add_column(astropy.table.Column(name=global_labels[4], data=data[:,3])) # Y
		t.add_column(astropy.table.Column(name=global_labels[5], data=data[:,10])) # ObjType

		# other relevant columns: Instrumental Mag, Err, SNR, Sharp, Round, Crowd, Flag
		cols = np.int_(np.asarray((15, 17, 19, 20, 21, 22, 23)))

		# loops over number of filters, names of filters to generate output columns
		for i in range(nfilters):
			for j, k in enumerate(filter_labels):
				t.add_column(astropy.table.Column(name=filters[i]+k, 
					data=data[:,cols[j] + (i*13) ]))

		t.write(sys.argv[1]+'.summary.fits', overwrite=True)
		

		if gst == True:

			# cull photometry on both bands
			# assumes only 2 bands for now
			snr = 5.
			sharp = 0.1
			crowd = 1.0
			objtype = 1

			wgood = np.where( (t[filters[0]+'_SNR'] >= snr) & (t[filters[1]+'_SNR'] >= snr) &
						( (t[filters[0]+'_SHARP'] + t[filters[1]+'_SHARP'])**2 < sharp ) &
						( (t[filters[0]+'_CROWD'] + t[filters[1]+'_CROWD']) < crowd ) &
						(t['OBJECT_TYPE'] <= objtype) )


			t1 = t[wgood]
			t1.write(sys.argv[1]+'.gst.fits', overwrite=True)
			
			'''
			plt.figure()
			plt.scatter(t[filters[0]+'_VEGA'] - t[filters[1]+'_VEGA'],t[filters[1]+'_VEGA'], color='k', edgecolor='None', s=0.5)
			plt.scatter(t1[filters[0]+'_VEGA'] - t1[filters[1]+'_VEGA'],t1[filters[1]+'_VEGA'], color='r', edgecolor='None', s=0.25)
			plt.xlim(-1,4)
			plt.ylim(30,16)
			'''








def main():
	datafile = sys.argv[1]
	outfile = sys.argv[2]
	filters = sys.argv[3]
	ref_image = sys.argv[4]
	
	make_phot(datafile, ref_image, filters, outfile)


main()



'''
t = astropy.table.Table()
t.add_column(astropy.table.Column(name=global_labels[0], data=data[:,0]))
t.add_column(astropy.table.Column(name=global_labels[1], data=data[:,1]))
t.add_column(astropy.table.Column(name=global_labels[2], data=data[:,2]))
k=3
for i in range(len(filters)):
    for j in range(len(filter_labels)):
        t.add_column(astropy.table.Column(name=filters[i]+filter_labels[j], data=data[:,k]))
        print data[:,k][-1]
        k+=1

t.write(sys.argv[1]+'.fits')
'''



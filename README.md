# pydolphot
python wrappers for DOLPHOT


This DOLPHOT example makes use of 'Grid 4' HST/ACS images from [HST-GO-12180](http://www.stsci.edu/cgi-bin/get-proposal-info?id=12180&submit=Go&observatory=HST) as presnted in [Cannon et al. (2012)](http://adsabs.harvard.edu/abs/2012ApJ...747..122C).  
Let's assume we have the raw images from the HST archive in the 'raw' subdirectory of 'NGC6822':

``` tcsh
> pwd
NGC6822
> ls
raw/
> ls/raw/
images
```

The first step is to copy the a reference image (usually a drizzled image) and all the science images (usually flt or flc images) from the raw directory to the current directory. Images will be modified by DOLPHOT and we want to preserve the originals in case its necessary to start over.

``` tcsh
> cp raw/drc .
> cp raw/*flc* .
> gunzip *.gz
> ls
images
```

The next step is to run _acsmask_ (or _wfc3mask_ or _wfpc2mask_, for WFC3 or WFPC2 images) on each of the images and store the output in a log file.  _acsmask_ masks out all pixels flagged as bad in the data quality image, and multiplies by the pixel areas so that the resulting images are approximately in units of electrons on the raw image. A masked or saturated pixel is skipped by all other DOLPHOT routines - it is not used in sky determination, photometry, aperture corrections, etc.

``` tcsh
> acsmask image1 >> phot.log
> acsmask image2 >> phot.log
> acsmask image3 >> phot.log
> ls
images
```
The next step is to run _splitgroups_, which splits the image files into each chip.  Some cameras, e.g., HST/HRC, do not have multiple chips.

``` tcsh
> splitgroups *.fits >> phot.log
> ls
images
```

The next step is to run _calcsky_ on each image for each chip.  This includes both reference and science images.  _calcsky_ creates a sky image, which depending on your DOLPHOT parameters, can either provide an initial guess of the sky map or a definitive measurement. The sky computation is made by taking all pixels in an annulus around the pixel in question. The annulus extends from **r<sub>in</sub>** to **r<sub>out</sub>** pixels from the pixel whose value is being measured, and is sampled every step pixels. While **step** = 1 will always work, one can typically set step to the PSF size and achieve equally good results.  The recommended paramters for ACS/WFC images are:

* **r<sub>in</sub>** = 15
* **r<sub>in</sub>** = 35
* **step** = -128 (for a quick estimate; 4 for a more accurate, but slower measurement)
* **sigma<sub>low</sub>** = 2.25
* **sigma<sub>low</sub>** = 2.00

``` tcsh
> calcsky 
> Usage: calcsky <fits base> <inner radius> <outer radius> <step> <lower sigma> <upper sigma>
> calcsky fitsbase 15 35 -128 2.25 2.00 >> phot.log
> calcsky fitsbase 15 35 -128 2.25 2.00 >> phot.log
> calcsky fitsbase 15 35 -128 2.25 2.00 >> phot.log
> calcsky fitsbase 15 35 -128 2.25 2.00 >> phot.log
> ls
images
```

Running _calcsky_ completes the preprocessing steps and now we can run DOLPHOT.  
The first step for running DOLPHOT is setting up a parameter file (called 'phot.param' in this case). In this example, I'll show you and already constructed parameter file. 

First part of the DOLPHOT parameter file is specifying the reference and science images.

``` tcsh
> more phot.param 

Nimg = 4 # specifies the number of science images
img0_file = jcnb01020_f814w_drc.chip1 # reference image
img0_shift = 0 0  # shift in (x,y) pixels wrt to reference image. Should be set for reference image.
img0_xform = 1 0 0 # scale ratio, cubic distortion, and rotation of the image relative to the reference image. Should be set for reference image.
img1_file = jcnb01lyq_f475w_flc.chip1
img1_shift = 0 0
img1_xform = 1 0 0
img2_file = jcnb01lyq_f475w_flc.chip1
img2_shift = 0 0
img2_xform = 1 0 0
img3_file = jcnb01lyq_f475w_flc.chip1
img3_shift = 0 0
img3_xform = 1 0 0
img4_file = jcnb01lyq_f475w_flc.chip1
img4_shift = 0 0
img4_xform = 1 0 0


images
```









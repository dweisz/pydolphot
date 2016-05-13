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

The next step is to run _calcsky_ on each image for each chip.  This includes both reference and science images.  _calcsky_ creates a sky image, which depending on your DOLPHOT parameters, can either provide an initial guess of the sky map or a definitive measurement. The sky computation is made by taking all pixels in an annulus around the pixel in question. The annulus extends from **rin** to **rout** pixels from the pixel whose value is being measured, and is sampled every step pixels. While **step = 1** will always work, one can typically set step to the PSF size and achieve equally good results.  The recommended paramters for ACS/WFC images are:

* **rin** = 15




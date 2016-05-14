# pydolphot
A set of python scripts to streamline running DOLPHOT on HST imaging.


This DOLPHOT example makes use of 'Grid 4' HST/ACS images from [HST-GO-12180](http://www.stsci.edu/cgi-bin/get-proposal-info?id=12180&submit=Go&observatory=HST) as presnted in [Cannon et al. (2012)](http://adsabs.harvard.edu/abs/2012ApJ...747..122C).  Let's assume we have the raw images from the HST archive in the 'raw' subdirectory of 'NGC6822':

``` tcsh
> pwd
/home/astro/photometry/NGC6822
> ls
raw/
> ls/raw/
jbin02011_drc.fits.gz  jbin02exq_drc.fits.gz  jbin02ezq_drc.fits.gz  jbin02f1q_drc.fits.gz  jbin02f4q_drc.fits.gz
jbin02021_drc.fits.gz  jbin02exq_flc.fits.gz  jbin02ezq_flc.fits.gz  jbin02f1q_flc.fits.gz  jbin02f4q_flc.fits.gz
```  

I'll walk through two examples with the same data: running DOLPHOT manually and running DOLPHOT with _pydolphot_. If you're a new user to DOLPHOT, it's important that you learn to use DOLPHOT manually in order to understand what happens under the hood of _pydolphot_ and when you inevitably need to troubleshoot.


#### Running DOLPHOT manually 

The first step is to copy the a reference image (usually a drizzled image) and all the science images (usually flt or flc images) from the raw directory to the current directory. Images will be modified by DOLPHOT and we want to preserve the originals in case its necessary to start over.

``` tcsh
> cp raw/jbin02021_drc.fits.gz .
> cp raw/*flc* .
> gunzip *.gz
> ls
jbin02021_drc.fits jbin02exq_flc.fits  jbin02ezq_flc.fits  jbin02f1q_flc.fits  jbin02f4q_flc.fits  raw/
```

The next step is to run _acsmask_ (or _wfc3mask_/_wfpc2mask_, for WFC3/WFPC2 images) on each of the images and store the output in a log file.  _acsmask_ masks out all pixels flagged as bad in the data quality image, and multiplies by the pixel areas so that the resulting images are approximately in units of electrons on the raw image. A masked or saturated pixel is skipped by all other DOLPHOT routines - it is not used in sky determination, photometry, aperture corrections, etc.

``` tcsh
> acsmask jbin02021_drc.fits >> phot.log
> acsmask jbin02exq_flc.fits >> phot.log
> acsmask jbin02ezq_flc.fits >> phot.log
> acsmask jbin02f1q_flc.fits >> phot.log
> acsmask jbin02f4q_flc.fits >> phot.log
> ls
jbin02021_drc.fits jbin02exq_flc.fits  jbin02ezq_flc.fits  jbin02f1q_flc.fits  jbin02f4q_flc.fits  raw/
```
The next step is to run _splitgroups_, which splits the image files into each chip.  Some cameras, e.g., HST/HRC, do not have multiple chips.

``` tcsh
> splitgroups *.fits >> phot.log
> ls
jbin02021_drc.chip1.fits  jbin02exq_flc.fits	    jbin02f1q_flc.chip1.fits  jbin02f4q_flc.chip2.fits
jbin02021_drc.fits	  jbin02ezq_flc.chip1.fits  jbin02f1q_flc.chip2.fits  jbin02f4q_flc.fits
jbin02exq_flc.chip1.fits  jbin02ezq_flc.chip2.fits  jbin02f1q_flc.fits	      raw
jbin02exq_flc.chip2.fits  jbin02ezq_flc.fits	    jbin02f4q_flc.chip1.fits
```

The next step is to run _calcsky_ on each image for each chip.  This includes both reference and science images.  _calcsky_ creates a sky image, which depending on your DOLPHOT parameters, can either provide an initial guess of the sky map or a definitive measurement. The sky computation is made by taking all pixels in an annulus around the pixel in question. The annulus extends from **r<sub>in</sub>** to **r<sub>out</sub>** pixels from the pixel whose value is being measured, and is sampled every step pixels. While **step** = 1 will always work, one can typically set step to the PSF size and achieve equally good results.  The recommended paramters for ACS/WFC images are:

* **r<sub>in</sub>** = 15
* **r<sub>in</sub>** = 35
* **step** = -128 (for a quick estimate; 4 for a more accurate, but slower measurement)
* **sigma<sub>low</sub>** = 2.25
* **sigma<sub>high</sub>** = 2.00

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
img0_shift = 0 0  # shift in (x,y) pixels wrt to reference image. Should not be set for reference image.
img0_xform = 1 0 0 # scale ratio, cubic distortion, and rotation of the image relative to the reference image.Should not be set for reference image.
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
```

Next we have to set each of the photometry parameters for DOLPHOT.

``` tcsh
RAper = 3            #photometry apeture size (flt)
Rchi = 3.0           #chi statistic apeture size (flt)
PSFPhot = 1          #photometry type (int/0=aper,1=psf,2=wtd-psf)
FitSky = 2           #fit sky? (int/0=no,1=yes,2=small,3=with-phot)
RSky0 = 15           #inner sky radius (flt>=RAper+0.5)
Rsky1 = 35           #outer sky radius (flt>=RSky0+1)
SkipSky = 2          #spacing for sky measurement (int>0)
SkySig = 2.25        #sigma clipping for sky (flt>=1)
SecondPass = 5       #second pass finding stars (int 0=no,1=yes)
SearchMode = 1       #searching algorithm (int 0=S/N/chi,1=1/chi)
SigFind = 2.5        #sigma detection threshold (flt)
SigFindMult = 0.85   #Multiple for quick-and-dirty photometry (flt>0)
SigFinal = 3.5       #sigma output threshold (flt)
SubResRef = 1        #subpixel resolution for reference image (int>0)
MaxIT = 25           #maximum iterations (int>0)
NoiseMult = 0.10     #noise multiple in imgadd (flt)
FSat = 0.999         #fraction of saturate limit (flt)
FlagMask = 4         #Use Saturated Cores? (4 if yes)
ApCor = 1            #find/make aperture corrections? (int 0=no,1=yes)
Force1 = 1           #force type 1/2 (stars)? (int 0=no,1=yes)
Align = 2            #align images? (int 0=no,1=const,2=lin,3=cube)
Rotate = 1           #allow cross terms in alignment? (int 0=no, 1=yes)
RCentroid = 1        #centroid box size (int>0)
PosStep = 0.25       #search step for position iterations (flt)
dPosMax = 2.5        #maximum single-step in position iterations (flt)
RCombine = 3.0       #minimum separation for two stars for cleaning (flt)
RPSF = 10            #PSF size (int>0)
SigPSF = 5.0         #min S/N for psf parameter (flt)
PSFres = 1           #make PSF residual image? (int 0=no,1=yes)
psfoff = 0.0         #coordinate offset (PSF system - dolphot system)
DiagPlotType = PS    # create .ps diagnostic plots (requires pgplot)
UseWCS = 1           # use WCS from .fits headers for alignment
ACSpsfType = 0       # 0 = Tiny Tim, 1 = Anderson
InterpPSFlib = 1     #interpolate PSF library spatially
ACSuseCTE = 0        # use CTE corrections y/n = 1/0
CombineChi = 1       # weight combined photometry by chi^2 per exposure y/n = 1/0
```

With image pre-processing done and the parameter file setup, the last step is to execute DOLPHOT.  This is simply done with:


``` tcsh
> dolphot ngc6822_acs_grid4.phot -pphot.param >> phot.log &
```

where **ngc6822_acs_grid4.phot** will be the name of the output photometry file and **phot.param** is the name of the parameter file.  Note that in this instance DOLPHOT is set to run in the background.  For small image stacks (e.g., 4 images) this might be OK.  But for large image stacks, DOLPHOT can take quite some time to run, and it will lose all progress if interrupted.  It is recommended that DOLPHOT is submitted via a queue system (slurm, etc.) to a machine that is not likely to be interrupted, whenever possible.

#### Running DOLPHOT with _pydolphot_

Assuming this directory strucutre:

``` tcsh
> pwd
/home/astro/photometry/NGC6822
> ls
raw/
> ls/raw/
images
```  

_pydolphot_ provides a simpler interface that executes all the pre-processing steps and generates a DOLPHOT parameter file.

The first thing to do is clone the pydolphot repository locally, e.g.,:

``` tcsh
> pwd
/home/astro/
> git clone https://github.com/dweisz/pydolphot.git
...
> ls pydolphot/
LICENSE  README.md  make_dolparam.py  make_photfits.py
```  

usage of _pydolphot_ requires numpy, glob, and astropy in order to handle .fits files.  Other dependancies should be native to python.  To run image pre-processing and generate a parameter file:


``` tcsh
> pwd
/home/astro/photometry/NGC6822
> python ../make_dolparam.py reference_file
> ls


> dolphot ngc6822_acs_grid4.phot -pphot.param >> phot.log &
```

First, make_dolphot.param removes.fits files and exisiting parameter and log files in your directory.  It copies and unzips images on the specficied reference file and all HST science images types it finds in 'raw'. It detects the images type and runs the appropriate pixel masking routine (e.g., _acsmask_), _splitgroups_, _calcsky_, and finally generates 'phot.param'. 

I have tested it on all ACS, UVIS, WFC3/IR, and WFPC2 science files and it works. However, it is a work in progress and has bugs.  Currently, it should exectute all image pre-processing correctly and generate a parameter file.  However, expect to inspect and edit the parameter file before running DOLPHOT (e.g., make_dolparam.py currently defaults to best global parameters for ACS, doesn't generate all WFPC2 information).  Feel free to raise issues or fork the repository and fix bugs or add features.


#### DOLPHOT Output


Upon completion DOLPHOT will have added a number of files to the working directory. Most contain useful diagnostic information (e.g., PSF residuals, aperture corrections).  For now, let's focus on getting the photometry processed into a usable format.  The raw photometry is in this file:

``` tcsh
ngc6822_acs_grid4.phot
```

each row contains an entry for a single stars including photometry measured in each exposure, the global photometry solution (i.e., all exposures combined), and quality information.  Each of these values are store per column.  The column metadata is stored in:

``` tcsh
ngc6822_acs_grid4.phot.columns
```

Typically, we will want to apply cuts to the photometry based on S/N, sharpness, crowding, and perhaps other quality criteria.  This can simply be done using something like awk or through python, etc.

I have written a basic python utility, make_photfits.py' that takes the raw dolphot file and compresses it to a binary .fits file.  Currently, it only works with 2 filter photometry. To execute:


``` tcsh
> python /home/astro/pydolphot/make_photfits.py raw_photometry outputname 'F475W F814W' reference.fits
> ls

```







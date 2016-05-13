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

The second step is to run _acsmask_ (or _wfc3mask_ or _wfpc2mask_, for WFC3 or WFPC2 images) on each of the images.

``` tcsh
> acsmask image1
> acsmask image2
> acsmask image3
> ls
images
```



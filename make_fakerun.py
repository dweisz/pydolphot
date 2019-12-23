import numpy as np
import sys 
import subprocess 
import os

'''
def makephotfiles(base, nstart, nruns, nimages):
	for i in range(nstart,nstart+nruns):
		for j in range(1, nimages+1):
			subprocess.call("ln -s "+base+"."+np.str(j)+".res.fits "  + base+"_"+np.str(i)+"."+np.str(j)+".res.fits", shell=True)
			subprocess.call("ln -s "+base+"."+np.str(j)+".psf.fits " + base+"_"+np.str(i)+"."+np.str(j)+".psf.fits", shell=True)
			subprocess.call("ln -s "+base+".info " + base+"_"+np.str(i)+".info", shell=True)
			subprocess.call("ln -s "+base+".apcor " + base+"_"+np.str(i)+".apcor", shell=True)
			subprocess.call("ln -s "+base+".psfs " + base+"_"+np.str(i)+".psfs", shell=True)
			subprocess.call("ln -s "+base+".columns " + base+"_"+np.str(i)+".columns", shell=True)

		subprocess.call("ln -s "+base + " " + base+"_"+np.str(i), shell=True)
'''


def makefakelist(photfile, filter1, filter2, fmin, fmax, cmin, cmax, nruns, nstars=15000, nstart=1):
	for i in range(nstart, nstart+nruns):
		subprocess.call('fakelist '+ np.str(photfile) + ' ' + np.str(filter1) + ' ' + np.str(filter2) + ' ' + np.str(fmin) + ' ' + np.str(fmax) + ' ' + np.str(cmin) + ' ' + np.str(cmax) + ' ' + "-nstar=" + np.str(nstars) + "> fake.list_" + np.str(i), shell=True)
		subprocess.call('sleep 5', shell=True )

def makefakeparam(param_file, base, nruns, nstart=1):
	infile = param_file
	for i in range(nstart, nstart+nruns):
		fakeparam = "phot.fake_"+np.str(i)+".param"
		subprocess.call("cp "+infile+" "+fakeparam, shell=True)
		outfile = fakeparam
		f1 = open(fakeparam, 'w')
		f1.write("ACSuseCTE = 1\n")
		f1.write("WFC3useCTE = 1\n")
		f1.write("RandomFake = 1\n")
		f1.write("FakeMatch=3.0\n")
		f1.write("FakePad=0\n")
		f1.write("FakeStarPSF = 1.5\n")
		f1.write("FakeOut="+base+"_fake_"+np.str(i)+".fake\n")
		f1.write("FakeStars=fake.list_"+np.str(i)+"\n")
		f1.close()

def makerunfake(param_file, base, nruns, nstart=1):
	for i in range(nstart, nstart+nruns):
		fakeparam = "phot.fake_"+np.str(i)+".param"
		outfile = "runfake"+np.str(i)
		f = open(outfile, 'w')
		f.write("cd " + os.getcwd()+"\n")
		f.write("dolphot " + base+ " -p" + fakeparam + " >> fake.log_"+np.str(i))
		f.close()
		subprocess.call("chmod +x " + outfile, shell=True)





'''
cd /clusterfs/dweisz/photometry/leop/
dolphot leop_acs.phot_1 -pleop.fake.param_1 >> fake1.log
'''

#if __name__ == '__main__':

base = sys.argv[1]  # e.g., test.phot
#rundir = sys.argv[2]
#nimages = np.int(sys.argv[3])
#name = sys.argv[3]
param_file = sys.argv[2]  # name of photometry parameter file

nruns = np.int(sys.argv[3])

filters = sys.argv[4]

f1min = np.float(sys.argv[5])
f1max = np.float(sys.argv[6])
c1min = np.float(sys.argv[7])
c1max = np.float(sys.argv[8])

#nimages = 12
#nruns = 72

#makephotfiles(base, 1, nruns , nimages)

makefakeparam(param_file, base, nruns)

makerunfake(param_file, base, nruns)

makefakelist(base, filters.split()[0], filters.split()[1], f1min, f1max, c1min, c1max, nruns)



#main()

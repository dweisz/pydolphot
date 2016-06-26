import numpy as np
import sys
import subprocess



def makephotfiles(base, nstart, nruns, nimages):
	for i in range(nstart,nstart+nruns):
		for j in range(1,nimages):
			subprocess.call("rm -rf *.fits " + param_file+" "+log_file, shell=True)
			subprocess.call("ln -s "+base+"."+np.str(j)+".res.fits", base+"_"+np.str(i)+"."+np.str(j)+".res.fits", shell=True)
			subprocess.call("ln -s "+base+"."+np.str(j)+".psf.fits", base+"_"+np.str(i)+"."+np.str(j)+".psf.fits", shell=True)
			subprocess.call("ln -s "+base+".info", base+"_"+np.str(i)+".info", shell=True)
			subprocess.call("ln -s "+base+".apcor", base+"_"+np.str(i)+".apcor", shell=True)
			subprocess.call("ln -s "+base+".psfs", base+"_"+np.str(i)+".psfs", shell=True)
			subprocess.call("ln -s "+base+".columns", base+"_"+np.str(i)+".columns", shell=True)

		subprocess.call("ln -s "+base, base+"_"+np.str(i))

def makefakelist(nruns, nstart, photfile,filter1, filter2, fmin, fmax, cmin, cmax, nstars=100000):
	for i in range(nstart, nstart+nruns):
		subprocess.call('fakelist '+ np.str(photfile) + ' ' + np.str(filter1) + ' ' + np.str(filter2) + ' ' + np.str(fmin) + ' ' + np.str(fmax) + ' ' + np.str(cmin) + ' ' + np.str(cmax) + ' ' + "-nstar= " + np.str(nstars) + "> fake.list_" + np.str(i), shell=True)


def makefakeparam(param_file, nstart, nruns):
	infile = param_file
	for i in range(nstart, nstart+nruns):
		outfile = param_file+".fake_"+np.str(i)
		with open(infile) as f, open(outfile, 'w') as f1:
			for line in f:
				if not "ACSuseCTE" in line:
					f1.write(line)
			f1.write("ACSuseCTE = 1\n")
			f1.write("RandomFake = 1\n")
			f1.write("FakeMatch=3.0\n")
			f1.write("FakeStars=fake.list_"+np.str(i)+"\n")
		f1.close()


#if __name__ == '__main__':
makefakeparam('n4163.phot.param', 1, 5)



#main()
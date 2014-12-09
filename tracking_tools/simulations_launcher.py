# Code block that contains all the utilities to launch a simulation block

#-----------------------------------------------------------------------------------------------------------------
# LIBRARIES
#-----------------------------------------------------------------------------------------------------------------

import numpy as np
import datetime
import subprocess
import os

from uniform_distribution import calc_beam_params,gaussian, uniform_distribution_generator,write_to_file,initialize_coordinates





#-----------------------------------------------------------------------------------------------------------------
# UTILITIES
#-----------------------------------------------------------------------------------------------------------------



def make_folder(folder_name):
	'''creates the folder in which to store the input data for Sixtrack
	'''
	os.makedirs('uniform/particleset_%s' %folder_name)
	relpath = 'uniform/particleset_%s' %folder_name
	
	return relpath
	
	
	
	

def copy_SixTrack(relpath,SixTrack_folder):
	'''imports SixTrack executable
	'''
	Sixname = SixTrack_folder

	os.system('cp %s %s' %(Sixname,relpath))
	
	print ('SixTrack copied inside %s' %relpath)





def copy_forts(relpath, forts_folder, fort_n_list):
	'''imports the fort.2, fort.3 (idfor=2!!), fort.8 and fort.16 
	input files for SixTrack
	'''
	for j in fort_n_list:
		fortname = forts_folder+'/fort.'+str(j)
		os.system('cp %s %s' %(fortname,relpath))
		print ('fort.%d copied inside %s' %(j,relpath))




		
def launch_jobs(relpath, SixTrack_folder):
	'''launches SixTrack_pro in bsub through the tracking.sh script
	'''
	
	home = os.environ['PWD']

	#os.chdir(relpath)

	os.system('pwd')

	os.system('ls')

	print datetime.datetime.now().time(),' : Launching Sixtrack'

	#out = open('log_%s.log'%jobname, 'wb')

	#err = open('err_%s.log'%jobname, 'wb')

	DIR = home +'/'+ relpath

	print DIR

	os.system('chmod +x tracker.sh')

	#proc_stat = subprocess.Popen('bsub -q 8nh tracker.sh %s' %DIR, shell=True)

	#os.chdir(home)
	
	
	return home





#-----------------------------------------------------------------------------------------------------------------
# MAIN
#-----------------------------------------------------------------------------------------------------------------
	
		
def simulations_launcher_func( 	emitn, 
								energy0, 
								deltap0, 
								xp0, 
								yp0,
								sig0,
								iamp,
								eamp,
								n_samples,
								n_parts,
								wr_fr,
								SixTrack_folder,
								forts_folder,
								fort_n_list,
								folder_name, 
								beta_star,beta_stary,alpha_x,alpha_y,
								):





	start_time = datetime.datetime.now().time()
	
	print '\n\n ======= START OF USER INPUT GENERATION AND JOB LAUNCHER ====== \n\n'
	
	
	
	
	
	assert n_samples % n_parts == 0.0
	
	sigmax,sigmay, sigmapx,sigmapy, gamma_rel, beta_rel = calc_beam_params(emitn, energy0, beta_star,beta_stary, alpha_x, alpha_y)
	
	
	print 'Next step: generating uniform distribution of ',n_samples
	
	print 'distributed between ', iamp, 'and ', eamp, ' mm of radius'
	
	x, y = uniform_distribution_generator(n_samples,iamp,eamp,sigmax,sigmay)
	
	print 'Uniform distribution generated.'

	
	

	print 'Next step: calculating the Gaussian and storing its values in a file'
	
	gd = gaussian(x, y, sigmax)
	
	#gaussian_to_file(gd, filename)
	
	#print 'Gaussian distribution stored in ', filename, '.txt'
	
	
	
	
	
	print 'Next step: generation of the fort.13 with the desidered initial conditions'
	
	#---------
	xp, yp, sig, deltap, energy = initialize_coordinates(n_samples, xp0, yp0, sig0, deltap0, energy0)
	
	iter_num = int(n_samples/n_parts) # number of iterations
	
	n_file = np.arange(iter_num) # folder number
	
	for i in range(iter_num): #loop to launch SixTrack jobs in parallel, one every 30 particles i.c.s
		ii = i*n_parts
		ie = (i+1)*n_parts
		relpath = make_folder(i)
		write_to_file(x[ii:ie],y[ii:ie],xp[ii:ie],yp[ii:ie],sig[ii:ie],deltap[ii:ie],energy[ii:ie],int(n_parts),relpath)
		#copy_SixTrack(relpath,SixTrack_folder)
		copy_forts(relpath,forts_folder,fort_n_list)
		home = launch_jobs(relpath, SixTrack_folder)
		print ('job %s launched' %relpath)
	
	#----------
	print "ONGOING SIMULATION. DON'T TOUCH"
	
	#print 'Waiting for SixTrack to complete.'
	
	#proc_status.wait()
	
	print 'Launched ', iter_num, 'jobs, as shown here:\n'
	
	os.chdir(home)
	
	os.system('bjobs')
	
	
	print datetime.datetime.now().time(),': bsub run. Returning to home directory.'
	
	
	
	
	
	end_time = datetime.datetime.now().time()
	
	print 'This script was launched at ',start_time,' and terminated at',end_time
	
	
	
	
	
	print '\n ======= END OF USER INPUT GENERATION AND JOB LAUNCHER ====== \n\n'
	

	

import numpy as np
import scipy.special as ss
from math import fmod
from vecPBC import vecPBC




def ql_local(self, l):


	# Define the box dimensions
	if self.pbc==True:
		Lx = self.boxBounds[0][1] - self.boxBounds[0][0]
		Ly = self.boxBounds[1][1] - self.boxBounds[1][0]
		if self.dim==3:
			Lz = self.boxBounds[2][1] - self.boxBounds[2][0]
		else:
			Lz = None



	phi_theta = {}
	qlmtilde_neighs = {}
	unit_sph = []
	for j in self.neighs:
		if self.pbc==True:
			d = np.array(vecPBC([self.x, self.y, self.z], [self.data[j].x, self.data[j].y, self.data[j].z], Lx, Ly, Lz), dtype=np.float)

		else:
			d = np.array([self.x, self.y, self.z], dtype=np.float) - np.array([self.data[j].x, self.data[j].y, self.data[j].z], dtype=np.float)	


		mag = np.sqrt(np.sum(d**2, axis=0))
		unit = d/mag				
		
		if unit[2]!=0.0:		
			theta = np.arctan(np.sqrt(unit[0]**2 + unit[1]**2)/(unit[2]))
		else:
			theta = np.pi/2

		phi = np.arctan2(unit[1],unit[0])



		if phi<0:
			phi = np.fmod((phi+2*np.pi),2*np.pi)
		if theta<0:
			theta = np.fmod((theta+2*np.pi),np.pi)

		unit_sph.append([phi,theta])







		#----------------------------------
		# To get the qlm for the single neighbor (single bond) first

		qlmbar = []			#qlm bar--list with each element the sum of the spher harm over all neighbors divided by the number of neighbors *for a specific m value*
		qlmbar_mag_sq = []	#qlm bar magnitude squared--list with each element the magnitude squared of Ylm_sum. Used to make qlm bar into qlm tilde

		for m in range(-l,l+1):
			Ylm_sum = 0.0
			angle = unit_sph[-1]
			Ylm_sum += ss.sph_harm(m,l,angle[0],angle[1])	
			Ylm_sum_mag_sq = Ylm_sum*np.conj(Ylm_sum)
			qlmbar.append(Ylm_sum)
			qlmbar_mag_sq.append(Ylm_sum_mag_sq)

		# Normalize qlmbar to ideal particle or lattice or fall back to usual way from Frenkel
		# With this normalization, pl will be 1 if the particles' orientations or bond orientation 
		# lines up perfectly as the ideal structure and less than one other wise.

		D = np.sqrt(sum(qlmbar_mag_sq))

		if D!=0.0:
			qlmtilde_neighs[j] = [x/D for x in qlmbar]		# Normalize Y_lm_sum with D to get qlm tilde. Normalzed 2*l+1-dimensional complex vector
		else:
			print("Error: q_"+str(l)+" may be zero. Somehow your vector of spherical harmonics has a magnitude of zero. The particle is acting like it has no neighbors. This is strange. Email Jack. Line 87")
			sys.exit(1)
		#----------------------------------








	# Now to get qlm for all neighbors of particle
	# Form qlmbar, ql, and qlmtilde

	if len(self.neighs) != 0:

		qlmbar = []			#qlm bar--list with each element the sum of the spher harm over all neighbors divided by the number of neighbors *for a specific m value*
		qlmbar_mag_sq = []	#qlm bar magnitude squared--list with each element the magnitude squared of Ylm_sum. Used to make qlm bar into qlm tilde

		for m in range(-l,l+1):
			Ylm_sum = 0.0
			for angle in unit_sph:
				Ylm_sum += ss.sph_harm(m,l,angle[0],angle[1])/len(unit_sph)	
			Ylm_sum_mag_sq = Ylm_sum*np.conj(Ylm_sum)
			qlmbar.append(Ylm_sum)
			qlmbar_mag_sq.append(Ylm_sum_mag_sq)



		# Normalize qlmbar to ideal particle or lattice or fall back to usual way from Frenkel
		# With this normalization, pl will be 1 if the particles' orientations or bond orientation 
		# lines up perfectly as the ideal structure and less than one other wise.

		D = np.sqrt(sum(qlmbar_mag_sq))

		ql_i = np.abs(np.sqrt((4*np.pi/(2*l+1))*sum(qlmbar_mag_sq)))		# Local invariant ql for each particle

		if D!=0.0:
			qlmtilde = [x/D for x in qlmbar]		# Normalize Y_lm_sum with D to get qlm tilde. Normalzed 2*l+1-dimensional complex vector
		else:
			print("Error: q_"+str(l)+" may be zero. Somehow your vector of spherical harmonics has a magnitude of zero. The particle is acting like it has no neighbors. This is strange. Email Jack.")
			sys.exit(1)



	
		ql = [ql_i, qlmbar, qlmtilde, qlmtilde_neighs, phi_theta]

	
	else:
		ql = [None, [], [], [], phi_theta]



	return ql







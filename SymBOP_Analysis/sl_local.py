import numpy as np
import scipy.special as ss
from vecPBC import vecPBC










def sl_local(self, l):


	# Define the box dimensions
	if self.pbc==True:
		Lx = self.boxBounds[0][1] - self.boxBounds[0][0]
		Ly = self.boxBounds[1][1] - self.boxBounds[1][0]
		if self.dim==3:
			Lz = self.boxBounds[2][1] - self.boxBounds[2][0]
		else:
			Lz = None


	unit_sph = []
	for j in self.vertices:

		if self.pbc==True:
			d = np.array(vecPBC([self.x, self.y, self.z], [self.xyz[j][0], self.xyz[j][1], self.xyz[j][2]], Lx, Ly, Lz), dtype=np.float)
		else:
			d = np.array([self.x, self.y, self.z], dtype=np.float) - np.array([self.xyz[j][0], self.xyz[j][1], self.xyz[j][2]], dtype=np.float)	

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



	# Form slmbar, sl, and slmtilde

	if len(self.vertices) != 0:

		slmbar = []			#slm bar--list with each element the sum of the spher harm over all neighbors divided by the number of neighbors *for a specific m value*
		slmbar_mag_sq = []	#slm bar magnitude squared--list with each element the magnitude squared of Ylm_sum. Used to make slm bar into slm tilde

		for m in range(-l,l+1):
			Ylm_sum = 0.0
			for angle in unit_sph:
				Ylm_sum += ss.sph_harm(m,l,angle[0],angle[1])/len(unit_sph)	
			Ylm_sum_mag_sq = Ylm_sum*np.conj(Ylm_sum)
			slmbar.append(Ylm_sum)
			slmbar_mag_sq.append(Ylm_sum_mag_sq)


		# Normalize slmbar to ideal particle or lattice or fall back to usual way from Frenkel
		# With this normalization, pl will be 1 if the particles' orientations or bond orientation 
		# lines up perfectly as the ideal structure and less than one other wise.
		if l in self.slmbar_ideal:
			slmtilde = list(np.array(slmbar, dtype=complex)/self.slmbar_ideal[l])
			sl_i = round(np.abs(np.sqrt(np.vdot(np.array(slmtilde, dtype=complex), np.array(slmtilde, dtype=complex)))),6)

			D = np.sqrt(sum(slmbar_mag_sq))

			if D!=0.0:
				slmtilde_not_ideal = [x/D for x in slmbar]		# Normalize Y_lm_sum with D to get qlm tilde. Normalzed 2*l+1-dimensional complex vector

		else:
			D = np.sqrt(sum(slmbar_mag_sq))

			sl_i = np.abs(np.sqrt((4*np.pi/(2*l+1))*sum(slmbar_mag_sq)))		# Local invariant sl for each particle

			if D!=0.0:
				slmtilde = [x/D for x in slmbar]		# Normalize Y_lm_sum with D to get slmtilde. Normalzed 2*l+1-dimensional complex vector
			else:
				print("Error: s_"+str(l)+" may be zero. Somehow your vector of spherical harmonics has a magnitude of zero. The particle is acting like it has no neighbors. This is strange. Email Jack.")
				sys.exit(1)

			slmtilde_not_ideal = slmtilde



		
		sl = [sl_i, slmbar, slmtilde, slmtilde_not_ideal]

	
	else:
		sl = [None, [], [], []]



	return sl 







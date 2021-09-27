import numpy as np
import scipy.special as ss
from vecPBC import vecPBC
from Particle import Particle





def ql_local_PP(l, ipos, neighspos):


	unit_sph = []
	for j in neighspos:
		d = np.array([ipos[0], ipos[1], ipos[2]], dtype=np.float) - np.array([j[0], j[1], j[2]], dtype=np.float)	
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



	# Form qlmbar, ql, and qlmtilde

	if len(neighspos) != 0:

		qlmbar = []			#qlm bar--list with each element the sum of the spher harm over all neighbors divided by the number of neighbors *for a specific m value*
		qlmbar_mag_sq = []	#qlm bar magnitude squared--list with each element the magnitude squared of Ylm_sum. Used to make qlm bar into qlm tilde

		for m in range(-l,l+1):
			Ylm_sum = 0.0
			for angle in unit_sph:
				Ylm_sum += ss.sph_harm(m,l,angle[0],angle[1])/len(unit_sph)	
			Ylm_sum_mag_sq = Ylm_sum*np.conj(Ylm_sum)
			qlmbar.append(Ylm_sum)
			qlmbar_mag_sq.append(Ylm_sum_mag_sq)

		

					
		D = np.sqrt(sum(qlmbar_mag_sq))

		ql_i = np.abs(np.sqrt(sum(qlmbar_mag_sq)))		# Local invariant ql for each particle



		if D!=0.0:
			qlmtilde = [x/D for x in qlmbar]		# Normalize Y_lm_sum with D to get qlm tilde. Normalzed 2*l+1-dimensional complex vector
		else:
			print("Error: q_"+str(l)+" may be zero. Somehow your vector of spherical harmonics has a magnitude of zero. The particle is acting like it has no neighbors. This is strange. Email Jack.")
			sys.exit(1)


		
		ql = [ql_i, qlmbar, qlmtilde]



	return ql 





import numpy as np
import scipy.special as ss
import pathlib
from Particle import Particle











def ql_global(l, particles):

	# Keep only particles that have neighbors (this was changed 5/23/2020)
	particles = [i for i in particles if len(Particle.data[i].neighs)>0]

	neigh_total = sum([len(Particle.data[i].neighs) for i in particles])


	

	if isinstance(l, int):

		if len(particles)!=0:
	
			# average slmbar weighted by the number of neighbors
			Qlmbar = list(sum([np.array(Particle.data[p].qlmbar[l], dtype=complex)*len(Particle.data[p].neighs)/neigh_total for p in particles]))
			Qlmtilde = list(sum([np.array(Particle.data[p].qlmtilde[l], dtype=complex)*len(Particle.data[p].neighs)/neigh_total for p in particles]))
	
			
			if l in Particle.qlmbar_ideal:						
				Ql = np.abs(np.sqrt((4*np.pi/(2*l+1))*np.vdot(np.array(Qlmtilde, dtype=complex), np.array(Qlmtilde, dtype=complex))))

			
			else:
				Qlmbar_mag_sq = np.abs(np.vdot(np.array(Qlmbar, dtype=complex), np.array(Qlmbar, dtype=complex)))

				Ql = np.abs(np.sqrt((4*np.pi/(2*l+1))*Qlmbar_mag_sq))

				D = np.sqrt(Qlmbar_mag_sq)

		else:
			Qlmbar = [0]*(2*l+1)
			Qlmtilde = [0]*(2*l+1)
			Ql = 0.0



		return [Ql, Qlmbar, Qlmtilde]







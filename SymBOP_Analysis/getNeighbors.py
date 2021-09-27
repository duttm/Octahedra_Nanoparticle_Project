import numpy as np
from distPBC import distPBC
from Particle import Particle
import sys


def getNeighbors(rmin, rmax, excluded_part_pairs, excluded_bonds, excluded_parts):#self, data, orientational_only):

	print("\nGetting Neighbors...\n")



	if Particle.orientational_only==False and Particle.pbc==False:
		# Reset bonds
		Particle.bonds = {}


		# Distance between particles as numpy array
		pos = np.array([[Particle.data[i].x,Particle.data[i].y,Particle.data[i].z] for i in Particle.centers], dtype=float)

		distsq = -2 * np.dot(pos, pos.T) + np.sum(pos**2, axis=1) + np.sum(pos**2, axis=1)[:, np.newaxis]

		findneighs = [[i,[j for j in range(distsq.shape[1]) if i!=j and rmin < np.sqrt(distsq[i,j]) <= rmax]] for i in range(distsq.shape[0])]

		# To make sure those with no neighbors get an empty list
		for i in Particle.centers:
			Particle.data[i].neighs = []

		avgnumneighs = 0
		centers = list(Particle.centers.keys())
		for n in range(len(findneighs)):

			m = centers[n]

			nei = [centers[i] for i in findneighs[n][1]]

			for each in nei:

				Particle.data[m].neighs.append(each)

				Particle.bonds[len(Particle.bonds)] = [m, each]
				avgnumneighs += 1

		avgnumneighs /= len(centers)


		print("\n\n(getNeighbors()) # bonds: ", len(Particle.bonds))
		print("(getNeighbors()) avg # neighs: ", avgnumneighs)
		print("(getNeighbors()) # centers: ", len(centers))
		print("(getNeighbors()) # particles: ", len(Particle.centers))



	elif Particle.orientational_only==False and Particle.pbc==True:

		# To make sure those with no neighbors get an empty list
		for i in Particle.centers:
			Particle.data[i].neighs = []

		center_keys = list(Particle.centers.keys())
		total_neighs = 0
		for i in range(len(center_keys)):
			excluded_i_pairs = [pp[0] for pp in excluded_part_pairs if pp[1]==center_keys[i]] + [pp[1] for pp in excluded_part_pairs if pp[0]==center_keys[i]] 	

			for j in range(i+1, len(center_keys)):
				if center_keys[j] not in excluded_i_pairs:
					dist = distPBC(Particle.data[center_keys[i]].pos(), Particle.data[center_keys[j]].pos())
					if rmin < dist < rmax:
						Particle.data[center_keys[i]].neighs.append(center_keys[j])
						Particle.data[center_keys[j]].neighs.append(center_keys[i])
						total_neighs += 1
					
						#if center_keys[j] not in excluded_i_pairs:
						Particle.bonds[len(Particle.bonds)] = [center_keys[i], center_keys[j]]

				
		if total_neighs==0:
			print("\nNo Particles have any neighbors. Try a different rmin and rmax.\n")
			sys.exit(0)

	else:

		neighs = [i for i in Particle.centers]

		for i in Particle.centers:
			Particle.data[i].neighs = neighs


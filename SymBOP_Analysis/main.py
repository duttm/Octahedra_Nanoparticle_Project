from Particle import Particle
from readData import readData
from getNeighbors import getNeighbors
from normalization import normalization
from writeFiles import writeFiles
from plots import plots
from getprojqs import getprojqs
from bonds_to_parts_anisotropic import bonds_to_parts_anisotropic





def main(startline, delim, IN, FILE, OUT, dim, boundaries, pbc, center_type, isotropic, squares, l, orientational_only, use_ideal_normalization, rmin, rmax, find_domains, dom_min, show_plots, writefiles, particle_type, lattice_type, excluded_part_pairs=[], excluded_bonds=[], excluded_parts=[], bad_particle_types=[], ratio=None, ideal_ss=None, ideal_qs=None, qs_width=None, ss_width=None):





	#--------------------------------------------------------
	## Basics ##


	## Make class variables holding all particles positions and types, and which positions represent centers of particles
	## If isotropic==True, all positions represent centers of particles
	xyz, centers, NP = readData(IN=IN, FILE=FILE, dim=dim, center_type=center_type, startline=startline, delim=delim, isotropic=isotropic, boxBounds=boundaries, PBC=pbc, excluded_parts=excluded_parts, bad_particle_types=bad_particle_types)


	## Set important variables in Particle class ##
	Particle.setClassVariables(IN, OUT, dim, boundaries, l, pbc, center_type, isotropic, orientational_only, xyz, centers, find_domains, particle_type, lattice_type, show_plots, writefiles, NP)


	## Make all the centers into Particles ##
	## The constructor finds the vertices of this center particle if isotropic==False
	data = {i:Particle(i, [xyz[i][0], xyz[i][1], xyz[i][2]], xyz[i][3], isotropic) for i in centers}
	Particle.setData(data)


	## Make all squares into octahedra ##
	if squares==True:
		for part in Particle.centers:
			Particle.data[part].square_to_octahedron()




	## Get the neighbors of each particle ##
	getNeighbors(rmin, rmax, excluded_part_pairs, excluded_bonds, excluded_parts)


	# If normalizing the order parameters to an ideal object and/or lattice
	# Enter the name of the ideal particle, ideal lattice type, if available.
	if use_ideal_normalization==True:
		for lval in l:
			slmbar_ideal, qlmbar_ideal = normalization(lval, particle_type, lattice_type, orientational_only)				
			Particle.setNorms(lval, slmbar_ideal, qlmbar_ideal)






	## Particle Orientational Order ##

	if isotropic==False:
		# Get the sl order parameter of the body order
		for lval in l:

			# Get the slm value for the extended particle
			for i in Particle.centers:
				Particle.data[i].getLocalsl(lval)

			# Get the inner product between slmtilde and all neighboring particles' slmtilde
			for i in Particle.centers:
				Particle.data[i].get_slm_dot_slm(lval)







	## Bond-Orientational Order and SymBOPs ##

	if orientational_only==False:
		# Get the ql order parameter of the bond order
		for lval in l:

			# Get the qlm value for the particle
			for i in Particle.centers:
				Particle.data[i].getLocalql(lval)


			for i in Particle.centers:	
				Particle.data[i].get_neighs_qlm_dot_qlm(lval)




	#--------------------------------------------------------
	## Extra Output ##

	if writefiles==True:
		writeFiles(rmin, rmax)

		if show_plots==True or writefiles==True:
			plots()


	#--------------------------------------------------------
	
	## Finding Domains ##
	if find_domains==True:
		dom = []
		bond_phi_theta_qs = {lval:[] for lval in l}
		for lval in l:

			dom_addition, bond_phi_theta_addition = getprojqs(lval, ideal_qs[lval], ideal_ss[lval], qs_width, ss_width, orientational_only)

			dom += dom_addition


		# remove repeated bonds after combining the possible domains for differe l-values	
		dom = list(set(dom))	
		

		if len(l)>1:
			lval = 4
		else:
			lval = l[0]

		doms_parts = []
		doms_parts.append(bonds_to_parts_anisotropic(dom, Particle.xyz, dom_min, lval, qs_width, ss_width))






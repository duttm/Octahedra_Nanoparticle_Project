import numpy as np
from square_to_octahedron import square_to_octahedron
from sl_local import sl_local
from ql_local import ql_local
import os
import sys
from pathlib import Path





# Clarification of Notation
# qlm		bond orientational for one PARTICLE
# slm		particle orientational for one PARTICLE

# We can get inner products between any two vectors with the same spherical harmonic degree l
# For two anisotropic particles:
#	slm dot slm
#	qlm dot qlm

# Class Variables
# Particle.xyz			# (dict) Holds the position and particle type of all vertices and centers of particles
# Particle.centers		# (list) Holds all the numbers of the centers of the particles
# Particle.data			# (dict) Holds the Particle instance of each center particle





class Particle():

	IN = None
	OUT = {}
	dim = 3
	boxBounds = None
	pbc = True
	center_type = None
	isotropic = False
	xyz = {}
	centers = []
	data = {}	
	bonds = {}
	NP = {}		# Nanoparticles

	slmbar_ideal = {}
	qlmbar_ideal = {}

	# Domain
	sldomains = {}


	def __init__(self, partnum, centerpos, particle_type=None, isotropic=True):


		self.part = partnum

		self.x = centerpos[0]
		self.y = centerpos[1]
		if len(centerpos)==3:
			self.z = centerpos[2]
			self.dim = 3
		else:
			self.dim = 2

		self.isotropic = isotropic

		self.particle_type = particle_type

		# Nearest Neighbor particles. If isotropic==False, particles are extended objects, not vertices.
		self.neighs = []

		self.vertices = []

		if isotropic == False:
			self.getVertices()


		### Order Parameters ###
		
		# These are set using getLocalql()
		self.ql = {}								# scalar local invariant. key=l-value (dict)
		self.qlmbar = {}							# vector order parameter. key=l-value (dict)
		self.qlmtilde = {}							# unit vector order parameter. key=l-value (dict)
		self.neighs_qlm = {}						# qlmtilde for each individual neighbor (bond) key=l-value, key2=neighbor (2D dict)


		# These are set using getLocalsl()
		self.sl = {}								# scalar local invariant. key=l-value (dict)
		self.slmbar = {}							# vector order parameter. key=l-value (dict)
		self.slmtilde = {}							# unit vector order parameter. key=l-value (dict)
		self.slmtilde_not_ideal = {}


		### Inner products of order parameters ###
													
		self.slmdotslm = {}							# 2D Dict. For each key l-value, a dict with keys of neighbor part numbers
                                                    # and values given by the inner product between this particle slmtilde
                                                    # and its neighbors' slmtilde vectors.

		self.qlmdotqlm = {}							# 2D Dict. For each key l-value, a dict with keys of neighbor part numbers
                                                    # and values given by the inner product between this particle qlmtilde
                                                    # and another particle's qlmtilde vectors.





	def setClassVariables(IN, OUT, dim, boundaries, l, pbc, center_type, isotropic, orientational_only, xyz, centers, find_domains, particle_type, lattice_type, show_plots, writefiles, NP):
		Particle.dim = dim
		Particle.boxBounds = boundaries
		Particle.l = l
		Particle.pbc = pbc
		Particle.center_type = center_type
		Particle.isotropic = isotropic
		Particle.orientational_only = orientational_only
		Particle.xyz = xyz
		Particle.centers = centers

		Particle.find_domains = find_domains
		Particle.particle_type = particle_type
		Particle.lattice_type = lattice_type
		Particle.show_plots = show_plots
		Particle.writefiles = writefiles
		Particle.NP = NP

		Particle.IN = IN
		if OUT != None:
			Particle.OUT = OUT		
		else:
			Particle.OUT = IN

		# Set up output directories for sl and ql
		for each in l:
			newpath = Path(str(Particle.OUT)+"s"+str(each)+"/")
			if newpath.exists()==False:
				newpath.mkdir(parents=True, exist_ok=False)
			else:
				print("Error: "+str(Particle.OUT)+"s"+str(each)+"/ already exists. \nCannot save data in this directory, because it could overwrite the current files. \nEither put a new output path into OUT or delete or change the name of the directory "+str(Particle.OUT)+"s"+str(each)+"     ;)")
				#cont = input("\nContinue anyway? (y or n)\n")
				cont = "n"#"n"
				if cont=="n":
					sys.exit(1)
				#else:
				#	Particle.OUT[each] = newpath 

			if orientational_only==False:
				newpath = Path(str(Particle.OUT)+"q"+str(each)+"/")
				if newpath.exists()==False:
					newpath.mkdir(parents=True, exist_ok=False)
				else:
					print("Error: "+str(Particle.OUT)+"q"+str(each)+"/ already exists. \nCannot save data in this directory, because it could overwrite the current files. \nEither put a new output path into OUT or delete or change the name of the directory "+str(Particle.OUT)+"q"+str(each)+"     ;)")
					#cont = input("\nContinue anyway? (y or n)\n")
					cont = "n"#"n"
					if cont=="n":
						sys.exit(1)
					#else:
					#	Particle.OUT[each] = newpath 



		





	# Class Methods


	############################################################################################
	### Read data, set normalizations for perfect structures, and get vertices, if necessary ###
	############################################################################################

	def setData(data):
		Particle.data = data

	def set_xyz(self):
		self.x = Particle.data[partnum][0]
		self.y = Particle.data[partnum][1]
		self.z = Particle.data[partnum][2]

	def setNorms(l, slmbar_ideal, qlmbar_ideal):
		Particle.slmbar_ideal[l] = slmbar_ideal
		Particle.qlmbar_ideal[l] = qlmbar_ideal

	def setParticleType(particle_type):
		self.particle_type = particle_type

	def pos(self):
		if Particle.dim==3:
			return [self.x, self.y, self.z]
		elif Particle.dim==2:
			return [self.x, self.y]


	# For anisotropic particles, this will populate self.vertices=[] for each particle.
	# The vertices are treated as particles (and may even be particles in some cases)
	# This function depends on how the input file is written.
	# For now it is made so the center particle is followed ("\n") immediately by its vertices, then the next center particle, etc. 
	def getVertices(self):
		for i in list(Particle.xyz.keys())[self.part+1:]:
			if Particle.xyz[i][Particle.dim] != Particle.center_type:
				self.vertices.append(i)
			else:
				break
		

	# To convert all square particles to icosahedra, one particle at a time
	def square_to_octahedron(self):
		square_to_octahedron(self)




	#########################################################################
	### Get the orientational order vectors slm and qlm for this particle ###
	#########################################################################

	# Get the bond orientational order parameter for the particle with the particles in its neighborhood [rmin, rmax], given in Sample.py.
	# This populates self.ql[l], self.qlmbar[l], self.qlmtilde[l]
	def getLocalql(self, l):
		self.ql[l], self.qlmbar[l], self.qlmtilde[l], self.neighs_qlm[l], self.neighs_phi_theta = ql_local(self, l)	

	# Get the orientational order parameter (ql, ql_i, qlmtilde) of the particle itself--treating the vertices as particles around the center "particle".
	# The vertices and center may or may not be actual particles
	# This populates self.sl[l], self.slmbar[l], self.slmtilde[l]
	# If the particles are all the same type of perfect polyhedron (ex. all perfect octahedra), sl will be the same for all, but slmbar and slmtilde will not
	def getLocalsl(self, l):
		self.sl[l], self.slmbar[l], self.slmtilde[l], self.slmtilde_not_ideal[l] = sl_local(self, l)	




	##########################################################################################
	### Inner product between particle slmtilde vectors (normalized to the ideal particle) ###
	##########################################################################################

	def get_slm_dot_slm(self, l):
		self.slmdotslm[l] = {j:np.vdot(np.array(self.slmtilde[l], dtype=complex), np.array(Particle.data[j].slmtilde[l], dtype=complex)) for j in self.neighs}




	#############################################################################################################
	### Inner product of usual bond orientational order parameter qlmtlde between particles (normalized to 1) ###
	#############################################################################################################

	# Get the inner product of the full (normalized to 1) bond orientational order vector qlmtilde of particle i with each of its neighbors qlmtilde 
	def get_neighs_qlm_dot_qlm(self, l):
		self.qlmdotqlm[l] = {j:np.vdot(np.array(self.qlmtilde[l], dtype=complex), np.array(Particle.data[j].qlmtilde[l], dtype=complex)) for j in self.neighs}







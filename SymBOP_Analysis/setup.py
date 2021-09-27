from main import main
from pathlib import Path
from Particle import Particle




def Setup(ratio, IN, OUT=None, l=[], particle_type=None, bond_type=None, dom_min=4,  boundaries=[], rmin=None, rmax=None, ideal_qs={}, ideal_ss={}, qs_width=0.2, ss_width=0.2):

	print("\n\n-----------------------------------")

	print("Ratio: ", ratio, "\n")

	print("\nSetting up...\n")


	# Set parameters
	# Changing these parameters may lead to 
	# undefined paths through the code, but you're free to try
	show_plots = False
	writefiles = True
	startline = 2
	delim = "\t"	
	find_domains = True
	dim = 3
	pbc = True
	center_type = 1
	isotropic = False

	FILE = "PP_data_"+str(ratio)+".txt"





	##########################################
	## Read Settings from file Settings.txt ##
	##########################################
	if Path.is_file(Path(IN+"Settings.txt")) == True:
		bound = []
		boundaries = []
		with open(IN+"Settings.txt", "r") as f:
			lines = f.readlines()
			for i in range(len(lines)):
				if lines[i].strip("\n")==str(ratio):
					line = lines[i+1].strip("\n").split("\t")
					rmin = float(line[0])
					rmax = float(line[1])
				elif lines[i].strip("\n")=="Box":
					for j in [1,2,3]:
						bound.clear()
						line = lines[i+j].strip("\n").split("\t")
						bound.append(float(line[0]))
						bound.append(float(line[1]))
						boundaries.append(bound)
				elif (lines[i].strip("\n")).lower()=="particle_type":
					line = lines[i+1].strip("\n").split("\t")
					particle_type = str(line[0]).lower()
				elif (lines[i].strip("\n")).lower()=="bond_type":
					line = lines[i+1].strip("\n")
					bond_type = str(line).lower()
				elif (lines[i].strip("\n")).lower()=="l":
					line = lines[i+1].strip("\n").split(",")
					l = [int(i) for i in line]
				elif (lines[i].strip("\n")).lower()=="dom_min":
					line = lines[i+1].strip("\n")
					dom_min = int(line)
				elif (lines[i].strip("\n")).lower()=="ideal_qs":
					line = lines[i+1].strip("\n").split(",")
					line_ = []
					for li in line:
						line_ = li.split(":")
						ideal_qs[int(line_[0])] = [float(line_[1])]
				elif (lines[i].strip("\n")).lower()=="ideal_ss":
					line = lines[i+1].strip("\n").split(",")
					line_ = []
					for li in line:
						line_ = li.split(":")
						ideal_ss[int(line_[0])] = [float(line_[1])]
				elif (lines[i].strip("\n")).lower()=="qs_width":
					line = lines[i+1].strip("\n")
					qs_width = float(line)
				elif (lines[i].strip("\n")).lower()=="ss_width":
					line = lines[i+1].strip("\n")
					ss_width = float(line)
				elif (lines[i].strip("\n")).upper()=="OUT":
					line = lines[i+1].strip("\n")
					OUT = str(line)
		if OUT == None:
			OUT = IN

	##########################################
	##########################################

	
	print("\n\n\nSettings Used:")
	print("boundaries: ", boundaries)
	print("rmin, rmax: ", rmin, rmax)
	print("particle_type: ", particle_type)
	print("bond_type: ", bond_type)
	print("dom_min: ", dom_min)
	print("l: ", l)
	print("ideal_qs: ", ideal_qs)
	print("ideal_ss: ", ideal_ss)
	print("qs_width: ", qs_width)
	print("ss_width: ", ss_width)
	print("OUT: ", OUT, "\n\n\n")




	## make output directory if it doesn't exist ##
	OUT += str(ratio)+"/"+bond_type.lower()+"/"
	Path(OUT).mkdir(parents=True, exist_ok=True)	


	if particle_type.lower() == "square" or particle_type.lower() == "squares":
		squares = True
	else:
		squares = False




	# for anisotropic particles with nanoparticles or other particles that you do NOT want included in the particle shape
	# List the particle types here to not include
	bad_particle_types = [3,4,5]


	# particle_type options: "octahedron", "square", "fcc"
	# lattice_typee options: "cubic", "fcc", "bcc"
	# The squares are modeled as octahedra
	# It's important that above squares=True if you're using squares
	# Then it knows to change all squares to octahedra.
	# And that's why the particle_type is set to "octahedron" here
	particle_type = "octahedron"
	lattice_type = "fcc"

	# True to disregard Bond-orientation order and only use orientational order of the particles
	OOP_only = False
	use_ideal_normalization = True  	# Normalize particles to ideal particle type, and neighbors to ideal lattice type




	##########################################################
	##########################################################



	## Anisotropic ##
	# Set some common bond-orientational order values
	# and define face-to-face (FtF) and edge-to-edge (EtE) regions of the 
	# local order parameter plots for l=4,6

	# BOOPs values for common crystals
	FCC = {4:0.191, 6:0.575}
	BCC = {4:0.509, 6:0.629}
	HCP = {4:0.097, 6:0.485}
	SC = {4:0.764, 6:0.354}

	# face-to-face octahedra
	if bond_type == "FtF" or bond_type=="ftf":
		face_to_face_octa = {4:-0.5, 6:0.6}
		ideal_ss = {4:[-0.46], 6:[0.4]}
		ideal_qs = {i:[face_to_face_octa[i]] for i in l}

	# edge-to-edge octahedra
	if bond_type == "EtE" or bond_type=="ete":
		ideal_ss = {4:[1.0], 6:[1.0]}
		ideal_qs = {i:[-FCC[i]] for i in l}



	main(startline=startline, delim=delim, IN=IN, FILE=FILE, OUT=OUT, dim=dim, boundaries=boundaries, pbc=pbc, center_type=center_type, isotropic=isotropic, squares=squares, l=l, orientational_only=OOP_only, use_ideal_normalization=use_ideal_normalization, rmin=rmin, rmax=rmax, find_domains=find_domains, dom_min=dom_min, show_plots=show_plots, writefiles=writefiles, particle_type=particle_type, lattice_type=lattice_type, bad_particle_types=bad_particle_types, ratio=ratio, ideal_ss=ideal_ss, ideal_qs=ideal_qs, qs_width=qs_width, ss_width=ss_width)






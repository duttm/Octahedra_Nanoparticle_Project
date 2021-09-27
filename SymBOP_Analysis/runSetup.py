from setup import Setup
from getRatios import getRatios
from Particle import Particle
import os


#NOTE
## If Settings.txt has been made and is located in the 
## directory IN defined here, then it will be used.
## This is useful for running multiple ratios at once.
## To run a single ratio without a Settings.txt file
## remove any Settings.txt file from the IN directory
## (or rename it) and manually put the parameters in below.




## Path to input files ##
## This is defined whether you use "Settings.txt" or not
IN = "/Users/Desktop/"




#-------------------------------------------------------
#NOTE
## Only need to fill out parameters below this line if 
## you do not want to use a "Settings.txt" file to define
## the parameters


## Settings ##


# Patchy-particle size to Nanoparticle size ratio
ratio = 1.39

# Path to where to save output files
OUT = IN
# l-values to use for spherical harmonics (set as list)
l = [4,6]
# PBC box boundaries
boundaries = [[-0.65, 9.75], [-0.65, 9.75], [-0.65, 9.75]]
# Min and Max radius to look for neighbors
rmin = 0.65
rmax = 0.776

# Type of anisotropic particle
# Choose between "octahedron" and "square"
particle_type = "square"

# Type of bond to look for in data
# Can choose from "EtE", "FtF", or 
# set bond_type to None and define 
# your own using ideal_ss and ideal_qs.
# See README for more info. 
bond_type = "FtF"
ideal_ss = {}
ideal_qs = {}
#ideal_ss = {4:[-0.46], 6:[0.4]}
#ideal_qs = {4:[-0.5], 6:[0.6]}
qs_width = 0.1
ss_width = 0.1

# Minimum domain size to keep (default is 4)
dom_min = 4




















#--------------------------------------------------------------------
# No need to change anything below this line.
#--------------------------------------------------------------------

if os.path.isfile(IN+"Settings.txt") == True:
	ratios = getRatios(IN)

	for ratio in ratios:
		Setup(ratio, IN)

		if len(Particle.data) > 0:
			#print("\n\n\n----------------------Deleted variables----------------------\n\n\n")
			Particle.xyz.clear()
			Particle.centers.clear()
			Particle.NP.clear()
			Particle.data.clear()		
			Particle.bonds.clear()


else:

	Setup(ratio, IN, OUT, l, particle_type, bond_type, dom_min, boundaries, rmin, rmax, ideal_qs, ideal_ss, qs_width, ss_width)


	if len(Particle.data) > 0:
		#print("\n\n\n----------------------Deleted variables----------------------\n\n\n")
		Particle.xyz.clear()
		Particle.centers.clear()
		Particle.NP.clear()
		Particle.data.clear()		
		Particle.bonds.clear()


print("\n\n\n\n--------------Thanks! Have a great day!--------------\n\n\n\n")




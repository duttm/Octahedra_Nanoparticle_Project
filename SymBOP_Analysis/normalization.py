import numpy as np
from ql_local_PP import ql_local_PP
import sys



# This code is used to set the normalization for the particle and bond orientational orders.
# For example, if we normalize the particles to a perect octahedron, then each octahedron will
# have a scalar order parameter equal to one.
# The lattice can be normalized to cubic, for instance, than any bond orientational order is
# found relative to a cubic lattice, and a value of 1 would mean the neighbors form 
# a perfect cubic lattice around the particle.

def normalization(l, ideal_particle, ideal_lattice, orientational_only):

	if ideal_particle == "octahedron":

		center = [0,0,0]
		neighspos = [[1,0,0],[0,1,0],[0,0,1],[-1,0,0],[0,-1,0],[0,0,-1]]

		q_octahedron = ql_local_PP(l, center, neighspos)

		slmbar_real = [np.real(i) if np.abs(np.real(i))>1e-10 else 0 for i in q_octahedron[1]]
		slmbar_imag = [np.imag(i) if np.abs(np.imag(i))>1e-10 else 0 for i in q_octahedron[1]]
		slmbar = tuple(zip(slmbar_real, slmbar_imag))

		slmbar_ideal_particle = q_octahedron[0]

		slmtilde = q_octahedron[-1]
		#print("slmtilde: ", slmtilde)
		#print("slmtilde mag: ", np.sqrt(np.vdot(np.array(slmtilde, dtype=complex), np.array(slmtilde, dtype=complex))))	
				



	elif ideal_particle == "square":

		center = [0,0,0]
		neighspos = [[1,1,0],[-1,1,0],[-1,-1,0],[1,-1,0]]
		q_square = ql_local_PP(l, center, neighspos)

		slmbar_real = [np.real(i) if np.abs(np.real(i))>1e-10 else 0 for i in q_square[1]]
		slmbar_imag = [np.imag(i) if np.abs(np.imag(i))>1e-10 else 0 for i in q_square[1]]
		slmbar = tuple(zip(slmbar_real, slmbar_imag))

		slmbar_ideal_particle = q_square[0]

		slmtilde = q_square[-1]
		#print("slmbar_ideal: ", slmbar)
		#print("slmtilde: ", slmtilde)
		#print("slmtilde mag: ", np.sqrt(np.vdot(np.array(slmtilde, dtype=complex), np.array(slmtilde, dtype=complex))))	
	
		#print("\nSQUARE\n")
		#print("\n\nslmbar_ideal_particle: ", slmbar_ideal_particle, "\n\n")


	elif ideal_particle == "fcc" or ideal_particle == "FCC":

		center = [0,0,0]
		neighspos = [[np.sin(np.pi/4)*np.cos(0), np.sin(np.pi/4)*np.sin(0), np.cos(np.pi/4)],
					[np.sin(np.pi/4)*np.cos(np.pi/2), np.sin(np.pi/4)*np.sin(np.pi/2), np.cos(np.pi/4)],
					[np.sin(np.pi/4)*np.cos(np.pi), np.sin(np.pi/4)*np.sin(np.pi), np.cos(np.pi/4)], 
					[np.sin(np.pi/4)*np.cos(3*np.pi/2), np.sin(np.pi/4)*np.sin(3*np.pi/2), np.cos(np.pi/4)],

					[np.sin(np.pi/2)*np.cos(np.pi/4), np.sin(np.pi/2)*np.sin(np.pi/4), np.cos(np.pi/2)], 
					[np.sin(np.pi/2)*np.cos(3*np.pi/4), np.sin(np.pi/2)*np.sin(3*np.pi/4), np.cos(np.pi/2)], 
					[np.sin(np.pi/2)*np.cos(5*np.pi/4), np.sin(np.pi/2)*np.sin(5*np.pi/4), np.cos(np.pi/2)], 
					[np.sin(np.pi/2)*np.cos(7*np.pi/4), np.sin(np.pi/2)*np.sin(7*np.pi/4), np.cos(np.pi/2)],

					[np.sin(np.pi/4)*np.cos(0), np.sin(np.pi/4)*np.sin(0), -np.cos(np.pi/4)],
					[np.sin(np.pi/4)*np.cos(np.pi/2), np.sin(np.pi/4)*np.sin(np.pi/2), -np.cos(np.pi/4)],
					[np.sin(np.pi/4)*np.cos(np.pi), np.sin(np.pi/4)*np.sin(np.pi), -np.cos(np.pi/4)], 
					[np.sin(np.pi/4)*np.cos(3*np.pi/2), np.sin(np.pi/4)*np.sin(3*np.pi/2), -np.cos(np.pi/4)]]



		q_fcc = ql_local_PP(l, center, neighspos)

		slmbar_real = [np.real(i) if np.abs(np.real(i))>1e-10 else 0 for i in q_fcc[1]]
		slmbar_imag = [np.imag(i) if np.abs(np.imag(i))>1e-10 else 0 for i in q_fcc[1]]
		slmbar = tuple(zip(slmbar_real, slmbar_imag))

		slmbar_ideal_particle = q_fcc[0]



	#-----------------------------------------------------------------------------------------------------------------


	if orientational_only==False:

		if ideal_lattice == "cubic":
			center = [0,0,0]
			neighspos = [[i,j,k] for i in [-1,1] for j in [-1,1] for k in [-1,1]]
			q_cube = ql_local_PP(l, center, neighspos)
			
			qlmbar_real = [np.real(i) if np.abs(np.real(i))>1e-10 else 0 for i in q_cube[1]]
			qlmbar_imag = [np.imag(i) if np.abs(np.imag(i))>1e-10 else 0 for i in q_cube[1]]
			qlmbar = tuple(zip(qlmbar_real, qlmbar_imag))

			qlmbar_ideal_lattice = q_cube[0]




		elif ideal_lattice == "fcc":
			center = [0,0,0]
			neighspos = [[1,0,1],[1,0,-1],[-1,0,1],[-1,0,-1],[1,-1,0],[-1,-1,0],[0,-1,-1],[0,-1,1],[1,1,0],[-1,1,0],[0,1,-1],[0,1,1]]
			q_fcc = ql_local_PP(l, center, neighspos)

			qlmbar_real = [np.real(i) if np.abs(np.real(i))>1e-10 else 0 for i in q_fcc[1]]
			qlmbar_imag = [np.imag(i) if np.abs(np.imag(i))>1e-10 else 0 for i in q_fcc[1]]
			qlmbar = tuple(zip(qlmbar_real, qlmbar_imag))

			qlmbar_ideal_lattice = q_fcc[0]
			qlmtilde = q_fcc[-1]



		elif ideal_lattice == "bcc":
			center = [0,0,0]
			neighspos = [[1,1,1],[1,1,-1],[-1,1,1],[-1,1,-1],[1,-1,1],[1,-1,-1],[-1,-1,1],[-1,-1,-1]]
			q_bcc = ql_local_PP(l, center, neighspos)
			
			qlmbar_real = [np.real(i) if np.abs(np.real(i))>1e-10 else 0 for i in q_bcc[1]]
			qlmbar_imag = [np.imag(i) if np.abs(np.imag(i))>1e-10 else 0 for i in q_bcc[1]]
			qlmbar = tuple(zip(qlmbar_real, qlmbar_imag))

			qlmbar_ideal_lattice = q_bcc[0]

			qlmtilde = q_bcc[-1]



	if orientational_only==False and qlmbar_ideal_lattice < 1e-3:
		print("The ideal lattice for l="+str(l)+", qlmbar_ideal_lattice, is very small (= "+str(qlmbar_ideal_lattice)+") and could lead to problems when it divides plmtilde.")
		print("Maybe try a different value for l.")
		sys.exit(1)
	if slmbar_ideal_particle < 1e-3:
		print("The ideal particle for l="+str(l)+", slmbar_ideal_particle, is very small (= "+str(slmbar_ideal_particle)+") and could lead to problems when it divides slmtilde.")
		print("Maybe try a different value for l.")
		sys.exit(1)


	if orientational_only==False:
		return [slmbar_ideal_particle, qlmbar_ideal_lattice]
	else:
		return [slmbar_ideal_particle, None]







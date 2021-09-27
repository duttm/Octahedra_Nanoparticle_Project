import numpy as np
import matplotlib.pyplot as plt
from Particle import Particle
from math import fmod
import pathlib

params = {'text.usetex' : True}#, 'font.size' : 28, 'font.family' : 'lmodern'}
plt.rcParams.update(params)


#	Here we record the value of <s^i_lm|q^ij_lm> for each bond between particles i and j
#	This combined with <s^i_lm|s^j_lm> are used to create the local order parameter scatter 
#	plot that we use to percolate around the best values (depending on the lattice expected)
#	ideal_ss assumes the shape is normalized to an ideal polyhedron



def getprojqs(lval, ideal_qs, ideal_ss, projqs_width, projss_width, OOP_only = False):



	print("\nFinding Domains for l="+str(lval)+"...\n")



	

	# This is for the standard bond orientational order parameter vector

	with open(Particle.OUT+"q"+str(lval)+"/proj_q_on_s_for_each_bond.txt", "w") as f:
		f.write("bond number, <s^i_lm | q^ij_lm>, <s^i_lm | s^j_lm>\n\n")

	with open(Particle.OUT+"q"+str(lval)+"/proj_q_on_s_for_each_bond_in_possible_domain.txt", "w") as f:
		f.write("bond number, <s^i_lm | q^ij_lm>, <s^i_lm | s^j_lm>\n\n")

	with open(Particle.OUT+"q"+str(lval)+"/pairs_of_particle_positions_for_each_bond_in_possible_domain.txt", "w") as f:	
		f.write("particle type, x,y,z, position, bond number. listed as pairs of bonded particles\n")



	used_bonds = []

	proj_qs = []
	possible_dom = []
	possible_dom_qs_ss = []
	bonds_phi_theta_qs = []

	for i in Particle.centers:

		for j in Particle.data[i].neighs:
			# get the projection of the neighs_qlm onto slmtilde from i to j 
			proj_q_on_s = np.vdot(np.array(Particle.data[i].slmtilde[lval], dtype=complex), np.array(Particle.data[i].neighs_qlm[lval][j], dtype=complex))

			bond_num = [b for b in Particle.bonds if (Particle.bonds[b][0]==i and Particle.bonds[b][1]==j) or (Particle.bonds[b][0]==j and Particle.bonds[b][1]==i)]
			if bond_num[0] not in used_bonds:
				used_bonds += bond_num
				proj_qs.append([bond_num[0], proj_q_on_s, Particle.data[i].slmdotslm[lval][j]])
				
				

				if OOP_only==False:
					# Check the truth value of each ideal_q value expected
					in_qs_range = False
					in_ss_range = False

					for each in ideal_qs:
						if each - projqs_width < np.real(proj_qs[-1][1]) < each + projqs_width:
							in_qs_range = True

					for each in ideal_ss:
						if each - projss_width < np.real(proj_qs[-1][2]) < each + projss_width:
							in_ss_range = True

					if in_qs_range and in_ss_range:
						possible_dom.append(proj_qs[-1][0])
						possible_dom_qs_ss.append([np.real(proj_qs[-1][1]), np.real(proj_qs[-1][2]), proj_qs[-1][0]])
						

				else:
					in_ss_range = False
					for each in ideal_ss:
						if each - projss_width < np.real(proj_qs[-1][2]) < each + projss_width:
							in_ss_range = True

					if in_ss_range==True:					
						possible_dom.append(proj_qs[-1][0])
						possible_dom_qs_ss.append([np.real(proj_qs[-1][1]), np.real(proj_qs[-1][2]), proj_qs[-1][0]])






	# writes values for all bonds regardless of region of interest
	with open(Particle.OUT+"q"+str(lval)+"/proj_q_on_s_for_each_bond.txt", "a") as f:
		for i in proj_qs:
			f.write(str(i[0])+"\t"+str(i[1])+"\t"+str(i[2])+"\n")

	# writes values only for the region of interest	
	with open(Particle.OUT+"q"+str(lval)+"/proj_q_on_s_for_each_bond_in_possible_domain.txt", "a") as f:
		for i in possible_dom_qs_ss:
			f.write(str(i[2])+"\t"+str(i[0])+"\t"+str(i[1])+"\n")

	# writes positions of octahedra and vertices for bonded pairs
	with open(Particle.OUT+"q"+str(lval)+"/pairs_of_particle_positions_for_each_bond_in_possible_domain.txt", "a") as f:	
		f.write(str(len(possible_dom_qs_ss))+"\n")
		for i in [i[2] for i in possible_dom_qs_ss]:
			f.write("1\t"+str(Particle.data[Particle.bonds[i][0]].x)+"\t"+str(Particle.data[Particle.bonds[i][0]].y)+"\t"+str(Particle.data[Particle.bonds[i][0]].z)+"\t"+str(i)+"\n")
			for j in Particle.data[Particle.bonds[i][0]].vertices:
				if Particle.xyz[j][3]==2:
					f.write("2\t"+str(Particle.xyz[j][0])+"\t"+str(Particle.xyz[j][1])+"\t"+str(Particle.xyz[j][2])+"\n")

			f.write("1\t"+str(Particle.data[Particle.bonds[i][1]].x)+"\t"+str(Particle.data[Particle.bonds[i][1]].y)+"\t"+str(Particle.data[Particle.bonds[i][1]].z)+"\t"+str(i)+"\n")
			for j in Particle.data[Particle.bonds[i][1]].vertices:
				if Particle.xyz[j][3]==2:
					f.write("2\t"+str(Particle.xyz[j][0])+"\t"+str(Particle.xyz[j][1])+"\t"+str(Particle.xyz[j][2])+"\n")




	#print("\n\nMax number of bonds in domain: ", len(possible_dom))	
	

	# PLOT

	fig, ax = plt.subplots()


	# Get the x and y values to plot scatter
	xyvals = []
	for k in Particle.centers:
		for n in Particle.data[k].neighs:
			# get the projection of the neighs_qlm onto slmtilde from i to j 
			proj_q_on_s = np.vdot(np.array(Particle.data[k].slmtilde[lval], dtype=complex), np.array(Particle.data[k].neighs_qlm[lval][n], dtype=complex))

			xyvals.append([Particle.data[k].slmdotslm[lval][n], proj_q_on_s])


	slmvals = [np.real(i[0]) for i in xyvals]
	qlmvals = [np.real(i[1]) for i in xyvals]

	ax.scatter(slmvals, qlmvals, c='r', s=0.2)

	plt.rc('text', usetex=True)
	plt.rc('font', family='serif')


	ax.set_xlabel(r"$(s_{\alpha}^{"+str(lval)+r"m} | s_{\beta}^{"+str(lval)+r"m})$", fontsize=14)
	ax.set_ylabel(r"$(s_{\alpha}^{"+str(lval)+r"m} | q_{\alpha \beta}^{"+str(lval)+r"m})$", fontsize=14)



	minqs = min([i[1] for i in proj_qs])
	maxqs = max([i[1] for i in proj_qs])

	if OOP_only==True:
		q_range = [minqs, maxqs]	
		for each in range(len(ideal_ss)):
			s_range = [ideal_ss[each]-projss_width, ideal_ss[each]+projss_width]

			x = [s_range[0], s_range[0], s_range[1], s_range[1], s_range[0]]
			y = [q_range[0], q_range[1], q_range[1], q_range[0], q_range[0]]

			ax.plot(x, y, "b", lw=1)

	else:
		for each in range(len(ideal_qs)):
			q_range = [ideal_qs[each]-projqs_width, ideal_qs[each]+projqs_width]		

			for eachs in range(len(ideal_ss)):
				s_range = [ideal_ss[eachs]-projss_width, ideal_ss[eachs]+projss_width]

			x = [s_range[0], s_range[0], s_range[1], s_range[1], s_range[0]]
			y = [q_range[0], q_range[1], q_range[1], q_range[0], q_range[0]]

			ax.plot(x, y, "b", lw=1)


	plt.grid(axis="x")
	plt.grid(axis="y")

	plt.tight_layout()



	if Particle.writefiles==True:
		plt.savefig(pathlib.Path(str(Particle.OUT)+"/s"+str(lval)+"/<s"+str(lval)+"_i|q"+str(lval)+"_ij>_VS_<s"+str(lval)+"lm_i|s"+str(lval)+"lm_j>_scatter_for_domains.png"),dpi=300, transparent=True)		

	if Particle.show_plots==True:
		plt.show()	
	plt.close()





	return [possible_dom, bonds_phi_theta_qs]





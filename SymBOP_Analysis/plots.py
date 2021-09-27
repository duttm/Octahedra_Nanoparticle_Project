import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc #, colors, colorbar, cm, tri
import pathlib
from Particle import Particle

params = {'text.usetex' : True}#, 'font.size' : 28, 'font.family' : 'lmodern'}
plt.rcParams.update(params)







def plots():

	print("\nMaking Plots...\n")



	# aspect ratio of plots
	aspect = 9/16
	# bin density for histograms
	bin_density = 50



	for l in Particle.l:




		# sl histogram

		if Particle.isotropic==False:

			# Not plotting ql of particles with fewer than 2 neighbors. 
			# 0 neighbors will always give ql=0.0, and 1 neighbor gives ql=1.0

			maxsl = max([Particle.data[k].sl[l] for k in Particle.centers if Particle.data[k].sl[l]!=None and len(Particle.data[k].neighs) > 1])
			minsl = min([Particle.data[k].sl[l] for k in Particle.centers if Particle.data[k].sl[l]!=None and len(Particle.data[k].neighs) > 1])

			step = 0.02

			binbounds = np.arange(minsl-step, maxsl+step, step)

			vals = [Particle.data[k].sl[l] for k in Particle.centers if Particle.data[k].sl[l]!=None and len(Particle.data[k].neighs) > 1]



			fig2, ax2 = plt.subplots()

			bins = int(bin_density*(max(vals) - min(vals)))
			if bins < 2:
				bins = 10

			n, bins, patches = ax2.hist(vals, bins=bins, align='mid')
			plt.close()

			area = sum([(bins[i]-bins[i-1])*n[i-1] for i in range(1,len(bins))])
			n = [i/area for i in n]


			fig, ax = plt.subplots()

			# Plot the resulting histogram
			center = (bins[:-1]+bins[1:])/2
			width = 0.95*(bins[1]-bins[0])
			ax.bar(center, n, width)#, align="center")

			if minsl > 0.0:
				if maxsl < 1.0:
					ax.set_xlim(left=-step,right=1.0+step)
				else:
					ax.set_xlim(left=-step,right=maxsl+step)
			else:
				ax.set_xlim(left=minsl-step,right=maxsl+step)



			plt.rc('text', usetex=True)
			plt.rc('font', family='serif')
			ax.set_xlabel(r"$s_"+str(l)+"$", fontsize=14)
			ax.set_ylabel(r"Probability", fontsize=14)
			plt.grid(axis="x")

			if Particle.writefiles==True:
				plt.savefig(pathlib.Path(str(Particle.OUT)+"/s"+str(l)+"/s"+str(l)+"_histogram.png"),dpi=300, transparent=True)		
			if Particle.show_plots==True:
				plt.show()	
			plt.close()









		# ql histogram
		if Particle.orientational_only==False:

			# Not plotting ql of particles with fewer than 2 neighbors. 
			# 0 neighbors will always give ql=0.0, and 1 neighbor gives ql=1.0
			
			maxql = max([Particle.data[k].ql[l] for k in Particle.centers if Particle.data[k].ql[l]!=None and len(Particle.data[k].neighs) > 1])
			minql = min([Particle.data[k].ql[l] for k in Particle.centers if Particle.data[k].ql[l]!=None and len(Particle.data[k].neighs) > 1])

			step = 0.02

			binbounds = np.arange(minql-step, maxql+step, step)

			vals = [Particle.data[k].ql[l] for k in Particle.centers if Particle.data[k].ql[l]!=None and len(Particle.data[k].neighs) > 1]




			fig2, ax2 = plt.subplots()

			bins = int(bin_density*(max(vals) - min(vals)))
			if bins < 2:
				bins = 10

			n, bins, patches = ax2.hist(vals, bins=bins, align='mid')
			plt.close()

			area = sum([(bins[i]-bins[i-1])*n[i-1] for i in range(1,len(bins))])
			n = [i/area for i in n]


			fig, ax = plt.subplots()

			# Plot the resulting histogram
			center = (bins[:-1]+bins[1:])/2
			width = 0.95*(bins[1]-bins[0])
			ax.bar(center, n, width)#, align="center")


			if minql > 0.0:
				if maxql < 1.0:
					ax.set_xlim(left=-step,right=1.0+step)
				else:
					ax.set_xlim(left=-step,right=maxql+step)
			else:
				ax.set_xlim(left=minql-step,right=maxql+step)


			plt.rc('text', usetex=True)
			plt.rc('font', family='serif')
			ax.set_xlabel(r"$q_"+str(l)+"$", fontsize=14)
			ax.set_ylabel(r"Probability", fontsize=14)
			plt.grid(axis="x")

			if Particle.writefiles==True:
				plt.savefig(pathlib.Path(str(Particle.OUT)+"/q"+str(l)+"/q"+str(l)+"_histogram.png"),dpi=300, transparent=True)		
			if Particle.show_plots==True:
				plt.show()	
			plt.close()






		# qlmtilde dot qlmtilde histogram

		if Particle.orientational_only==False:


			maxqlmdotqlm = max([np.real(Particle.data[k].qlmdotqlm[l][n]) for k in Particle.centers for n in Particle.data[k].qlmdotqlm[l] if Particle.data[k].qlmdotqlm[l][n]!=None and len(Particle.data[k].neighs) > 1])
			minqlmdotqlm = min([np.real(Particle.data[k].qlmdotqlm[l][n]) for k in Particle.centers for n in Particle.data[k].qlmdotqlm[l] if Particle.data[k].qlmdotqlm[l][n]!=None and len(Particle.data[k].neighs) > 1])

			step = 0.02

			binbounds = np.arange(minqlmdotqlm-step, maxqlmdotqlm+step, step)

			vals = [np.real(Particle.data[k].qlmdotqlm[l][n]) for k in Particle.centers for n in Particle.data[k].qlmdotqlm[l] if Particle.data[k].qlmdotqlm[l][n]!=None and len(Particle.data[k].neighs) > 1]



			fig2, ax2 = plt.subplots()

			bins = int(bin_density*(max(vals) - min(vals)))
			if bins < 2:
				bins = 10

			n, bins, patches = ax2.hist(vals, bins=bins, align='mid')
			plt.close()

			area = sum([(bins[i]-bins[i-1])*n[i-1] for i in range(1,len(bins))])
			n = [i/area for i in n]


			fig, ax = plt.subplots()

			# Plot the resulting histogram
			center = (bins[:-1]+bins[1:])/2
			width = 0.95*(bins[1]-bins[0])
			ax.bar(center, n, width)#, align="center")


			plt.rc('text', usetex=True)
			plt.rc('font', family='serif')

			ax.set_xlim(1.05*minqlmdotqlm, 1.05*maxqlmdotqlm)

			ax.set_xlabel(r"$(q_{i}^{"+str(l)+r"m} | q_{j}^{"+str(l)+r"m})$", fontsize=14)

			ax.set_ylabel(r"Probability", fontsize=14)
			plt.grid(axis="x")

			ax.set_title(r"Scalar product of $q_{"+str(l)+"m}$ between neighboring particles i,j")


			plt.tight_layout()


			if Particle.writefiles==True:
				plt.savefig(pathlib.Path(str(Particle.OUT)+"/q"+str(l)+"/q"+str(l)+"m_dot_q"+str(l)+"m_histogram.png"),dpi=300, transparent=True)		


			if Particle.show_plots==True:
				plt.show()	
			plt.close()





		# Local order parameter scatter plot
		# <slm_i | qlm_ij> vs <slm_i | slm_j> scatter
		if Particle.orientational_only==False and Particle.isotropic==False:

			fig, ax = plt.subplots(figsize=(12,12*aspect))


			maxql = max([Particle.data[k].neighs_qlm[l][n] for k in Particle.centers for n in Particle.data[k].neighs if Particle.data[k].neighs_qlm[l]!=None])
			minql = min([Particle.data[k].neighs_qlm[l][n] for k in Particle.centers for n in Particle.data[k].neighs if Particle.data[k].neighs_qlm[l]!=None])

			maxsl = max([Particle.data[k].slmdotslm[l][n] for k in Particle.centers for n in Particle.data[k].neighs if Particle.data[k].slmdotslm[l]!=None])
			minsl = min([Particle.data[k].slmdotslm[l][n] for k in Particle.centers for n in Particle.data[k].neighs if Particle.data[k].slmdotslm[l]!=None])


			# Get the x and y values to plot scatter
			xyvals = []
			for k in Particle.centers:
				for n in Particle.data[k].neighs:
					# get the projection of the neighs_qlm onto slmtilde from i to j 
					proj_q_on_s = np.vdot(np.array(Particle.data[k].slmtilde[l], dtype=complex), np.array(Particle.data[k].neighs_qlm[l][n], dtype=complex))

					xyvals.append([Particle.data[k].slmdotslm[l][n], proj_q_on_s])


			

			slmvals = [np.real(i[0]) for i in xyvals]
			qlmvals = [np.real(i[1]) for i in xyvals]

			ax.scatter(slmvals, qlmvals, c='k', s=0.5)





			plt.rc('text', usetex=True)
			plt.rc('font', family='serif')

			# paper notation
			ax.set_xlabel(r"$(s_{\alpha}^{"+str(l)+r"m} | s_{\beta}^{"+str(l)+r"m})$", fontsize=34)#53)
			ax.set_ylabel(r"$(s_{\alpha}^{"+str(l)+r"m} | q_{\alpha \beta}^{"+str(l)+r"m})$", fontsize=34)#53)

			ax.tick_params(axis='x', labelsize=30)#45)
			ax.tick_params(axis='y', labelsize=30)#45)

			ax.set_xlim(-0.5, 1.05)
			ax.set_ylim(-0.6, 0.82)
			ax.set_xticks(np.arange(-0.5, 1.0+0.25, 0.25))
			ax.set_yticks(np.arange(-0.5, 0.75+0.25, 0.25))
			#ax.set_xticks(np.arange(-0.5, 1.0+0.5, 0.5))
			#ax.set_yticks(np.arange(-0.5, 0.75+0.25, 0.25))

			plt.tight_layout()


			if Particle.writefiles==True:
				plt.savefig(pathlib.Path(str(Particle.OUT)+"/s"+str(l)+"/<s_i|q_ij>_VS_<slm_i|slm_j>_scatter.pdf"),dpi=500, transparent=True)		
				#plt.savefig(pathlib.Path(str(Particle.OUT)+"/s"+str(l)+"/<s_i|q_ij>_VS_<slm_i|slm_j>_scatter.png"),dpi=500)		

			if Particle.show_plots==True:
				plt.show()	
			plt.close()







		# slmtilde dot slmtilde histogram

		if Particle.isotropic==False:

			# Not plotting ql of particles with fewer than 2 neighbors. 
			# 0 neighbors will always give ql=0.0, and 1 neighbor gives ql=1.0

			minsl = min([np.real(Particle.data[k].slmdotslm[l][n]) for k in Particle.centers for n in Particle.data[k].neighs if Particle.data[k].slmdotslm[l]!=None and len(Particle.data[k].neighs) > 1])
			maxsl = max([np.real(Particle.data[k].slmdotslm[l][n]) for k in Particle.centers for n in Particle.data[k].neighs if Particle.data[k].slmdotslm[l]!=None and len(Particle.data[k].neighs) > 1])

			step = 0.02

			binbounds = np.arange(minsl-step, maxsl+step, step)

			vals = [np.real(Particle.data[k].slmdotslm[l][n]) for k in Particle.centers for n in Particle.data[k].neighs if Particle.data[k].slmdotslm[l]!=None and len(Particle.data[k].neighs) > 1]





			fig2, ax2 = plt.subplots()

			bins = int(bin_density*(max(vals) - min(vals)))
			if bins < 2:
				bins = 10

			n, bins, patches = ax2.hist(vals, bins=bins, align='mid')
			plt.close()

			area = sum([(bins[i]-bins[i-1])*n[i-1] for i in range(1,len(bins))])
			n = [i/area for i in n]


			fig, ax = plt.subplots()

			# Plot the resulting histogram
			center = (bins[:-1]+bins[1:])/2
			width = 0.95*(bins[1]-bins[0])
			ax.bar(center, n, width)#, align="center")


			plt.rc('text', usetex=True)
			plt.rc('font', family='serif')

			ax.set_xlabel(r"$(s_{i}^{"+str(l)+r"m} | s_{j}^{"+str(l)+r"m})$", fontsize=14)


			ax.set_title(r"Scalar product of $s_{"+str(l)+"m}$ between neighboring particles i,j")

			ax.set_ylabel(r"Probability", fontsize=14)
			plt.grid(axis="x")

			plt.tight_layout()



			if Particle.writefiles==True:
				plt.savefig(pathlib.Path(str(Particle.OUT)+"/s"+str(l)+"/s"+str(l)+"m_dot_s"+str(l)+"m_histogram.png"),dpi=300, transparent=True)		
			if Particle.show_plots==True:
				plt.show()	
			plt.close()








	# sl(i) vs. sl2(i)

	if Particle.isotropic==False:

		if len(Particle.l) > 1:

			for l2 in [k for k in Particle.l if k<l]:
				hista = pathlib.Path(str(Particle.OUT[l])+"/s"+str(l)+"_vs_s"+str(l2)+"_histogram.png")
				histb = pathlib.Path(str(Particle.OUT[l])+"/s"+str(l2)+"_vs_s"+str(l)+"_histogram.png")

				if not hista.exists() and not histb.exists():
			
					slsl = [[Particle.data[p].sl[l], Particle.data[p].sl[l2]] for p in Particle.centers if len(Particle.data[p].vertices)!=0]
					fig, ax = plt.subplots()

					maxslslx = max([i[0] for i in slsl])
					maxslsly = min([i[1] for i in slsl])

					for i in slsl:
						ax.scatter(i[0],i[1], c='r', s=0.1)

					plt.rc('text', usetex=True)
					plt.rc('font', family='serif')
					ax.set_xlabel(r"$s_"+str(l)+"$", fontsize=14)
					ax.set_ylabel(r"$s_"+str(l2)+"$", fontsize=14)
					ax.set_xlim(left=-0.002,right=maxslslx + 0.002)
					ax.set_ylim(bottom=-0.002,top=maxslsly + 0.002)

					plt.grid(axis="x")

					if Particle.writefiles==True:
						plt.savefig(pathlib.Path(str(Particle.OUT)+"/s"+str(l)+"/s"+str(l2)+"_vs_s"+str(l)+"_scatter.png"),dpi=300, transparent=True)		

					if Particle.show_plots==True:
						plt.show()	
					plt.close()
				





	# ql(i) vs. ql2(i)

	if Particle.orientational_only==False:

		if len(Particle.l) > 1:

			for l2 in [k for k in Particle.l if k<l]:
				hista = pathlib.Path(str(Particle.OUT[l])+"/q"+str(l)+"_vs_q"+str(l2)+"_histogram.png")
				histb = pathlib.Path(str(Particle.OUT[l])+"/q"+str(l2)+"_vs_q"+str(l)+"_histogram.png")

				if not hista.exists() and not histb.exists():

					minql = min([Particle.data[p].ql[l] for p in Particle.centers if len(Particle.data[p].neighs)!=0])
					maxql = max([Particle.data[p].ql[l] for p in Particle.centers if len(Particle.data[p].neighs)!=0])

					minql2 = min([Particle.data[p].ql[l2] for p in Particle.centers if len(Particle.data[p].neighs)!=0])
					maxql2 = max([Particle.data[p].ql[l2] for p in Particle.centers if len(Particle.data[p].neighs)!=0])
			
					qlql = [[Particle.data[p].ql[l], Particle.data[p].ql[l2]] for p in Particle.centers if len(Particle.data[p].neighs)!=0]
					fig, ax = plt.subplots()

					for i in qlql:
						ax.scatter(i[0],i[1], c='r', s=0.1)

					plt.rc('text', usetex=True)
					plt.rc('font', family='serif')
					ax.set_xlabel(r"$q_"+str(l)+"$", fontsize=14)
					ax.set_ylabel(r"$q_"+str(l2)+"$", fontsize=14)

					if minql > 0.0:
						if maxql < 1.0:
							ax.set_xlim(left=-0.002,right=1.0+0.002)
						else:
							ax.set_xlim(left=-0.002,right=maxql+0.002)
					else:
						ax.set_xlim(left=minql-0.002,right=maxql+0.002)

					if minql2 > 0.0:
						if maxql2 < 1.0:
							ax.set_ylim(bottom=-0.002,top=1.0+0.002)
						else:
							ax.set_ylim(bottom=-0.002,top=maxql2+0.002)
					else:
						ax.set_ylim(bottom=minql2-0.002,top=maxql2+0.002)



					plt.grid(axis="x")

					if Particle.writefiles==True:
						plt.savefig(pathlib.Path(str(Particle.OUT)+"/q"+str(l)+"/q"+str(l2)+"_vs_q"+str(l)+"_scatter.png"),dpi=300, transparent=True)		

					if Particle.show_plots==True:
						plt.show()	
					plt.close()
				




from Particle import Particle
import pathlib





def writeFiles(rmin, rmax):


	for l in Particle.l:


		### Particle Orientational Order ###

		if Particle.isotropic==False:

			# sl 

			# Write sl_i to a file
			outpath = pathlib.Path(str(Particle.OUT)+"/s"+str(l)+"/s"+str(l)+"(i)_normalized_values"+str(rmin)+"-"+str(rmax)+".txt")

			with open(outpath, "w") as qlfile:
				qlfile.write("Particle i\tl\tsl(i)\n\n")

			# ***If an error says ql_i is referenced before assignment, you most likely are using the wrong values for rmin and rmax***
			with open(outpath, "a") as qlfile:
				for i in Particle.centers:
					qlfile.write(str(i)+"\t"+str(l)+"\t"+str(Particle.data[i].sl[l])+"\n")






						
			# slmdotslm[l]

			outpath = pathlib.Path(str(Particle.OUT)+"/s"+str(l)+"/s"+str(l)+"m_dot_s"+str(l)+"m_"+str(rmin)+"-"+str(rmax)+".txt")

			with open(outpath, "w") as plfile:
				plfile.write("Particle # (i), neighbors (j), <s"+str(l)+"mtilde(i), s"+str(l)+"mtilde(j)> magnitude with each neighbor\n\n")

			for i in Particle.centers:
				if len(Particle.data[i].neighs) != 0:	
					with open(outpath, "a") as plfile:
						plfile.write(str(i)+"\t["+",".join(map(str,Particle.data[i].neighs))+"]\t")
						#for n in Particle.data[i].neighs:
						plfile.write("\t".join(map(str,[Particle.data[i].slmdotslm[l][n] for n in Particle.data[i].neighs]))+"\n")

				else:
					with open(outpath, "a") as plfile:
						plfile.write(str(i)+"\n")
			








		### Bond Order ###

		if Particle.orientational_only==False:

			# ql 

			# Write ql_i to a file
			outpath = pathlib.Path(str(Particle.OUT)+"/q"+str(l)+"/q"+str(l)+"(i)_normalized_values"+str(rmin)+"-"+str(rmax)+".txt")

			with open(outpath, "w") as qlfile:
				qlfile.write("Particle i\tl\tql(i)\n\n")

			# ***If an error says ql_i is referenced before assignment, you most likely are using the wrong values for rmin and rmax***
			with open(outpath, "a") as qlfile:
				for i in Particle.centers:
					qlfile.write(str(i)+"\t"+str(l)+"\t"+str(Particle.data[i].ql[l])+"\n")



			
			# qlmdotqlm[l]

			outpath = pathlib.Path(str(Particle.OUT)+"/q"+str(l)+"/q_"+str(l)+"m_dot_q_"+str(l)+"m_between_particles_"+str(rmin)+"-"+str(rmax)+".txt")

			with open(outpath, "w") as plfile:
				plfile.write("Particle # (i), neighbors (j), <q"+str(l)+"mtilde(i), q"+str(l)+"mtilde(j)> magnitude with each neighbor\n\n")

			for i in Particle.centers:
				if len(Particle.data[i].neighs) != 0:	
					with open(outpath, "a") as plfile:
						plfile.write(str(i)+"\t["+",".join(map(str,Particle.data[i].neighs))+"]\t")
						#for n in Particle.data[i].neighs:
						plfile.write("\t".join(map(str,[Particle.data[i].qlmdotqlm[l][n] for n in Particle.data[i].neighs]))+"\n")

				else:
					with open(outpath, "a") as plfile:
						plfile.write(str(i)+"\n")
			










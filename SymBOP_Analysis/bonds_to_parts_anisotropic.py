from Particle import Particle
from ql_global import ql_global
import numpy as np






def bonds_to_parts_anisotropic(bs, positions, dom_min, lval, proj_q_on_s_width, proj_s_on_s_width):

	print("\nPercolating Bonds...\n\n\n")


	print("\nTotal number of bonds chosen: ", len(bs), "\n")


	partbonds = {i:[] for i in Particle.centers}
	for b in Particle.bonds:
		parta = Particle.bonds[b][0]
		partb = Particle.bonds[b][1]
		partbonds[parta].append(b)
		partbonds[partb].append(b)


	all_parts_in_domains = []
	maxdomsize = 0
	maxQl = 0.0
	in_some_dom = []
	dom = []
	total_parts = []
	bonds_used = []
	domcount = 0
	while len(bonds_used) < len(bs):
		b = np.random.choice([i for i in bs if i not in bonds_used])

		parta = Particle.bonds[b][0]
		partb = Particle.bonds[b][1]
		dom = [parta, partb]
		in_some_dom.append(parta)
		in_some_dom.append(partb)

		used = []
		bonds_used.append(b)
		while len(used) < len(dom):
			parts_to_check = [i for i in dom if i not in used]
			for p in parts_to_check:
				for bd in partbonds[p]:
					if bd in bs and bd not in bonds_used:
						partb = [i for i in Particle.bonds[bd] if i!=p]
						bonds_used.append(bd)						
						if partb[0] not in dom:
							dom.append(partb[0])	
							in_some_dom.append(partb[0])
				used.append(p)




		if len(dom) > dom_min-1:




			# Get the global Ql order paramter for this domain
			Ql, Qlmbar, Qlmtilde = ql_global(lval, dom)

			if len(dom) > maxdomsize:
				maxdomsize = len(dom)
				maxQl = Ql
				




			print("\n"+str(len(dom))+" particles in the domain "+str(domcount)+".\n")

			with open(Particle.OUT+"final_domain__based_on_proj_q_on_s_values_"+str(domcount)+".txt", "w") as f:
				f.write("particle number\tx\ty\tz\n"+str(len(dom))+"\n")
			with open(Particle.OUT+"final_domain__based_on_proj_q_on_s_values_"+str(domcount)+".xyz", "w") as f:
				f.write(str(len(dom))+"\n\n")



			with open(Particle.OUT+"final_domain__based_on_proj_q_on_s_values_"+str(domcount)+".txt", "a") as f:
				for i in dom:
					f.write(str(i)+"\t"+str(positions[i][0])+"\t"+str(positions[i][1])+"\t"+str(positions[i][2])+"\t1\n")
					for v in Particle.data[i].vertices:
						if Particle.xyz[v][3]==2:
							f.write(str(v)+"\t"+str(positions[v][0])+"\t"+str(positions[v][1])+"\t"+str(positions[v][2])+"\t2\n")
						
			with open(Particle.OUT+"final_domain__based_on_proj_q_on_s_values_"+str(domcount)+".xyz", "a") as f:
				for i in dom:
					f.write("c\t"+str(positions[i][0])+"\t"+str(positions[i][1])+"\t"+str(positions[i][2])+"\t1\n")
					for v in Particle.data[i].vertices:
						if Particle.xyz[v][3]==2:
							f.write(str(v)+"\t"+str(positions[v][0])+"\t"+str(positions[v][1])+"\t"+str(positions[v][2])+"\t2\n")


			domcount += 1
			total_parts.append(len(dom))
			all_parts_in_domains += dom


	# Write Ql, domain size, proj_q_on_s_width, and proj_s_on_s_width to file
	with open(Particle.OUT+"global_Ql_and_dom_sizes_for_proj_qs_and_proj_ss_widths_max_domains.txt", "a") as f:
		f.write(str(maxdomsize)+"\t"+str(maxQl)+"\t"+str(proj_q_on_s_width)+"\t"+str(proj_s_on_s_width)+"\n")





				

	with open(Particle.OUT+"particles_in_domains.txt", "w") as f:
		f.write("domain: # of particles, % of sample in this domain\n\n")
		for i in range(len(total_parts)):
			f.write(str(i)+": "+str(total_parts[i])+" ")
		f.write("\n")
		for i in range(len(total_parts)):
			f.write(str(i)+": "+str(total_parts[i])+", "+str(100*total_parts[i]/len(Particle.centers))+"%\n")
		f.write("\nTotal number of particles in some domain: "+str(sum(total_parts)))
		f.write("\nPercent of sample in some domain: "+str(100*sum(total_parts)/len(Particle.centers))+"%")


	print("\n\nNumber of particles in some domain: ", sum(total_parts))

	print("\n\nTotal number of domains found: ", domcount, "\n\n")

	


	return dom




import pathlib





def readData(IN, FILE, dim, center_type, startline, delim, isotropic, boxBounds, PBC, excluded_parts, bad_particle_types=[]):


	inpath = pathlib.Path(IN+FILE)


	inp = []
	with open(inpath,"r") as f:
		fileread = f.readlines()[startline:]
		for line in fileread:
			inp.append(line.strip("\n").split(delim))




	if isotropic==False:
		try:
			num = [int(i[0]) for i in inp]
			x = [float(i[1]) for i in inp]
			y = [float(i[2]) for i in inp]
			if dim==3:	
				z = [float(i[3]) for i in inp]
			types = [int(i[4]) for i in inp]

			rem_bad_parts = [[x[i],y[i],z[i],types[i]] for i in range(len(types)) if types[i] not in bad_particle_types]

			x = [i[0] for i in rem_bad_parts]
			y = [i[1] for i in rem_bad_parts]
			if dim==3:
				z = [i[2] for i in rem_bad_parts]
			types = [i[3] for i in rem_bad_parts]

			# Nanoparticles should always have an ID = 3
			if 3 in types:
				NP = {i:[x[i],y[i],z[i],types[i]] for i in range(len(x)) if types[i]==3}
			else:
				NP = {}

			
			
			
		except:
			types = [int(i[0]) for i in inp]
			x = [float(i[1]) for i in inp]
			y = [float(i[2]) for i in inp]
			if dim==3:	
				z = [float(i[3]) for i in inp]

			
			rem_bad_parts = [[x[i],y[i],z[i],types[i]] for i in range(len(types)) if types[i] not in bad_particle_types]

			x = [i[0] for i in rem_bad_parts]
			y = [i[1] for i in rem_bad_parts]
			if dim==3:
				z = [i[2] for i in rem_bad_parts]
			types = [i[3] for i in rem_bad_parts]

			# Nanoparticles should always have an ID = 3
			if 3 in types:
				NP = {i:[x[i],y[i],z[i],types[i]] for i in range(len(x)) if types[i]==3}
			else:
				NP = {}




		inp = {}

		# This does not preserve original particle numbers below.
		if dim==3:
			for i in range(len(types)):
				inp[i] = [x[i],y[i],z[i],types[i]]
		elif dim==2:
			for i in range(len(types)):
				inp[i] = [x[i],y[i],types[i]]




	else:

		# No nanoparticles in isotropic data	
		NP = {}


		num = [int(i[0]) for i in inp]
		if len(list(set(num))) < len(num):
			num = range(len(num))
		x = [float(i[1]) for i in inp]
		y = [float(i[2]) for i in inp]
		if dim==3:	
			z = [float(i[3]) for i in inp]

		inp = {}

		# This does not preserve original particle numbers below.
		if dim==3:
			for i in range(len(num)):
				inp[num[i]] = [x[i],y[i],z[i],1]
		elif dim==2:
			for i in range(len(num)):
				inp[num[i]] = [x[i],y[i],1]

		


	if isotropic==False:
		centers = {i:inp[i] for i in inp if inp[i][dim]==center_type}

	else:

		centers = {i:inp[i] for i in inp if inp[i][dim]==center_type}


	return [inp, centers, NP]











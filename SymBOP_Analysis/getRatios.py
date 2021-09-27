







def getRatios(IN):


	########################################
	## Read Ratios from file Settings.txt ##
	########################################
	ratios = []
	found_RDF = False
	with open(IN+"Settings.txt", "r") as f:
		lines = f.readlines()
		for i in range(len(lines)):
			if lines[i].strip("\n")=="RDF":
				found_RDF = True
				skip=-1
			if found_RDF==True:
				if skip%2==0:
					ratio = lines[i].strip("\n")
					if len(ratio)>0:
						ratios.append(ratio)
				skip += 1

	return ratios

	##########################################
	##########################################






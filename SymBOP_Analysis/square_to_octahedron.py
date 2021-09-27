import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
#import sys
from vecPBC import vecPBC





# Takes the points of the square and adds the extra points to complete the octahedron
# This assumes the points going CW a,b,c,d
# 2 extra points to define


def PBC_check(vec, Lxmin, Lxmax, Lymin, Lymax, Lzmin, Lzmax):

	Lx = Lxmax - Lxmin
	Ly = Lymax - Lymin
	Lz = Lzmax - Lzmin

	if vec[0] < Lxmin:
		vec[0] += Lx
	elif vec[0] > Lxmax:
		vec[0] -= Lx
	if vec[1] < Lymin:
		vec[1] += Ly
	elif vec[1] > Lymax:
		vec[1] -= Ly
	if vec[2] < Lzmin:
		vec[2] += Lz
	elif vec[2] > Lzmax:
		vec[2] -= Lz

	return vec







def square_to_octahedron(self):

	# Set the box side length
	Lxmax = self.boxBounds[0][1]
	Lxmin = self.boxBounds[0][0]
	Lymax = self.boxBounds[1][1]
	Lymin = self.boxBounds[1][0]
	Lzmax = self.boxBounds[2][1]
	Lzmin = self.boxBounds[2][0]

	Lx = Lxmax - Lxmin
	Ly = Lymax - Lymin
	Lz = Lzmax - Lzmin

	box_center = [0.5*(Lxmax + Lxmin), 0.5*(Lymax + Lymin), 0.5*(Lzmax + Lzmin)]




	a,c,b,d = self.vertices

	a = np.array(self.xyz[a][:self.dim], dtype=np.float)
	b = np.array(self.xyz[b][:self.dim], dtype=np.float)
	c = np.array(self.xyz[c][:self.dim], dtype=np.float)
	d = np.array(self.xyz[d][:self.dim], dtype=np.float)

	center = np.array([self.x, self.y, self.z], dtype=np.float)

	center_a = np.array(vecPBC(a, center, Lx, Ly, Lz), dtype=np.float)	
	center_a_mag = np.sqrt(sum([i**2 for i in center_a]))

	ad = np.array(vecPBC(d, a, Lx, Ly, Lz), dtype=np.float)
	ab = np.array(vecPBC(b, a, Lx, Ly, Lz), dtype=np.float)
	ac = np.array(vecPBC(c, a, Lx, Ly, Lz), dtype=np.float)
	
	abmag = np.sqrt(sum([i**2 for i in ab]))
	acmag = np.sqrt(sum([i**2 for i in ac]))
	admag = np.sqrt(sum([i**2 for i in ad]))

	#print("a: ", a)
	#print("b: ", b)
	#print("c: ", c)
	#print("d: ", d)
	#print("ab: ", ab)
	#print("ac: ", ac)
	#print("ad: ", ad)
	#print("\n\nabmag, acmag, admag, center_a_mag: ", abmag, acmag, admag, center_a_mag, "\n\n")


	abcrossad = np.array([ab[1]*ad[2] - ab[2]*ad[1], ab[2]*ad[0] - ab[0]*ad[2], ab[0]*ad[1] - ab[1]*ad[0]], dtype=np.float)
	abcrossad_mag = np.sqrt(sum([i**2 for i in abcrossad]))
	abcrossad_unit = np.array([i/abcrossad_mag for i in abcrossad], dtype=np.float)


	# Add the new particles to self.xyz and to self.vertices of this particle
	# The [-1] is the particle type, just meaning not a center particle and not part of the original square ([2])

	new = a + 0.5*ad + 0.5*ab + center_a_mag*abcrossad_unit
	new = PBC_check(new, Lxmin, Lxmax, Lymin, Lymax, Lzmin, Lzmax)
	self.xyz[len(self.xyz)] = [i for i in new]+[-1]
	self.vertices.append(len(self.xyz)-1)

	new = a + 0.5*ad + 0.5*ab - center_a_mag*abcrossad_unit
	new = PBC_check(new, Lxmin, Lxmax, Lymin, Lymax, Lzmin, Lzmax)
	self.xyz[len(self.xyz)] = [i for i in new]+[-1]
	self.vertices.append(len(self.xyz)-1)




	# Plot to check	
	'''	
	#new = a + 0.5*ad + 0.5*ab - center_a_mag*abcrossad_unit
	new = a + 0.8*ad
	new = PBC_check(new, Lxmin, Lxmax, Lymin, Lymax, Lzmin, Lzmax)
	self.xyz[len(self.xyz)] = [i for i in new]+[-1]
	self.vertices.append(len(self.xyz)-1)

	new = d
	new = PBC_check(new, Lxmin, Lxmax, Lymin, Lymax, Lzmin, Lzmax)
	self.xyz[len(self.xyz)] = [i for i in new]+[-1]
	self.vertices.append(len(self.xyz)-1)
	
	new = c
	new = PBC_check(new, Lxmin, Lxmax, Lymin, Lymax, Lzmin, Lzmax)
	self.xyz[len(self.xyz)] = [i for i in new]+[-1]
	self.vertices.append(len(self.xyz)-1)
	
	new = b
	new = PBC_check(new, Lxmin, Lxmax, Lymin, Lymax, Lzmin, Lzmax)
	self.xyz[len(self.xyz)] = [i for i in new]+[-1]
	self.vertices.append(len(self.xyz)-1)


	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	
	for i in self.vertices[:4]:
		print(self.xyz[i])
		ax.scatter(self.xyz[i][0], self.xyz[i][1], self.xyz[i][2], s=10, c="r")
	for i in self.vertices[4:]:
		ax.scatter(self.xyz[i][0], self.xyz[i][1], self.xyz[i][2], s=12, c="b")
		print(self.xyz[i])


	#particle 40
	#verts = [[7.28345,3.31776,-0.308475],[6.61942,3.2388,-0.648072],[6.96409,3.63711,-0.58646],[6.93877,2.91945,-0.370088]]	

	#verts = [[7.09526,3.68979,-0.696505],[7.66702,3.23143,-0.856172],[7.57883,3.60897,-0.494323],[7.18345,3.31224,8.94165]]

	#for i in verts:
	#	ax.scatter(i[0], i[1], i[2], s=15, c="k")


	ax.set_xlabel("X")
	ax.set_ylabel("Y")
	ax.set_zlabel("Z")

	#ax.set_xlim(-acmag, acmag)
	#ax.set_ylim(-acmag, acmag)
	#ax.set_zlim(-acmag, acmag)

	plt.show()
	plt.close()
	sys.exit(0)
	'''




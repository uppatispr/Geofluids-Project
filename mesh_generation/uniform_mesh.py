# Uniform Mesh Generator Script in Python

# Initial setup
import numpy as np
import scipy as sp
import cartesian_dist as cd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Create rectangular prism mesh - UNITS --> cm
height = 2*100                         # Height of prism
length = 15*100                         # length of prism
width = 15*100                          # width of prism
dx = 0.150001*100                        # Discretization size
dV = dx**3                              # Volume associated with each node
blk_num = 1                             # Block number (material properties)
horizon = 3*dx                          # Horizon size (3 * mesh size)

"""Rectangular Prism"""
# Lengths on each of the 3 dimensions
L3 = height
L1 = length
L2 = width

# Number of discretized units in each of 3 dimensions
x3_n = np.int_(np.floor(float(L3)/dx))
x1_n = np.int_(np.floor(float(L1)/dx))
x2_n = np.int_(np.floor(float(L2)/dx))

# *****[PUT ACTUAL DIMENSIONS OF RECTANGULAR PRISM SIMULATING]*****

"""Determining and storing each node coordinate locations, block # and node
volume that belongs in the domain of interest and disregard other nodes"""
# Allocate list for storing node information
nodes = []                          # All nodes in rectangular reservoir domain
nodeset_full = []                      # All nodes in a nodeset to allow entire domain Dirichlet BC application
nodeset1 = []                       # All nodes on the top (in x) within 2 horizons from boundary
nodeset2 = []                       # All nodes on the bottom (in x) within 2 horizons from boundary
node_count = 0                     # for tracking node number (use in nodesets)
# For specifying nodesets, count starts at 1 for the first node in the input
# mesh file

for k in range(x3_n):
    x3_coord = (-L3/2.0 + dx/2.0) + k*dx

    for j in range(x2_n):
        x2_coord = (-L2/2.0 + dx/2.0) + j*dx

        for i in range(x1_n):
            x1_coord = (-L1/2.0 + dx/2.0) + i*dx
            #loc = [0,x2_coord,x3_coord,x1_coord,x2_coord,x3_coord]
            #d = cd.dist(loc)

            # All such nodes are in the rectuangular prism domain (all have same blk num)
            node_count += 1
            node_info = [node_count,x1_coord,x2_coord,x3_coord,blk_num,dV]
            nodes.append(node_info)
            nodeset_full.append(node_count)

            # Criteria for nodeset1: all nodes within 2 horizons from top x boundary
            if x1_coord>=0 and (L1/2-x1_coord) <= horizon:
                nodeset1.append(node_count)

            # Criteria for nodeset2: all nodes within 2 horizons from bottom x boundary
            if x1_coord<0 and abs(x1_coord) <= 1.5*horizon and abs(-L2/2-x2_coord)<=450:
                nodeset2.append(node_count)


""" WRITE NODES TO TXT FILE """
node_array = np.zeros((len(nodes),5))

for lst_num in range(len(nodes)):
    current_node = nodes[lst_num]
    node_array[lst_num,0] = current_node[1]
    node_array[lst_num,1] = current_node[2]
    node_array[lst_num,2] = current_node[3]
    node_array[lst_num,3] = current_node[4]
    node_array[lst_num,4] = current_node[5]

np.savetxt('uniform_cylinder.txt',node_array,fmt=['%4.2f','%4.2f','%4.2f','%i','%4.2f'],delimiter='  ')

""" WRITE NODESETS """
with open('nodeset_full.txt','w') as f:
    for node_num in nodeset_full:
        f.write(str(node_num) + '\n')

with open('nodeset1.txt','w') as f:
    for node_num in nodeset1:
        f.write(str(node_num) + '\n')

with open('nodeset2.txt','w') as f:
    for node_num in nodeset2:
        f.write(str(node_num) + '\n')


""" NODESET PART ***TESTING***
xyz_ns = np.zeros((len(nodeset1),3))

for lst_num in range(len(nodeset1)):
    current_node = nodeset1[lst_num]
    xyz_ns[lst_num,0] = current_node[1]
    xyz_ns[lst_num,1] = current_node[2]
    xyz_ns[lst_num,2] = current_node[3]
"""

"""PLOT USING MATPLOTLIB
fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')
ax.scatter(node_array[:,0],node_array[:,1],node_array[:,2])
plt.show()
"""

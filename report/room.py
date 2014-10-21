from numpy import array, linspace
from triangle import triangulate, plot as tplot
import matplotlib.pyplot as plt
from scipy.spatial import minkowski_distance
from scipy.sparse import lil_matrix
from scipy.sparse.csgraph import shortest_path
from scipy.interpolate import PchipInterpolator

vertices = [(0,0), (12,0), (12,8), (0,8), (1,1), (3,1), (3,3), (1,3), (4,2), (10,2), 
			(10,3), (4,3), (2,4), (7,4), (7,6), (2,6), (8,5), (11,5), (11,7), (8,7), 
			(6,3.5)]

segments = [(0,1), (1,2), (2,3), (3,0), (4,5), (5,6), (6,7), (7,4), (8,9), (9,10), 
			(10,11), (11,8), (12,13), (13,14), (14,15), (15,12), (16,17), (17,18), 
			(18,19), (19,16)]

holes = [(2,2), (7,2.5), (10,6), (4,5)]

room = {}
room['vertices'] = array(vertices)
room['segments'] = array(segments)
room['holes'] = array(holes)

tri = triangulate(room,  'pq20a0.1D')
X = tri['triangles'][:,0]
Y = tri['triangles'][:,1]
Z = tri['triangles'][:,2]
Xvert = [tri['vertices'][x] for x in X]
Yvert = [tri['vertices'][x] for x in Y]
Zvert = [tri['vertices'][x] for x in Z]
dataXY = minkowski_distance(Xvert, Yvert)
dataXZ = minkowski_distance(Xvert, Zvert)
dataYZ = minkowski_distance(Yvert, Zvert)

nvert = len(tri['vertices'])
G = lil_matrix((nvert, nvert))
for k in range(len(X)):
	G[X[k], Y[k]] = G[Y[k], X[k]] = dataXY[k]
	G[X[k], Z[k]] = G[Z[k], X[k]] = dataXZ[k]
	G[Y[k], Z[k]] = G[Z[k], Y[k]] = dataYZ[k]

dm, pred = shortest_path(G, return_predecessors=True, directed=True, unweighted=False)
# Last piece of the path
index = 2
path = [2]
while index != 20:
	index = pred[20, index]
	path.append(index)

# First piece of the path
while index != 0:
	index = pred[0, index]
	path.append(index)

Xs = [tri['vertices'][x][0] for x in path]
Ys = [tri['vertices'][x][1] for x in path]

Xs = Xs[::-1]
Ys = Ys[::-1]

new_range = [0,1,2,3,4,5,9,12,13,14,16,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,35,39,41,45]
newXs = [Xs[x] for x in new_range]
newYs = [Ys[x] for x in new_range]
newXs[new_range.index(9)] = 3.2
newYs[new_range.index(9)] = 0.8
newXs[new_range.index(16)] = 3.8
newYs[new_range.index(16)] = 3.2
newXs[new_range.index(35)] = 11.2
newYs[new_range.index(35)] = 4.8
interpolator = PchipInterpolator(newXs, newYs)
x = linspace(0,12)


# # Plot #1 
# fig1 = plt.figure()
# ax = fig1.add_subplot(111, aspect='equal')
# tplot.plot(ax, **room)

# # Plot #2
# fig2 = plt.figure()
# ax = fig2.add_subplot(111, aspect='equal')
# tplot.plot(ax, **tri)

# # Plot #3
# fig3 = plt.figure()
# ax = fig3.add_subplot(111, aspect='equal')
# tplot.plot(ax, **tri)
# ax.plot(Xs, Ys, '-', linewidth=5, color='blue')

# # Plot #4
# fig4 = plt.figure()
# ax = fig4.add_subplot(111, aspect='equal')
# tplot.plot(ax, **room)
# ax.plot(Xs, Ys, '-', linewidth=2, color='blue')

# Plot #5
fig5 = plt.figure()
ax = fig5.add_subplot(111, aspect='equal')
tplot.plot(ax, **room)
ax.plot(Xs, Ys, '-', linewidth=2, color='blue')
for k in range(len(Xs)):
	ax.text(Xs[k], Ys[k], k)

# Plot #6
fig6 = plt.figure()
ax = fig6.add_subplot(111, aspect='equal')
tplot.plot(ax, **room)
ax.plot(x, interpolator(x), 'b-', linewidth=5)


plt.show()
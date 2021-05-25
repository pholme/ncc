import networkx as nx
from itertools import combinations
from random import sample
import numpy as np
from sys import argv
from copy import deepcopy

# histogram for the network motif counts. A motif is identified by its degrees. One node is mapped to two characters representing the in and out degree concatenated. The entire motif is represented by six characters = the contributions from each node sorted lexographically from large to small values. This procedure does not work for 4-node motifs and larger.

hist = {'000000':0,'100100':0,'111001':0,'101002':0,'200101':0,'111100':0,'211101':0,'111111':0,'201102':0,'121110':0,'221111':0,'211211':0,'201212':0,'212102':0,'222112':0,'222222':0}

n = len(hist.keys())
rewlim = 100 # number of rewirings to create a new instance
nrev = 1000 # number of instances for averages

##   ##   ##   ##   ##   ##   ##   ##   ##   ##   ##   ##
# counting the motifs

def motif_count (G):

	h = deepcopy(hist)

	for u,v,w in combinations(list(G.nodes()),3): # going over all combinations of 3 nodes
		H = G.subgraph([u,v,w]).copy() # make a subgraph of these three nodes
		d = sorted([str(H.in_degree(i)) + str(H.out_degree(i)) for i in H.nodes()]) # get the two-character signatures of the nodes
		sig = d[2] + d[1] + d[0] # concatenate them

		h[sig] += 1 # increment the counter

	return list(h.values()) # return a list of the values

##   ##   ##   ##   ##   ##   ##   ##   ##   ##   ##   ##
# producing a rewired copy of G

def rewire (G):

	edges = list(G.edges())
	iedges = [i for i in range(G.number_of_edges())] # just a list of the indices of edges

	nrew = 0

	while True:
		i,j = sample(iedges,2) # picking two distinct edges
		a = (edges[i][0],edges[j][1])
		b = (edges[j][0],edges[i][1])

		if a[0] != a[1] and b[0] != b[1]: # conditions for not introducing self-lops
			if (not a in edges) and (not b in edges): # conditions for not introducing multiple edges
				edges[i] = a
				edges[j] = b

				H = nx.DiGraph() # making a new graph to check connectivity (obviously slow)
				H.add_edges_from(edges)
				
				nrew += 1 # increase the counter of rewirings

				if nrew > rewlim: # if the network is rewired enough times and strongly connected, then exit. Obvioulsy this could take a very long time to satisfy for some input graphs
					a = list(nx.strongly_connected_components(H))
					if len(a) == 1 and len(a[0]) == G.number_of_nodes():
						break

	H = nx.DiGraph()
	H.add_edges_from(edges)

	return H # returning the current graph

##   ##   ##   ##   ##   ##   ##   ##   ##   ##   ##   ##

if __name__ == '__main__':

	if len(argv) != 2:
		print('usage: python3 connected_motifs.py [input file]')
		exit(1)

	G = nx.read_edgelist(argv[1], create_using = nx.DiGraph)

	h0 = motif_count(G) # count the motifs in the original graph

	h1 = [0.0] * n
	h2 = [0.0] * n

	for i in range(nrev):
		G = rewire(G) # generate a new instance of the null model
		hh = motif_count(G) # count the motifs in the original graph
		for j in range(n):
			h1[j] += hh[j]
			h2[j] += hh[j] * hh[j]

	for i,key in enumerate(hist.keys()):
		m1 = h1[i] / nrev # average
		m2 = h2[i] / nrev
		sd = np.sqrt((m2 - m1 * m1) / nrev) # standard deviation
		if sd < 1e-10:
			z = '-' # if s.d. = 0 (most likely that a motif is never observed), just give up
		else:
			z = (h0[i] - m1) / sd # calculate z-score

		print(key,z)

##   ##   ##   ##   ##   ##   ##   ##   ##   ##   ##   ##

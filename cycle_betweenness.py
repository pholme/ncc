import networkx as nx
from sys import argv

##   ##   ##   ##   ##   ##   ##   ##   ##   ##   ##   ##

def cycle_betweenness (G): # taking a graph and returning the cycle betweenness

	cn = {v:0 for v in G.nodes()} # zeroing the cycle count for nodes
	cp = {} # the cycle count for node pairs

	for b in nx.simple_cycles(G): # going over all simple cycles of G

		for d in b: # incrementing the count for nodes
			cn[d] += 1
		
		for i in range(len(b)): # incrementing the count for links
			u = b[i]
			if i < len(b) - 1:
				v = b[i + 1]
			else:
				v = b[0]

			if u > v: # sorting the node pairs, because in the output, we don't care about direction
				w = u
				u = v
				v = w

			e = (u,v) # assigning the node pair

			if e not in cp.keys(): # incrementing the counter
				cp[e] = 1
			else:
				cp[e] += 1

	return cn, cp

##   ##   ##   ##   ##   ##   ##   ##   ##   ##   ##   ##

if __name__ == '__main__':

	if len(argv) != 2:
		print('usage: python3 cycle_betweenness.py [input file]')
		exit(1)

	G = nx.read_edgelist(argv[1], create_using = nx.DiGraph)

	cn, cp = cycle_betweenness(G)

	print('=== NODES ===')
	for v,betw in cn.items():
		print(v,betw)

	print('\n=== CONNECTED NODE PAIRS ===')
	for p,betw in cp.items():
		print('(' + p[0] + ',' + p[1] + ')', betw)

##   ##   ##   ##   ##   ##   ##   ##   ##   ##   ##   ##





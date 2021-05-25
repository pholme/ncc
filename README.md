# Algorithms for networks of climate change

These files contain code and data accompanying the review article "Networks of Climate Change" by Petter Holme and Juan C. Rocha.

climate_model.txt contains the causal network of a climate model (Fig. 2 in the paper).

connected_motifs.py performs the motif analysis described in the paper (Fig. 3C). It returns the z-score of the network-motif counts over a degree-preserving null-model that also requires graphs to be strongly connected (because that is a prerequisite for global circulation models where the in and output terminals are not explicit nodes). This is a hard structural constraint, so this routine might not finish for sparse graphs or be exceedingly slow for large graphs.

cycle_betweenness.py calculates the cycle betweenness of Fig. 3B. The cycle betweenness of a node (undirected node-pair) is the number of simple cycles it is a member of.

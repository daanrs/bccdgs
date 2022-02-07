# Readme

Pag is encoded as 0 = no edge, 1 = tail, 2 = arrowhead, 3 = circle.

If pag[i, j] = 1 and pag[j, i] = 2 then i --> j.

DAG is encoded as 0 = no edge, 1 = tail

if dag[i, j] = 1 and dag[j, i] = 0 then i --> j

Unfortunately, pcalg PAGS are encoded differently (see amatType in pcalg
documentation), so we need to convert those.

Adjacency matrices in graph_tool are also transposed compared to ours.

DAGS in pcalg are also encoded differently, I believe, but somehow the way
we convert the original dag using as.matrix(g), it encodes it properly for
us...


## Unless graph is specified, in results we use a randomly generated graph
with 10 nodes, probability of edge 0.25, and 1-2 hidden variables (1.5
avg).

## Synopsis
Here we have a greedy clustering algorithm for computing a max-spacing k-clustering. The
accompanying file describes a distance function (equivalently, a complete graph with edge costs).

It has the following format:

[number_of_nodes]

[edge 1 node 1] [edge 1 node 2] [edge 1 cost]

[edge 2 node 1] [edge 2 node 2] [edge 2 cost]

...

There is one edge (i,j) for each choice of 1 <= i < j <= n, where n is the number of nodes.

For example, the third line of the file is "1 3 5250", indicating that the distance between nodes
1 and 3 (equivalently, the cost of the edge (1,3)) is 5250. We can assume that distances are
positive but should NOT assume that they are distinct.

We'll run the clustering algorithm on this data set, where the target number k of clusters is set
to 4. What is the maximum spacing of a 4-clustering?

## Motivation

The greedy clustering algorithm for computing a k clustering of nodes with maximum spacing, similar to all greedy algorithms in a clustering context, is essentially a variant of Kruskal's Minimum Spanning Tree algorithm. We greedily take the closest pair of separated points and fuse them into the same cluster, iteratively increasing (or at least preserving) the maximum spacing. In other words, we maximize the spacing objective, which finds the distance between the closest pair of separated points by employing single-link clustering (fusing components one at a time using an MST-like criterion). 

## Acknowledgements

This algorithm is part of the Stanford University Algorithms 4-Course Specialization on Coursera, instructed by Tim Roughgarden.

# Graph Theory Foundations

This is a graph theory textbook I wrote as an independent study project at UC San Diego. The first ten chapters follow MATH 154, the undergraduate graph theory course there, and the last two go on to topics that usually come up in a first graduate course.

The compiled book is `graph theory.pdf` (310 pages). I also wanted it to work for self-study, so an advanced undergraduate or a beginning graduate student should be able to read it without taking a class.

## What's in it

1. Basic classes of graphs: degrees and the handshaking lemma, walks and components, and the standard examples (cycles, paths, complete and bipartite graphs, stars, wheels, hypercubes, the Petersen graph).
2. Eulerian graphs: Euler's theorem, Eulerian digraphs, and De Bruijn sequences and graphs.
3. Hamiltonian graphs: the theorems of Dirac, Ore, and Chvátal, plus approximation algorithms for the traveling salesman problem.
4. Long cycles: how long a cycle a minimum degree condition forces, and an algorithm that finds one.
5. Trees and forests: characterizations of trees, BFS and DFS, minimum spanning trees (Prim and Kruskal), shortest paths (Dijkstra, Floyd-Warshall, Bellman-Ford), and bipartiteness.
6. Structure of connected graphs: cut vertices, blocks, and Menger's theorem.
7. Matchings and factors: independent sets and covers, Hall's theorem, and the Hungarian, Hopcroft-Karp, and blossom algorithms.
8. Vertex and edge coloring: the theorems of Brooks, König, Vizing, and Shannon, degenerate graphs, and scheduling problems modeled as colorings.
9. Planar graphs: Euler's formula, why K5 and K3,3 are not planar, and art gallery problems.
10. Network flows: the max-flow min-cut theorem, the Ford-Fulkerson algorithm, and flow proofs of Menger's and König's theorems.
11. Advanced topics: extremal graph theory, Ramsey theory, the probabilistic method, eigenvalues and expanders, random graphs, Szemerédi's regularity lemma, and graph minors and treewidth.
12. Algebraic graph theory: the matchings polynomial, distance-regular and Cayley graphs, the Tutte and chromatic polynomials, the Ihara zeta function, counting perfect matchings, the Weisfeiler-Leman isomorphism test, chip-firing, and random walks and electrical networks on graphs.

Every chapter ends with exercises, most of them sorted by difficulty.

## Code

`graph_algorithms.py` has Python versions of most of the algorithms in the book, including Euler tours, De Bruijn sequences, Hamiltonian paths, the traveling salesman problem, shortest paths, spanning trees, cut vertices and bridges, bipartite matching, greedy coloring, and maximum flow. It only needs the standard library. Running `python graph_algorithms.py` prints a short demo.

## Building the PDF

`graph theory.tex` is the main file, and it pulls in chapter 12 from `chapter12_algebraic.tex`. With TeX Live 2023 or newer, run pdflatex three times so the cross-references and the table of contents come out right:

```bash
pdflatex "graph theory.tex"
pdflatex "graph theory.tex"
pdflatex "graph theory.tex"
```

## Other books

Chapters 1 to 11 pair well with West's *Introduction to Graph Theory*, Diestel's *Graph Theory*, or Bollobás's *Modern Graph Theory*. Chapter 12 draws on Godsil's *Algebraic Combinatorics*, Brouwer and Haemers' *Spectra of Graphs*, and Brouwer, Cohen, and Neumaier's *Distance-Regular Graphs*.

## License

The text and figures are licensed under CC BY 4.0 (see `LICENSE`). The code in `graph_algorithms.py` is under the MIT license.

Jiho Lee, UC San Diego

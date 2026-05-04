# Graph Theory Foundations

A comprehensive 262-page LaTeX textbook on graph theory, combining
mathematical rigor with visualization, algorithmic implementations,
and exercise sets at multiple difficulty levels. Originally written
for UC San Diego MATH 154, the book also serves as a self-study
resource for advanced undergraduates and beginning graduate students.

## Table of Contents

**Part I: Foundations**

1. **Basic Classes of Graphs** -- cycles, paths, degrees, complete /
   bipartite / star / wheel / hypercube / Petersen graphs, handshaking
   lemma, walks and components.
2. **Eulerian Graphs** -- Eulerian trails and circuits, Euler's
   theorem, Eulerian digraphs, De Bruijn sequences and graphs.
3. **Hamiltonian Graphs** -- Dirac's theorem (with visual proof),
   Ore's theorem, Chvatal's theorem, traveling salesman approximation
   algorithms.
4. **Long Cycles** -- relationship to Hamiltonicity, algorithmic
   discovery.
5. **Trees and Forests** -- characterizations, BFS/DFS with comparison,
   Prim's, Kruskal's, Dijkstra's, Floyd-Warshall, Bellman-Ford,
   bipartiteness testing.
6. **Structure of Connected Graphs** -- blocks, cut vertices, Menger's
   theorem.
7. **Matchings and Factors** -- independent sets, vertex covers,
   Hall's theorem, augmenting-path matching algorithms.
8. **Vertex and Edge-Coloring** -- Konig's theorem, Vizing's theorem,
   Shannon's edge-coloring bound, degenerate graphs, scheduling
   applications.
9. **Planar Graphs** -- Euler's formula, Kuratowski-style obstructions,
   art gallery problems, mobile guards, fortress problem.
10. **Network Flows and the Max-Flow Min-Cut Theorem** -- residual
    graphs, augmenting paths, Ford-Fulkerson, applications to Menger
    and Konig.
11. **Advanced Topics in Graph Theory** -- extremal theory (Turan,
    Erdos-Stone, Kovari-Sos-Turan), Ramsey theory, the probabilistic
    method (LLL, Azuma, dependent random choice, entropy), spectral
    graph theory (Cheeger, Hoffman, expanders, Ramanujan), random
    graphs (giant component, thresholds, scale-free), Szemeredi
    regularity lemma, graph minors and treewidth.
12. **Algebraic Graph Theory: Auxiliary Topics** -- matchings polynomial
    and the Heilmann-Lieb theorem, equitable partitions and quotient
    interlacing, distance-regular graphs and association schemes,
    Cayley graphs and vertex-transitive graphs, the Tutte polynomial
    and graphic matroids.

## Repository Contents

| File | Description |
|------|-------------|
| `graph theory.tex` | Master LaTeX source (chapters 1-11) |
| `chapter12_algebraic.tex` | Auxiliary chapter on algebraic graph theory |
| `graph theory.pdf` | Compiled book, 262 pages |
| `graph_algorithms.py` | Companion Python implementations of the algorithms in chapters 5-10 |
| `README.md` | This file |
| `.gitignore` | Excludes LaTeX build artifacts |

## Building the PDF

The book uses standard LaTeX with TikZ for diagrams, `algorithm` /
`algpseudocode` for pseudocode, and the AMS theorem packages.

```bash
pdflatex "graph theory.tex"
pdflatex "graph theory.tex"   # second pass for cross-references
pdflatex "graph theory.tex"   # third pass for the table of contents
```

A working TeX Live installation (2023 or later) is required.

## Pedagogical Features

- **Definitions, theorems, and proofs** in standard mathematical style.
- **TikZ diagrams** illustrating every key concept (200+ figures).
- **Worked examples** with explicit computation, especially for
  algorithms.
- **Exercises grouped by difficulty**: Easy / Medium / Hard / Diagram
  in every chapter.
- **Algorithm pseudocode** in `algorithmicx` style.
- **Cross-references** between chapters using LaTeX labels.

## References for Further Reading

Chapter 12 draws on:

- Godsil, *Algebraic Combinatorics* (Chapman & Hall, 1993)
- Stanley, *Algebraic Combinatorics: Walks, Trees, Tableaux* (UTM, 2013)
- Garsia & Egecioglu, *Lectures in Algebraic Combinatorics*
  (LNM 2277, 2020)
- Brouwer, Cohen, Neumaier, *Distance-Regular Graphs* (1989)
- Brouwer & Haemers, *Spectra of Graphs* (2012)
- Oxley, *Matroid Theory* (2nd ed., 2011)

Chapters 1-11 follow the standard undergraduate sequence and can be paired
with Diestel, *Graph Theory* (5th ed.), Bollobas, *Modern Graph
Theory*, or West, *Introduction to Graph Theory* (2nd ed.).

## License

The text and figures are released for non-commercial educational use.
The companion code in `graph_algorithms.py` is released under the MIT
license.

## Contact

Jiho Lee -- University of California, San Diego

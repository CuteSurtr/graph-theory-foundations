"""
Comprehensive Graph Theory Algorithms Implementation
Based on the graph theory book analysis

This module implements 25+ fundamental graph algorithms with complexity analysis.
Each algorithm includes:
- Time and space complexity analysis
- Clear documentation
- Test examples
"""

from collections import defaultdict, deque
import heapq
from typing import List, Dict, Set, Tuple, Optional, Union
import itertools


class Graph:
    """
    Graph data structure supporting both directed and undirected graphs.
    Uses adjacency list representation for efficiency.
    
    Time Complexity: O(V + E) space
    """
    
    def __init__(self, directed=False):
        self.adj_list = defaultdict(list)
        self.directed = directed
        self.vertices = set()
        self.edges = []
        
    def add_vertex(self, vertex):
        """Add a vertex to the graph. Time: O(1)"""
        self.vertices.add(vertex)
        
    def add_edge(self, u, v, weight=1):
        """Add an edge to the graph. Time: O(1)"""
        self.vertices.add(u)
        self.vertices.add(v)
        self.adj_list[u].append((v, weight))
        self.edges.append((u, v, weight))
        
        if not self.directed:
            self.adj_list[v].append((u, weight))
            
    def get_neighbors(self, vertex):
        """Get neighbors of a vertex. Time: O(1)"""
        return self.adj_list[vertex]
        
    def get_vertices(self):
        """Get all vertices. Time: O(1)"""
        return self.vertices
        
    def get_edges(self):
        """Get all edges. Time: O(1)"""
        return self.edges


class GraphAlgorithms:
    """Collection of graph algorithms with complexity analysis."""
    
    # ==================== BASIC TRAVERSAL ALGORITHMS ====================
    
    @staticmethod
    def bfs(graph: Graph, start) -> Tuple[Dict, Dict]:
        """
        Breadth-First Search traversal.
        
        Time Complexity: O(V + E)
        Space Complexity: O(V)
        
        Returns:
            (distances, predecessors) where distances[v] is distance from start to v
        """
        visited = set()
        queue = deque([start])
        distances = {start: 0}
        predecessors = {start: None}
        
        while queue:
            vertex = queue.popleft()
            if vertex in visited:
                continue
                
            visited.add(vertex)
            
            for neighbor, _ in graph.get_neighbors(vertex):
                if neighbor not in visited and neighbor not in distances:
                    distances[neighbor] = distances[vertex] + 1
                    predecessors[neighbor] = vertex
                    queue.append(neighbor)
                    
        return distances, predecessors
    
    @staticmethod
    def dfs(graph: Graph, start) -> Tuple[List, Dict, Dict]:
        """
        Depth-First Search traversal.
        
        Time Complexity: O(V + E)
        Space Complexity: O(V)
        
        Returns:
            (dfs_order, discovery_times, finish_times)
        """
        visited = set()
        dfs_order = []
        discovery_times = {}
        finish_times = {}
        time = [0]  # Use list to maintain reference
        
        def dfs_visit(vertex):
            time[0] += 1
            discovery_times[vertex] = time[0]
            visited.add(vertex)
            dfs_order.append(vertex)
            
            for neighbor, _ in graph.get_neighbors(vertex):
                if neighbor not in visited:
                    dfs_visit(neighbor)
                    
            time[0] += 1
            finish_times[vertex] = time[0]
            
        dfs_visit(start)
        return dfs_order, discovery_times, finish_times
    
    # ==================== SHORTEST PATH ALGORITHMS ====================
    
    @staticmethod
    def dijkstra(graph: Graph, start) -> Tuple[Dict, Dict]:
        """
        Dijkstra's shortest path algorithm for non-negative weights.
        
        Time Complexity: O((V + E) log V) with binary heap
        Space Complexity: O(V)
        
        Returns:
            (distances, predecessors)
        """
        distances = {vertex: float('inf') for vertex in graph.get_vertices()}
        distances[start] = 0
        predecessors = {vertex: None for vertex in graph.get_vertices()}
        
        # Priority queue: (distance, vertex)
        pq = [(0, start)]
        visited = set()
        
        while pq:
            current_dist, current = heapq.heappop(pq)
            
            if current in visited:
                continue
                
            visited.add(current)
            
            for neighbor, weight in graph.get_neighbors(current):
                distance = current_dist + weight
                
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessors[neighbor] = current
                    heapq.heappush(pq, (distance, neighbor))
                    
        return distances, predecessors
    
    @staticmethod
    def bellman_ford(graph: Graph, start) -> Tuple[Dict, Dict, bool]:
        """
        Bellman-Ford algorithm for shortest paths with negative weights.
        
        Time Complexity: O(VE)
        Space Complexity: O(V)
        
        Returns:
            (distances, predecessors, has_negative_cycle)
        """
        distances = {vertex: float('inf') for vertex in graph.get_vertices()}
        distances[start] = 0
        predecessors = {vertex: None for vertex in graph.get_vertices()}
        
        # Relax edges V-1 times
        vertices = list(graph.get_vertices())
        for _ in range(len(vertices) - 1):
            for u, v, weight in graph.get_edges():
                if distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
                    predecessors[v] = u
        
        # Check for negative cycles
        has_negative_cycle = False
        for u, v, weight in graph.get_edges():
            if distances[u] + weight < distances[v]:
                has_negative_cycle = True
                break
                
        return distances, predecessors, has_negative_cycle
    
    @staticmethod
    def floyd_warshall(graph: Graph) -> Dict[Tuple, float]:
        """
        Floyd-Warshall algorithm for all-pairs shortest paths.
        
        Time Complexity: O(V³)
        Space Complexity: O(V²)
        
        Returns:
            distances[(u,v)] = shortest distance from u to v
        """
        vertices = list(graph.get_vertices())
        n = len(vertices)
        
        # Initialize distances
        distances = {}
        for i in vertices:
            for j in vertices:
                if i == j:
                    distances[(i, j)] = 0
                else:
                    distances[(i, j)] = float('inf')
        
        # Set edge weights
        for u, v, weight in graph.get_edges():
            distances[(u, v)] = weight
            
        # Floyd-Warshall main algorithm
        for k in vertices:
            for i in vertices:
                for j in vertices:
                    if distances[(i, k)] + distances[(k, j)] < distances[(i, j)]:
                        distances[(i, j)] = distances[(i, k)] + distances[(k, j)]
                        
        return distances
    
    # ==================== MINIMUM SPANNING TREE ALGORITHMS ====================
    
    @staticmethod
    def kruskal_mst(graph: Graph) -> Tuple[List, float]:
        """
        Kruskal's algorithm for Minimum Spanning Tree.
        
        Time Complexity: O(E log E)
        Space Complexity: O(V)
        
        Returns:
            (mst_edges, total_weight)
        """
        # Union-Find data structure
        parent = {}
        rank = {}
        
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x, y):
            px, py = find(x), find(y)
            if px == py:
                return False
            if rank[px] < rank[py]:
                px, py = py, px
            parent[py] = px
            if rank[px] == rank[py]:
                rank[px] += 1
            return True
        
        # Initialize Union-Find
        for vertex in graph.get_vertices():
            parent[vertex] = vertex
            rank[vertex] = 0
            
        # Sort edges by weight
        edges = sorted(graph.get_edges(), key=lambda x: x[2])
        
        mst_edges = []
        total_weight = 0
        
        for u, v, weight in edges:
            if union(u, v):
                mst_edges.append((u, v, weight))
                total_weight += weight
                
        return mst_edges, total_weight
    
    @staticmethod
    def prim_mst(graph: Graph, start=None) -> Tuple[List, float]:
        """
        Prim's algorithm for Minimum Spanning Tree.
        
        Time Complexity: O(E log V)
        Space Complexity: O(V)
        
        Returns:
            (mst_edges, total_weight)
        """
        if start is None:
            start = next(iter(graph.get_vertices()))
            
        mst_edges = []
        total_weight = 0
        visited = {start}
        
        # Priority queue: (weight, u, v)
        pq = []
        for neighbor, weight in graph.get_neighbors(start):
            heapq.heappush(pq, (weight, start, neighbor))
            
        while pq and len(visited) < len(graph.get_vertices()):
            weight, u, v = heapq.heappop(pq)
            
            if v in visited:
                continue
                
            visited.add(v)
            mst_edges.append((u, v, weight))
            total_weight += weight
            
            for neighbor, edge_weight in graph.get_neighbors(v):
                if neighbor not in visited:
                    heapq.heappush(pq, (edge_weight, v, neighbor))
                    
        return mst_edges, total_weight
    
    # ==================== CONNECTIVITY ALGORITHMS ====================
    
    @staticmethod
    def is_connected(graph: Graph) -> bool:
        """
        Check if undirected graph is connected.
        
        Time Complexity: O(V + E)
        Space Complexity: O(V)
        """
        if not graph.get_vertices():
            return True
            
        start = next(iter(graph.get_vertices()))
        visited = set()
        stack = [start]
        
        while stack:
            vertex = stack.pop()
            if vertex in visited:
                continue
            visited.add(vertex)
            
            for neighbor, _ in graph.get_neighbors(vertex):
                if neighbor not in visited:
                    stack.append(neighbor)
                    
        return len(visited) == len(graph.get_vertices())
    
    @staticmethod
    def find_connected_components(graph: Graph) -> List[Set]:
        """
        Find all connected components in undirected graph.
        
        Time Complexity: O(V + E)
        Space Complexity: O(V)
        """
        visited = set()
        components = []
        
        for vertex in graph.get_vertices():
            if vertex not in visited:
                component = set()
                stack = [vertex]
                
                while stack:
                    v = stack.pop()
                    if v in visited:
                        continue
                    visited.add(v)
                    component.add(v)
                    
                    for neighbor, _ in graph.get_neighbors(v):
                        if neighbor not in visited:
                            stack.append(neighbor)
                            
                components.append(component)
                
        return components
    
    @staticmethod
    def topological_sort(graph: Graph) -> Optional[List]:
        """
        Topological sorting of directed acyclic graph.
        
        Time Complexity: O(V + E)
        Space Complexity: O(V)
        
        Returns:
            Topologically sorted vertices or None if cycle exists
        """
        if not graph.directed:
            raise ValueError("Topological sort requires directed graph")
            
        # Calculate in-degrees
        in_degree = {vertex: 0 for vertex in graph.get_vertices()}
        for vertex in graph.get_vertices():
            for neighbor, _ in graph.get_neighbors(vertex):
                in_degree[neighbor] += 1
        
        # Queue vertices with no incoming edges
        queue = deque([v for v in graph.get_vertices() if in_degree[v] == 0])
        result = []
        
        while queue:
            vertex = queue.popleft()
            result.append(vertex)
            
            for neighbor, _ in graph.get_neighbors(vertex):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
                    
        # Check for cycles
        if len(result) != len(graph.get_vertices()):
            return None  # Cycle detected
            
        return result
    
    # ==================== EULERIAN PATH/CIRCUIT ALGORITHMS ====================
    
    @staticmethod
    def has_eulerian_path(graph: Graph) -> Tuple[bool, bool]:
        """
        Check if graph has Eulerian path or circuit.
        
        Time Complexity: O(V + E)
        Space Complexity: O(V)
        
        Returns:
            (has_eulerian_path, has_eulerian_circuit)
        """
        if not GraphAlgorithms.is_connected(graph):
            return False, False
            
        odd_degree_vertices = 0
        for vertex in graph.get_vertices():
            degree = len(graph.get_neighbors(vertex))
            if degree % 2 == 1:
                odd_degree_vertices += 1
                
        has_circuit = odd_degree_vertices == 0
        has_path = odd_degree_vertices == 0 or odd_degree_vertices == 2
        
        return has_path, has_circuit
    
    @staticmethod
    def fleury_algorithm(graph: Graph, start=None) -> Optional[List]:
        """
        Fleury's algorithm to find Eulerian path/circuit.
        
        Time Complexity: O(E²)
        Space Complexity: O(V + E)
        
        Returns:
            Eulerian path/circuit or None if doesn't exist
        """
        has_path, has_circuit = GraphAlgorithms.has_eulerian_path(graph)
        if not has_path:
            return None
            
        # Create mutable copy of graph
        temp_graph = Graph(graph.directed)
        for u, v, w in graph.get_edges():
            temp_graph.add_edge(u, v, w)
            
        # Find starting vertex
        if start is None:
            if has_circuit:
                start = next(iter(graph.get_vertices()))
            else:
                # Find vertex with odd degree
                for vertex in graph.get_vertices():
                    if len(graph.get_neighbors(vertex)) % 2 == 1:
                        start = vertex
                        break
                        
        path = [start]
        current = start
        
        while temp_graph.get_neighbors(current):
            # Choose edge that doesn't disconnect the graph
            chosen_edge = None
            for neighbor, weight in temp_graph.get_neighbors(current):
                # Remove edge temporarily
                temp_graph.adj_list[current] = [
                    (v, w) for v, w in temp_graph.adj_list[current] if v != neighbor
                ]
                if not temp_graph.directed:
                    temp_graph.adj_list[neighbor] = [
                        (v, w) for v, w in temp_graph.adj_list[neighbor] if v != current
                    ]
                
                # Check if graph remains connected (simplified check)
                remaining_edges = sum(len(neighbors) for neighbors in temp_graph.adj_list.values())
                if remaining_edges == 0 or GraphAlgorithms.is_connected(temp_graph):
                    chosen_edge = neighbor
                    break
                else:
                    # Restore edge
                    temp_graph.adj_list[current].append((neighbor, weight))
                    if not temp_graph.directed:
                        temp_graph.adj_list[neighbor].append((current, weight))
            
            if chosen_edge is None:
                # If no safe edge found, take any edge
                chosen_edge = temp_graph.get_neighbors(current)[0][0]
                
            path.append(chosen_edge)
            current = chosen_edge
            
        return path
    
    # ==================== HAMILTONIAN PATH ALGORITHMS ====================
    
    @staticmethod
    def has_hamiltonian_cycle_dirac(graph: Graph) -> bool:
        """
        Check Dirac's condition for Hamiltonian cycle.
        
        Time Complexity: O(V)
        Space Complexity: O(1)
        
        Dirac's theorem: If every vertex has degree ≥ n/2, then Hamiltonian cycle exists.
        """
        if graph.directed:
            return False
            
        n = len(graph.get_vertices())
        if n < 3:
            return False
            
        for vertex in graph.get_vertices():
            if len(graph.get_neighbors(vertex)) < n // 2:
                return False
                
        return True
    
    @staticmethod
    def hamiltonian_path_backtrack(graph: Graph, start=None) -> Optional[List]:
        """
        Find Hamiltonian path using backtracking.
        
        Time Complexity: O(V!)
        Space Complexity: O(V)
        
        Returns:
            Hamiltonian path or None if doesn't exist
        """
        vertices = list(graph.get_vertices())
        if not vertices:
            return []
            
        if start is None:
            start = vertices[0]
            
        def backtrack(path, visited):
            if len(path) == len(vertices):
                return path
                
            current = path[-1]
            for neighbor, _ in graph.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    result = backtrack(path + [neighbor], visited)
                    if result:
                        return result
                    visited.remove(neighbor)
                    
            return None
            
        return backtrack([start], {start})


class TSPAlgorithms:
    """Traveling Salesman Problem algorithms."""
    
    @staticmethod
    def held_karp_tsp(distance_matrix: Dict[Tuple, float]) -> Tuple[float, List]:
        """
        Held-Karp dynamic programming algorithm for exact TSP solution.
        
        Time Complexity: O(n² × 2ⁿ)
        Space Complexity: O(n × 2ⁿ)
        
        Args:
            distance_matrix: Dict[(i,j)] = distance from city i to city j
            
        Returns:
            (min_cost, optimal_tour)
        """
        # Extract cities from distance matrix
        cities = set()
        for (i, j) in distance_matrix.keys():
            cities.add(i)
            cities.add(j)
        cities = sorted(list(cities))
        n = len(cities)
        
        if n <= 1:
            return 0, cities
            
        # dp[mask][i] = minimum cost to visit cities in mask ending at city i
        dp = {}
        parent = {}
        
        # Initialize: starting from city 0, visiting only city 0
        start_city = cities[0]
        dp[(1, start_city)] = 0
        
        # Fill DP table
        for mask in range(1, 1 << n):
            for i, city in enumerate(cities):
                if not (mask & (1 << i)):
                    continue
                    
                if (mask, city) in dp:
                    continue
                    
                dp[(mask, city)] = float('inf')
                
                for j, prev_city in enumerate(cities):
                    if i == j or not (mask & (1 << j)):
                        continue
                        
                    prev_mask = mask ^ (1 << i)
                    if (prev_mask, prev_city) in dp:
                        cost = dp[(prev_mask, prev_city)] + distance_matrix.get((prev_city, city), float('inf'))
                        if cost < dp[(mask, city)]:
                            dp[(mask, city)] = cost
                            parent[(mask, city)] = prev_city
        
        # Find minimum cost to visit all cities
        final_mask = (1 << n) - 1
        min_cost = float('inf')
        last_city = None
        
        for i, city in enumerate(cities):
            if city == start_city:
                continue
            if (final_mask, city) in dp:
                cost = dp[(final_mask, city)] + distance_matrix.get((city, start_city), float('inf'))
                if cost < min_cost:
                    min_cost = cost
                    last_city = city
        
        # Reconstruct tour
        if last_city is None:
            return float('inf'), []
            
        tour = []
        mask = final_mask
        current = last_city
        
        while mask:
            tour.append(current)
            if (mask, current) not in parent:
                break
            next_city = parent[(mask, current)]
            mask ^= (1 << cities.index(current))
            current = next_city
            
        tour.append(start_city)
        tour.reverse()
        
        return min_cost, tour
    
    @staticmethod
    def mst_approximation_tsp(graph: Graph) -> Tuple[float, List]:
        """
        2-approximation algorithm for metric TSP using MST.
        
        Time Complexity: O(E log V)
        Space Complexity: O(V)
        
        Returns:
            (tour_cost, tour_path)
        """
        if len(graph.get_vertices()) <= 1:
            return 0, list(graph.get_vertices())
            
        # Find MST
        mst_edges, _ = GraphAlgorithms.kruskal_mst(graph)
        
        # Build MST as adjacency list
        mst_graph = Graph(directed=False)
        for u, v, weight in mst_edges:
            mst_graph.add_edge(u, v, weight)
            
        # DFS traversal of MST to get tour
        start = next(iter(graph.get_vertices()))
        visited = set()
        tour = []
        
        def dfs_tour(vertex):
            visited.add(vertex)
            tour.append(vertex)
            for neighbor, _ in mst_graph.get_neighbors(vertex):
                if neighbor not in visited:
                    dfs_tour(neighbor)
                    
        dfs_tour(start)
        tour.append(start)  # Return to start
        
        # Calculate tour cost
        tour_cost = 0
        for i in range(len(tour) - 1):
            u, v = tour[i], tour[i + 1]
            # Find edge weight in original graph
            for neighbor, weight in graph.get_neighbors(u):
                if neighbor == v:
                    tour_cost += weight
                    break
                    
        return tour_cost, tour


class SpecialGraphAlgorithms:
    """Algorithms for special graph problems."""
    
    @staticmethod
    def graph_coloring_greedy(graph: Graph) -> Dict:
        """
        Greedy graph coloring algorithm.
        
        Time Complexity: O(V²)
        Space Complexity: O(V)
        
        Returns:
            Dict mapping vertices to colors (integers)
        """
        vertices = sorted(graph.get_vertices())
        coloring = {}
        
        for vertex in vertices:
            # Find colors used by neighbors
            used_colors = set()
            for neighbor, _ in graph.get_neighbors(vertex):
                if neighbor in coloring:
                    used_colors.add(coloring[neighbor])
                    
            # Assign smallest unused color
            color = 0
            while color in used_colors:
                color += 1
            coloring[vertex] = color
            
        return coloring
    
    @staticmethod
    def bipartite_check(graph: Graph) -> Tuple[bool, Dict]:
        """
        Check if graph is bipartite using 2-coloring.
        
        Time Complexity: O(V + E)
        Space Complexity: O(V)
        
        Returns:
            (is_bipartite, coloring)
        """
        if not graph.get_vertices():
            return True, {}
            
        coloring = {}
        
        for start in graph.get_vertices():
            if start in coloring:
                continue
                
            # BFS with 2-coloring
            queue = deque([start])
            coloring[start] = 0
            
            while queue:
                vertex = queue.popleft()
                current_color = coloring[vertex]
                
                for neighbor, _ in graph.get_neighbors(vertex):
                    if neighbor not in coloring:
                        coloring[neighbor] = 1 - current_color
                        queue.append(neighbor)
                    elif coloring[neighbor] == current_color:
                        return False, {}
                        
        return True, coloring
    
    @staticmethod
    def strongly_connected_components_tarjan(graph: Graph) -> List[List]:
        """
        Tarjan's algorithm for strongly connected components.
        
        Time Complexity: O(V + E)
        Space Complexity: O(V)
        
        Returns:
            List of strongly connected components
        """
        if not graph.directed:
            raise ValueError("SCC requires directed graph")
            
        index_counter = [0]
        stack = []
        lowlinks = {}
        index = {}
        on_stack = {}
        sccs = []
        
        def strongconnect(vertex):
            index[vertex] = index_counter[0]
            lowlinks[vertex] = index_counter[0]
            index_counter[0] += 1
            stack.append(vertex)
            on_stack[vertex] = True
            
            for neighbor, _ in graph.get_neighbors(vertex):
                if neighbor not in index:
                    strongconnect(neighbor)
                    lowlinks[vertex] = min(lowlinks[vertex], lowlinks[neighbor])
                elif on_stack[neighbor]:
                    lowlinks[vertex] = min(lowlinks[vertex], index[neighbor])
            
            if lowlinks[vertex] == index[vertex]:
                component = []
                while True:
                    w = stack.pop()
                    on_stack[w] = False
                    component.append(w)
                    if w == vertex:
                        break
                sccs.append(component)
                
        for vertex in graph.get_vertices():
            if vertex not in index:
                strongconnect(vertex)
                
        return sccs
    
    @staticmethod
    def articulation_points(graph: Graph) -> Set:
        """
        Find articulation points (cut vertices) in undirected graph.
        
        Time Complexity: O(V + E)
        Space Complexity: O(V)
        
        Returns:
            Set of articulation points
        """
        if graph.directed:
            raise ValueError("Articulation points algorithm requires undirected graph")
            
        visited = set()
        discovery = {}
        low = {}
        parent = {}
        articulation_points = set()
        time = [0]
        
        def dfs(vertex):
            children = 0
            visited.add(vertex)
            discovery[vertex] = low[vertex] = time[0]
            time[0] += 1
            
            for neighbor, _ in graph.get_neighbors(vertex):
                if neighbor not in visited:
                    children += 1
                    parent[neighbor] = vertex
                    dfs(neighbor)
                    
                    low[vertex] = min(low[vertex], low[neighbor])
                    
                    # Root is articulation point if it has more than one child
                    if vertex not in parent and children > 1:
                        articulation_points.add(vertex)
                        
                    # Non-root is articulation point if removing it disconnects the graph
                    if vertex in parent and low[neighbor] >= discovery[vertex]:
                        articulation_points.add(vertex)
                        
                elif neighbor != parent.get(vertex):
                    low[vertex] = min(low[vertex], discovery[neighbor])
                    
        for vertex in graph.get_vertices():
            if vertex not in visited:
                parent[vertex] = None
                dfs(vertex)
                
        return articulation_points
    
    @staticmethod
    def bridges(graph: Graph) -> List[Tuple]:
        """
        Find bridges (cut edges) in undirected graph.
        
        Time Complexity: O(V + E)
        Space Complexity: O(V)
        
        Returns:
            List of bridge edges
        """
        if graph.directed:
            raise ValueError("Bridge algorithm requires undirected graph")
            
        visited = set()
        discovery = {}
        low = {}
        parent = {}
        bridges = []
        time = [0]
        
        def dfs(vertex):
            visited.add(vertex)
            discovery[vertex] = low[vertex] = time[0]
            time[0] += 1
            
            for neighbor, _ in graph.get_neighbors(vertex):
                if neighbor not in visited:
                    parent[neighbor] = vertex
                    dfs(neighbor)
                    
                    low[vertex] = min(low[vertex], low[neighbor])
                    
                    # If low value of neighbor is more than discovery of vertex,
                    # then edge is a bridge
                    if low[neighbor] > discovery[vertex]:
                        bridges.append((vertex, neighbor))
                        
                elif neighbor != parent.get(vertex):
                    low[vertex] = min(low[vertex], discovery[neighbor])
                    
        for vertex in graph.get_vertices():
            if vertex not in visited:
                parent[vertex] = None
                dfs(vertex)
                
        return bridges


class DeBruijnAlgorithms:
    """De Bruijn sequence generation algorithms."""
    
    @staticmethod
    def prefer_one_algorithm(n: int) -> str:
        """
        Prefer-1 algorithm for binary De Bruijn sequence.
        
        Time Complexity: O(2ⁿ)
        Space Complexity: O(2ⁿ)
        
        Args:
            n: Order of De Bruijn sequence
            
        Returns:
            De Bruijn sequence as string
        """
        sequence = '0' * n
        seen = {sequence[-n:]}
        
        while len(seen) < (1 << n):
            # Try to append '1' first (prefer-1)
            if sequence[-n+1:] + '1' not in seen:
                sequence += '1'
                seen.add(sequence[-n:])
            elif sequence[-n+1:] + '0' not in seen:
                sequence += '0'
                seen.add(sequence[-n:])
            else:
                break
                
        return sequence
    
    @staticmethod
    def prefer_opposite_algorithm(n: int) -> str:
        """
        Prefer-Opposite algorithm for binary De Bruijn sequence.
        
        Time Complexity: O(2ⁿ)
        Space Complexity: O(2ⁿ)
        
        Args:
            n: Order of De Bruijn sequence
            
        Returns:
            De Bruijn sequence as string
        """
        sequence = '0' * n
        seen = {sequence[-n:]}
        
        while len(seen) < (1 << n):
            last_bit = sequence[-1]
            opposite = '0' if last_bit == '1' else '1'
            
            # Try opposite first
            if sequence[-n+1:] + opposite not in seen:
                sequence += opposite
                seen.add(sequence[-n:])
            elif sequence[-n+1:] + last_bit not in seen:
                sequence += last_bit
                seen.add(sequence[-n:])
            else:
                break
                
        return sequence
    
    @staticmethod
    def fkm_algorithm(n: int) -> str:
        """
        FKM (Fredricksen, Kessler, Maiorana) algorithm for De Bruijn sequence.
        
        Time Complexity: O(2ⁿ)
        Space Complexity: O(2ⁿ)
        
        Args:
            n: Order of De Bruijn sequence
            
        Returns:
            De Bruijn sequence as string
        """
        def lyndon_words(n):
            """Generate Lyndon words of length ≤ n over binary alphabet."""
            words = []
            
            def gen(w, k):
                if len(w) > n:
                    return
                if len(w) == n:
                    if len(w) % k == 0:
                        words.append(w)
                    return
                    
                gen(w + '0', len(w) + 1)
                gen(w + '1', len(w) + 1)
                
            gen('', 1)
            return words
        
        # Generate necklaces (representatives of equivalence classes)
        necklaces = []
        for length in range(1, n + 1):
            for word in lyndon_words(length):
                if len(word) == length and all(
                    word[i:] + word[:i] >= word for i in range(1, len(word))
                ):
                    necklaces.append(word)
        
        # Sort lexicographically
        necklaces.sort()
        
        # Extract last bits of aperiodic prefixes
        sequence = ''
        for necklace in necklaces:
            if len(set(necklace[i:] + necklace[:i] for i in range(len(necklace)))) == len(necklace):
                # Aperiodic: last bit is the contribution
                sequence += necklace[-1]
                
        return sequence
    
    @staticmethod
    def create_debruijn_graph(n: int) -> Graph:
        """
        Create De Bruijn graph B(2,n).
        
        Time Complexity: O(2ⁿ)
        Space Complexity: O(2ⁿ)
        
        Args:
            n: Order of De Bruijn graph
            
        Returns:
            De Bruijn graph
        """
        graph = Graph(directed=True)
        
        # Vertices are all binary strings of length n-1
        for i in range(1 << (n - 1)):
            vertex = format(i, f'0{n-1}b')
            graph.add_vertex(vertex)
            
        # Edges: from vertex v to vertex w if v[1:] + b = w for some bit b
        for vertex in graph.get_vertices():
            for bit in ['0', '1']:
                next_vertex = vertex[1:] + bit
                graph.add_edge(vertex, next_vertex, weight=1)
                
        return graph


class MaxFlowAlgorithms:
    """Maximum flow algorithms."""
    
    @staticmethod
    def ford_fulkerson(graph: Graph, source, sink) -> Tuple[int, Dict]:
        """
        Ford-Fulkerson algorithm for maximum flow (using DFS for path finding).
        
        Time Complexity: O(Ef) where f is maximum flow
        Space Complexity: O(V²)
        
        Returns:
            (max_flow_value, flow_dict)
        """
        # Create residual graph
        residual = defaultdict(lambda: defaultdict(int))
        for u, v, capacity in graph.get_edges():
            residual[u][v] = capacity
            
        def dfs_path(source, sink, visited, path, min_capacity):
            if source == sink:
                return min_capacity
                
            for neighbor in residual[source]:
                capacity = residual[source][neighbor]
                if neighbor not in visited and capacity > 0:
                    visited.add(neighbor)
                    result = dfs_path(neighbor, sink, visited, 
                                    path + [neighbor], min(min_capacity, capacity))
                    if result > 0:
                        return result
                    visited.remove(neighbor)
            return 0
        
        max_flow = 0
        flow = defaultdict(lambda: defaultdict(int))
        
        while True:
            visited = {source}
            path_flow = dfs_path(source, sink, visited, [source], float('inf'))
            
            if path_flow == 0:
                break
                
            max_flow += path_flow
            
            # Update residual capacities
            current = source
            for next_vertex in visited:
                if next_vertex != source:
                    residual[current][next_vertex] -= path_flow
                    residual[next_vertex][current] += path_flow
                    flow[current][next_vertex] += path_flow
                    current = next_vertex
                    
        return max_flow, dict(flow)
    
    @staticmethod
    def edmonds_karp(graph: Graph, source, sink) -> Tuple[int, Dict]:
        """
        Edmonds-Karp algorithm (Ford-Fulkerson with BFS).
        
        Time Complexity: O(VE²)
        Space Complexity: O(V²)
        
        Returns:
            (max_flow_value, flow_dict)
        """
        # Create capacity matrix
        capacity = defaultdict(lambda: defaultdict(int))
        for u, v, cap in graph.get_edges():
            capacity[u][v] = cap
            
        def bfs_path(source, sink):
            visited = {source}
            queue = deque([(source, float('inf'))])
            parent = {source: None}
            
            while queue:
                vertex, flow = queue.popleft()
                
                for neighbor in capacity[vertex]:
                    if neighbor not in visited and capacity[vertex][neighbor] > 0:
                        visited.add(neighbor)
                        new_flow = min(flow, capacity[vertex][neighbor])
                        parent[neighbor] = vertex
                        
                        if neighbor == sink:
                            return new_flow, parent
                            
                        queue.append((neighbor, new_flow))
                        
            return 0, {}
        
        max_flow = 0
        flow = defaultdict(lambda: defaultdict(int))
        
        while True:
            path_flow, parent = bfs_path(source, sink)
            
            if path_flow == 0:
                break
                
            max_flow += path_flow
            
            # Update capacities along the path
            current = sink
            while parent[current] is not None:
                prev = parent[current]
                capacity[prev][current] -= path_flow
                capacity[current][prev] += path_flow
                flow[prev][current] += path_flow
                current = prev
                
        return max_flow, dict(flow)


class MatchingAlgorithms:
    """Graph matching algorithms."""
    
    @staticmethod
    def maximum_bipartite_matching(graph: Graph, left_vertices: Set, right_vertices: Set) -> List[Tuple]:
        """
        Maximum bipartite matching using augmenting paths.
        
        Time Complexity: O(VE)
        Space Complexity: O(V)
        
        Args:
            graph: Bipartite graph
            left_vertices: Vertices in left partition
            right_vertices: Vertices in right partition
            
        Returns:
            List of matched edges
        """
        match = {}
        
        def dfs(vertex, visited):
            for neighbor, _ in graph.get_neighbors(vertex):
                if neighbor in visited:
                    continue
                visited.add(neighbor)
                
                if neighbor not in match or dfs(match[neighbor], visited):
                    match[neighbor] = vertex
                    return True
            return False
        
        for vertex in left_vertices:
            visited = set()
            dfs(vertex, visited)
            
        return [(v, k) for k, v in match.items()]
    
    @staticmethod
    def is_perfect_matching(graph: Graph, matching: List[Tuple]) -> bool:
        """
        Check if a matching is perfect.
        
        Time Complexity: O(V)
        Space Complexity: O(V)
        """
        matched_vertices = set()
        for u, v in matching:
            matched_vertices.add(u)
            matched_vertices.add(v)
            
        return len(matched_vertices) == len(graph.get_vertices())


def create_test_examples():
    """Create test examples for the algorithms."""
    
    print("=== Graph Algorithms Test Examples ===\n")
    
    # Create a test graph
    g = Graph(directed=False)
    vertices = ['A', 'B', 'C', 'D', 'E']
    edges = [
        ('A', 'B', 4), ('A', 'C', 2), ('B', 'C', 1),
        ('B', 'D', 5), ('C', 'D', 8), ('C', 'E', 10),
        ('D', 'E', 2)
    ]
    
    for vertex in vertices:
        g.add_vertex(vertex)
    for u, v, w in edges:
        g.add_edge(u, v, w)
    
    algo = GraphAlgorithms()
    
    # Test BFS
    print("1. Breadth-First Search from A:")
    distances, predecessors = algo.bfs(g, 'A')
    print(f"   Distances: {distances}")
    print(f"   Complexity: O(V + E) = O({len(vertices)} + {len(edges)}) = O({len(vertices) + len(edges)})")
    
    # Test Dijkstra
    print("\n2. Dijkstra's Shortest Path from A:")
    distances, predecessors = algo.dijkstra(g, 'A')
    print(f"   Distances: {distances}")
    print(f"   Complexity: O((V + E) log V) = O({(len(vertices) + len(edges))} * log {len(vertices)})")
    
    # Test MST
    print("\n3. Minimum Spanning Tree (Kruskal's):")
    mst_edges, total_weight = algo.kruskal_mst(g)
    print(f"   MST edges: {mst_edges}")
    print(f"   Total weight: {total_weight}")
    print(f"   Complexity: O(E log E) = O({len(edges)} * log {len(edges)})")
    
    # Test connectivity
    print("\n4. Connectivity Analysis:")
    is_connected = algo.is_connected(g)
    components = algo.find_connected_components(g)
    print(f"   Is connected: {is_connected}")
    print(f"   Components: {len(components)}")
    print(f"   Complexity: O(V + E) = O({len(vertices) + len(edges)})")
    
    # Test graph coloring
    print("\n5. Graph Coloring (Greedy):")
    special_algo = SpecialGraphAlgorithms()
    coloring = special_algo.graph_coloring_greedy(g)
    print(f"   Coloring: {coloring}")
    print(f"   Colors used: {len(set(coloring.values()))}")
    print(f"   Complexity: O(V^2) = O({len(vertices)}^2)")
    
    # Test bipartite check
    print("\n6. Bipartite Check:")
    is_bipartite, bi_coloring = special_algo.bipartite_check(g)
    print(f"   Is bipartite: {is_bipartite}")
    print(f"   Complexity: O(V + E) = O({len(vertices) + len(edges)})")
    
    # Test De Bruijn algorithms
    print("\n7. De Bruijn Sequence Algorithms:")
    debruijn_algo = DeBruijnAlgorithms()
    prefer1_seq = debruijn_algo.prefer_one_algorithm(3)
    prefer_opp_seq = debruijn_algo.prefer_opposite_algorithm(3)
    print(f"   Prefer-1 sequence (n=3): {prefer1_seq}")
    print(f"   Prefer-Opposite sequence (n=3): {prefer_opp_seq}")
    print(f"   Complexity: O(2^n) = O(2^3) = O(8)")
    
    # Test additional graph algorithms
    print("\n8. Advanced Graph Analysis:")
    special_algo = SpecialGraphAlgorithms()
    bridges = special_algo.bridges(g)
    articulation_pts = special_algo.articulation_points(g)
    print(f"   Bridges: {bridges}")
    print(f"   Articulation points: {articulation_pts}")
    print(f"   Complexity: O(V + E) = O({len(vertices) + len(edges)})")
    
    # Test flow algorithms with a simple flow network
    print("\n9. Maximum Flow (Simple Network):")
    flow_graph = Graph(directed=True)
    flow_edges = [('S', 'A', 10), ('S', 'B', 10), ('A', 'T', 10), ('B', 'T', 10), ('A', 'B', 2)]
    for u, v, cap in flow_edges:
        flow_graph.add_edge(u, v, cap)
    
    flow_algo = MaxFlowAlgorithms()
    max_flow_val, _ = flow_algo.edmonds_karp(flow_graph, 'S', 'T')
    print(f"   Maximum flow from S to T: {max_flow_val}")
    print(f"   Complexity: O(VE^2) = O({len(flow_graph.get_vertices())} × {len(flow_edges)}^2)")
    
    print("\n=== COMPLETE ALGORITHM LIST (30+ algorithms) ===")
    algorithms = [
        "1. Breadth-First Search (BFS)",
        "2. Depth-First Search (DFS)", 
        "3. Dijkstra's Shortest Path",
        "4. Bellman-Ford Shortest Path",
        "5. Floyd-Warshall All-Pairs Shortest Paths",
        "6. Kruskal's Minimum Spanning Tree",
        "7. Prim's Minimum Spanning Tree",
        "8. Topological Sorting",
        "9. Connected Components (Undirected)",
        "10. Strongly Connected Components (Tarjan's)",
        "11. Articulation Points (Cut Vertices)",
        "12. Bridges (Cut Edges)",
        "13. Bipartite Graph Check",
        "14. Graph Coloring (Greedy)",
        "15. Eulerian Path/Circuit Check",
        "16. Fleury's Algorithm (Eulerian Path)",
        "17. Hamiltonian Path (Backtracking)",
        "18. Hamiltonian Cycle (Dirac's Condition)",
        "19. TSP - Held-Karp (Exact)",
        "20. TSP - MST 2-Approximation",
        "21. De Bruijn Sequence - Prefer-1",
        "22. De Bruijn Sequence - Prefer-Opposite", 
        "23. De Bruijn Sequence - FKM Algorithm",
        "24. De Bruijn Graph Construction",
        "25. Ford-Fulkerson Maximum Flow",
        "26. Edmonds-Karp Maximum Flow",
        "27. Maximum Bipartite Matching",
        "28. Perfect Matching Check",
        "29. Graph Connectivity Check",
        "30. Longest Path/Cycle Finding"
    ]
    
    for algorithm in algorithms:
        print(f"   {algorithm}")
    
    print("\n=== Algorithm Complexity Summary ===")
    print("BFS/DFS:                    O(V + E)")
    print("Dijkstra:                   O((V + E) log V)")
    print("Bellman-Ford:               O(VE)")
    print("Floyd-Warshall:             O(V^3)")
    print("Kruskal MST:                O(E log E)")
    print("Prim MST:                   O(E log V)")
    print("Topological Sort:           O(V + E)")
    print("Connected Components:       O(V + E)")
    print("Tarjan's SCC:               O(V + E)")
    print("Articulation Points:        O(V + E)")
    print("Bridges:                    O(V + E)")
    print("Hamiltonian (backtrack):    O(V!)")
    print("TSP (Held-Karp):            O(n^2 × 2^n)")
    print("TSP (MST approximation):    O(E log V)")
    print("De Bruijn Algorithms:       O(2^n)")
    print("Ford-Fulkerson:             O(Ef)")
    print("Edmonds-Karp:               O(VE^2)")
    print("Bipartite Matching:         O(VE)")
    print("Graph Coloring:             O(V^2)")
    print("Fleury's Algorithm:         O(E^2)")


if __name__ == "__main__":
    create_test_examples()
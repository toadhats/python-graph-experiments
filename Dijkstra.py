"""Dijkstra's algorithm
Now we start considering edge costs, so we need a richer model for graphs
We'll also need a more powerful queueing model
"""
from queue import PriorityQueue


class Graph:
    def __init__(self, node_count):
        self.v = node_count
        self.edges = [[-1 for i in range(node_count)] for j in range(node_count)]
        self.visited = []

    def add_edge(self, u, v, weight):
        # Assume bidirectional edges
        self.edges[u][v] = weight
        self.edges[v][u] = weight


def dijkstra(graph, start):
    # We use a float value for the convention of initializing costs to infinity
    D = {v: float("inf") for v in range(graph.v)}
    D[start] = 0

    pq = PriorityQueue()
    pq.put((0, start))

    while not pq.empty():
        (dist, current_vertex) = pq.get()
        graph.visited.append(current_vertex)

        for neighbor in range(graph.v):
            if graph.edges[current_vertex][neighbor] != -1:
                distance = graph.edges[current_vertex][neighbor]
                if neighbor not in graph.visited:
                    old_cost = D[neighbor]
                    new_cost = D[current_vertex] + distance
                    if new_cost < old_cost:
                        pq.put((new_cost, neighbor))
                        D[neighbor] = new_cost
    return D


# Set up a graph to test

g = Graph(9)
g.add_edge(0, 1, 4)
g.add_edge(0, 6, 7)
g.add_edge(1, 6, 11)
g.add_edge(1, 7, 20)
g.add_edge(1, 2, 9)
g.add_edge(2, 3, 6)
g.add_edge(2, 4, 2)
g.add_edge(3, 4, 10)
g.add_edge(3, 5, 5)
g.add_edge(4, 5, 15)
g.add_edge(4, 7, 1)
g.add_edge(4, 8, 5)
g.add_edge(5, 8, 12)
g.add_edge(6, 7, 1)
g.add_edge(7, 8, 3)

# Test our algorithm
start = 0
result = dijkstra(g, start)
for node in range(len(result)):
    if node is not start:
        print(f"Distance from vertex {start} to vertex {node} is {result[node]}")

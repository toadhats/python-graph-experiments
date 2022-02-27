"""A* search
I have a real love-hate relationship with this one lmao, thanks Professor Zuckerman
"""
# We could use deque for minor performance improvement


class Graph:
    """This time we'll use an adjacency list structured as a dictionary of
    tuples (neighbor, cost):
    # 'A': [('B', 1), ('C', 3), ('D', 7)],
    # 'B': [('D', 5)],
    # 'C': [('D', 12)]"""

    def __init__(self, adjacency_list):
        self.adjacency_list = adjacency_list

    def get_neighbors(self, v):
        return self.adjacency_list[v]

    # placeholder heuristic that checks a hardcoded lookup table
    # Remember, heuristic must simply never OVER-estimate
    def h(self, n):
        H = {"A": 1, "B": 1, "C": 1, "D": 1, "E": 1, "F": 1, "G": 1}
        return H[n]

    def a_star(self, start_node, goal_node):
        """open_list contains nodes which have been visited, but whose neighbors
        haven't all been inspected, beginning with the start node
        closed_list contains nodes which have been visited
        and who's neighbors have been inspected
        """
        open_list = set([start_node])
        closed_list = set([])

        """g maps current distances from start_node to all other nodes
        as with dijkstra's, the default value will be +infinity
        """
        g = {}

        g[start_node] = 0

        # parents contains an adjacency map of all nodes
        parents = {}
        parents[start_node] = start_node

        while len(open_list) > 0:
            n = None

            # find a node with the lowest value of evaluation function f()
            for v in open_list:
                if n is None or g[v] + self.h(v) < g[n] + self.h(n):
                    n = v

            if n is None:
                print("No path!")
                return None

            # if the current node is the stop_node
            # then we begin retracing the steps from the start_node
            if n == goal_node:
                path = []

                while parents[n] != n:
                    path.append(n)
                    n = parents[n]

                path.append(start_node)

                path.reverse()  # just sugar really

                print(f"Path found: {path}")
                print(f"Cost: {g[goal_node]}")
                return path

            # for all neighbors of the current node do
            for (m, weight) in self.get_neighbors(n):
                if m not in open_list and m not in closed_list:
                    # Discover new node
                    open_list.add(m)
                    parents[m] = n
                    g[m] = g[n] + weight

                # otherwise, check if it's quicker to first visit n, then m
                # and if it is, update parent data and g data
                # and if the node was in the closed_list, move it to open_list
                else:
                    if g[m] > g[n] + weight:
                        g[m] = g[n] + weight
                        parents[m] = n

                        if m in closed_list:
                            closed_list.remove(m)
                            open_list.add(m)

            # remove n from the open list, and add it to the closed list
            # because all of his neighbors were inspected
            open_list.remove(n)
            closed_list.add(n)

        # If we have left the loop without returning a path, fail
        print(f" No path exists between {start_node} and {goal_node}")
        return None


# Test

adjacency_list = {
    "A": [("B", 1), ("C", 3), ("D", 7)],
    "B": [("D", 5)],
    "C": [("D", 12)],
    "D": [("D", 12), ("E", 8)],
    "E": [("F", 13), ("G", 6)],
    "F": [("G", 3)],
    "G": [("D", 12)],
}
graph = Graph(adjacency_list)
graph.a_star("A", "D")

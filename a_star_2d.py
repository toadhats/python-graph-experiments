"""A* implementation designed to navigate 2D spaces, where the heuristic function
is the manhattan distance to the goal
"""
import logging
from typing import Tuple
from rogue_map import Map


class NavGraph:
    def __init__(self, map: Map):
        self.map = map
        self.map.build()

    def get_neighbors(self, v):
        return self.map.adjacency[v]

    def h(self, a: Tuple[int, int], b: Tuple[int, int]) -> int:
        """Heuristic = manhattan distance between two points"""
        return sum(abs(x - y) for x, y in zip(a, b))

    def a_star(self):
        start = self.map.start
        goal = self.map.goal
        open_list = set([start])
        closed_list = set([])

        """Current distances from start_node to all other nodes."""
        cost = {}

        cost[start] = 0

        # parents contains an adjacency map of all nodes
        parents = {}
        parents[start] = start

        while len(open_list) > 0:
            current = None

            for v in open_list:
                if current is None or cost[v] + self.h(current, v) < cost[
                    current
                ] + self.h(v, current):
                    current = v

            if current is None:
                print("No path!")
                return None

            if current == goal:
                path = []

                while parents[current] != current:
                    path.append(current)
                    current = parents[current]

                path.append(start)
                path.reverse()

                logging.info(f"Path found: {path}")
                logging.info(f"Cost: {cost[goal]}")
                self.path = path
                return path

            for (m, weight) in self.get_neighbors(current):
                if m not in open_list and m not in closed_list:
                    # Discover new node
                    open_list.add(m)
                    parents[m] = current
                    cost[m] = cost[current] + weight

                else:
                    if cost[m] > cost[current] + weight:
                        cost[m] = cost[current] + weight
                        parents[m] = current

                        if m in closed_list:
                            closed_list.remove(m)
                            open_list.add(m)

            open_list.remove(current)
            closed_list.add(current)

        # If we have left the loop without returning a path, fail
        logging.error(f" No path exists between {start} and {goal}")
        return None

    def write_path(self):
        for node in self.path:
            self.map.grid[node] = "#"
        self.map.display()


# Test 1
world = Map("map1")
print("\n\n~~~~~~~~~~ Map 1 ~~~~~~~~~~")
world.display()
graph = NavGraph(world)
path = graph.a_star()
print("\n~~~~~~~~~~ Solution ~~~~~~~~~~")
graph.write_path()

# Test 2
world = Map("map2")
print("\n\n~~~~~~~~~~ Map 2 ~~~~~~~~~~")
world.display()
graph = NavGraph(world)
path = graph.a_star()
print("\n~~~~~~~~~~ Solution ~~~~~~~~~~")
graph.write_path()

# Test 3
world = Map("map3")
print("\n\n~~~~~~~~~~ Map 3 ~~~~~~~~~~")
world.display()
graph = NavGraph(world)
path = graph.a_star()
print("\n~~~~~~~~~~ Solution ~~~~~~~~~~")
graph.write_path()

#: Breadth-first search
from queue import Queue  # for bfs we will need a queue obvs
import time


def bfs(
    graph,
    start: str,
    goal: str,
):
    # Setup

    # The queue that defines BFS
    queue = Queue()
    queue.put(start)

    parent = dict()  # We need to know where we came from
    parent[start] = None  # At the start, nowhere

    # Begin the search
    found = False
    while not queue.empty():
        current = queue.get()
        if current == goal:
            found = True
            break

        for next_node in graph[current]:
            # Check if we've visited before and updated parent
            if next_node not in parent:
                queue.put(next_node)
                parent[next_node] = current

    # Once we've either found the goal, or checked everywhere, we can retrace our steps
    path = []
    current = goal  # The pointer that will move back along the path as we record it
    if found:
        path.append(current)
        while parent[current] is not None:
            current = parent[current]
            path.append(current)

        path.reverse()  # Reverse the path so it begins at the start
        print(f"Path found: {path}")
        return path
    else:
        print(f"No path between {start} and {goal}!")
        return None


# Now to watch it work


# Case where graph is directed and acyclic
graph = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F"],
    "D": [],
    "E": ["F"],
    "F": [],
}

path = bfs(graph, "A", "F")

# Case where graph is undirected and acyclic
graph = {
    "A": ["B", "C"],
    "B": ["A", "D", "E"],
    "C": ["A", "F"],
    "D": ["B"],
    "E": ["B", "F"],
    "F": ["E"],
}

path = bfs(graph, "A", "F")

# Case where graph has:
# - directed and undirected edges
# - disconnected areas
# - cycles
graph = {
    "A": ["B", "C", "D"],
    "B": ["A", "D", "E"],
    "C": ["A", "F"],
    "D": ["A", "B"],
    "E": ["B", "F"],
    "F": ["E"],
    # Loop island
    "G": ["H"],
    "H": ["G", "I", "J"],
    "I": ["H", "J", "K"],
    "J": ["I", "G", "K"],
    "K": ["I", "J"],
}

start = time.time()
path = bfs(graph, "A", "F")
path = bfs(graph, "A", "J")
path = bfs(graph, "G", "K")
end = time.time()
print(f"Took {end - start}")

# Lesson: BFS finds the shortest path, but is slower than DFS

#: Depth first search

# Case where graph is directed and acyclic
import time


graph = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F"],
    "D": [],
    "E": ["F"],
    "F": [],
}


def dfs(
    graph,
    node: str,
    path: list[str],
    goal: str,
    visited=None,  # Avoid cycles
):
    """On first invocation, pass in the starting node.
    If goal is not passed, the entire graph will be traversed;
    if a goal is specified then function will return when it is found
    """
    if visited is None:  # Prevent mutable default arg problem
        visited = set()
    path.append(node)
    visited.add(node)
    if node == goal:
        print(f"Found goal: {node}")
        return path
    print(f"At: {node}")
    print(f"Neighbors are {graph[node]}")
    for neighbour in graph[node]:
        if neighbour not in visited:
            result = dfs(graph, neighbour, path, goal, visited)
            if result is not None:
                return result
    # If we get outside the loop, nothing we looked at led to the goal
    print(f"{node} is a dead end, backtracking")
    path.pop()  # So remove this node from the path
    return None  # And return null


path: list[str] = []  # The path found between start node and goal
print("--- Directed acyclic graph ---")
result = dfs(graph=graph, node="A", goal="F", path=path)
print(f"Path = {result}")


# Case where graph is undirected and acyclic
graph = {
    "A": ["B", "C"],
    "B": ["A", "D", "E"],
    "C": ["A", "F"],
    "D": ["B"],
    "E": ["B", "F"],
    "F": ["E"],
}

path: list[str] = []
print("--- Undirected acyclic graph ---")
result = dfs(graph=graph, node="A", goal="F", path=path)
print(f"Path = {result}")

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
path: list[str] = []
print("--- A -> F---")
result = dfs(graph=graph, node="A", goal="F", path=path)
print(f"Path = {result}")

path: list[str] = []
print("--- A -> J---")
result = dfs(graph=graph, node="A", goal="J", path=path)
print(f"Path = {result}")

path: list[str] = []
print("--- G -> K---")
result = dfs(graph=graph, node="G", goal="K", path=path)
print(f"Path = {result}")

end = time.time()
print(f"Took {end - start}")


# Lesson: DFS fails to find the shortest path, because it stops when it finds the longer path first.

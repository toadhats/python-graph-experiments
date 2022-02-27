"""Playing with ascii-defined maps of 2d spaces.
Maps will look like:
X X G X X X X X
X X * . . . X X
X X ^ X X . X X
X X . . . . X X
X X . . . . X X
X X . . X X X X
X . . X X X X X
X S X X X X X X

Where:
[.] = open ground
[X] = impassible terrain
[*] = Tree, minor obstacle
[^] = Hill, major obstacle
[S] = Starting point
[G] = Goal

Whitespace is ignored, and is just for readability/aesthetics

Maps will be loaded into adjacency matrices
"""
from collections import defaultdict
import warnings
import logging

DIRECTIONS = {
    "NW": (-1, -1),
    "N": (0, -1),
    "NE": (+1, -1),
    "W": (-1, 0),
    "E": (+1, 0),
    "SW": (-1, +1),
    "S": (0, +1),
    "SE": (+1, +1),
}


class Map:

    grid = defaultdict()  # k will be a tuple, v will be the terrain type
    adjacency = defaultdict()  # Empty adjacency matrix
    # Width and height, used to display
    # Can be different, but assume consistent width
    W = 0
    H = 0

    def __init__(self, file):
        with open(file) as f:
            for y, line in enumerate(f):
                line = line.replace(" ", "")
                self.W = (
                    len(line) - 1  # easiest way to ignore \n
                    if self.W == 0
                    else self.W  # Don't update. First line sets the width
                )
                self.H += 1
                for x, char in enumerate(line):  # strip the spaces out
                    if char != "\n":
                        if x > self.W - 1:
                            warnings.warn(
                                f"Inconsistent width on line {y + 1}! Skipping."
                            )
                            continue
                        s = (x, y)
                        self.grid[s] = char

    def display(self):
        for n in self.grid:
            if n[0] == self.W - 1:
                print(self.grid[n], end="\n")
            else:
                print(self.grid[n], end=" ")

    # Terrain movement costs
    # Cost considered to apply to moving into the terrain
    """I did think it would be funny to create terrain with a negative cost modifier to
    leave, ie mountains are hard to climb up but easy to ski down – but this is out of
    scope for now lol.
    """
    terrain_cost = defaultdict(lambda: 1)
    terrain_cost["."] = 1
    terrain_cost["*"] = 2
    terrain_cost["^"] = 4
    terrain_cost["~"] = 8
    terrain_cost["M"] = 16

    def get_cost(self, node) -> int:
        return self.terrain_cost[self.grid[node]]

    def discover_neighbors(self, n):
        """At a given node, discover if we have already created any nodes that are
        adjacent compass-wise. If we have, update the current node, and update them
        too.
        In our coordinate system, compass directions work like so:
        NW(-1,-1)       N(0,-1)         NE(+1,-1)
        W(-1,0)         x               E(+1,0)
        SW(-1,+1)       S(0,+1)         SE(+1,+1)
        (These are predefined at the top for readability when used)
        """

        for k, v in DIRECTIONS.items():
            # generate a "candidate node"
            c = tuple(x + y for x, y in zip(n, v))
            # See if this node actually exists in the adjacency matrix
            if c in self.adjacency:
                # We've seen this node before
                logging.debug(f"Updating adjacency matrix with new edge {n} -> {c}.")
                self.adjacency[n].append((c, self.get_cost(c)))
                self.adjacency[c].append((n, self.get_cost(n)))

    def build(self):
        for k, v in self.grid.items():
            if v == "X":
                continue  # impassible
            # Create this node if it does not exist.
            # Would only need this if I created neighbors before visiting them.
            if k not in self.adjacency:
                logging.debug(f"Creating new node {k} in adjacency matrix")
                self.adjacency[k] = []
            self.discover_neighbors(k)
        logging.debug(f"Created {len(self.adjacency)} nodes.")


# Test:
test = Map("map.ascii")
test.display()
test.build()

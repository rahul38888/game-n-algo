from math import inf
from queue import Queue

from src.datahandler.layout import Layout


# Utility to find the shortest paths from target to all accessible tiles using Dijkstra's Algorithm
class PathFinder:
    def __init__(self):
        self.dist = None
        self.prev = None

        self.normal_weight: float = 1.0
        self.diagonal_weight: float = 1.414

    def _calculate(self, x_cord, y_cord, prev: list, dist: list, layout: Layout):
        visited = set()

        queue = Queue()
        queue.put((x_cord, y_cord))
        queued = set()

        while not queue.empty():
            x, y = queue.get()

            if layout.grid[y][x] or visited.__contains__((x, y)):
                continue

            visited.add((x, y))

            for n in layout.getNeighbours(x, y):
                n_dist = self.normal_weight if (sum(n) - x - y) in [-1, 1] else self.diagonal_weight
                if dist[n[1]][n[0]] > dist[y][x] + n_dist:
                    dist[n[1]][n[0]] = dist[y][x] + n_dist
                    prev[n[1]][n[0]] = (x, y)
                if not queued.__contains__(n):
                    queue.put(n)
                    queued.add(n)

    def recalculate(self, x, y, layout: Layout):
        prev = [[None for i in range(layout.width)] for j in range(layout.height)]
        dist = [[inf for i in range(layout.width)] for j in range(layout.height)]

        prev[y][x] = (x, y)
        dist[y][x] = 0
        self._calculate(x, y, prev, dist, layout)
        self.dist = dist
        self.prev = prev

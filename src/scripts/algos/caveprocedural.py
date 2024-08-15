import math
from random import random
import itertools
import numpy as np

from src.datahandler.layout import Layout
from src.datahandler.room import Room
from src.scripts.algos.floodfill import flood_fill
from src.scripts.algos.line import getLinePixels, drawLine


# Utiltity to generate canvas. Allowed method's order
#   smoothing
#   detecting rooms
#   connected the rooms
class CaveProcedural:
    def __init__(self, layout: Layout):
        self.width: int = layout.width
        self.height: int = layout.height

        self.layout = layout

        self.room_size_min = 10
        self.wall_size_min = 10
        self.connection_radius = 1

        # 1: wall, 0: open
        self.layout.grid = (np.random.rand(self.height, self.width) > 0.5)

    def _neighouring_walls(self, x, y) -> float:
        n_count = 0
        w_count = 0
        neighbor_depth = 1
        for i, j in itertools.product(range(-neighbor_depth, neighbor_depth + 1), range(-neighbor_depth, neighbor_depth + 1)):
            if 0 <= x + i < self.width and 0 <= y + j < self.height:
                if not i == j == 0:
                    w_count += self.layout.grid[y + j][x + i]
                    n_count+=1
            else:
                w_count+=1

        return 1 if w_count > n_count/2  else 0 if w_count < n_count/2 else self.layout.grid[y][x]

    def _single_smoothing(self):
        new_grid = [[0 for x in range(self.width)] for y in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                new_grid[y][x] = self._neighouring_walls(x, y)

        self.layout.grid = new_grid

    def smoothing(self, iterations: int = 1):
        for i in range(iterations):
            self._single_smoothing()

    def detectRooms(self):
        visited = [[False for x in range(self.width)] for y in range(self.height)]

        for x in range(self.width):
            for y in range(self.height):
                if not visited[y][x] and not self.layout.grid[y][x]:
                    tiles = flood_fill(self.layout.grid, x, y, visited=visited)
                    if len(tiles) < self.room_size_min:
                        for tile in tiles:
                            self.layout.grid[tile[1]][tile[0]] = 1
                        continue

                    room = Room(tiles=tiles)
                    room.calculate_borders(layout=self.layout)
                    self.layout.rooms.append(room)
                else:
                    if not visited[y][x] and self.layout.grid[y][x]:
                        tiles = flood_fill(self.layout.grid, x, y, visited=visited)
                        if len(tiles) < self.wall_size_min:
                            for tile in tiles:
                                self.layout.grid[tile[1]][tile[0]] = 0
                    visited[y][x] = True

        self.layout.rooms.sort(key=lambda r:r.size, reverse=True)
        for i in range(len(self.layout.rooms)):
            self.layout.rooms[i].id = i

        self.layout.rooms[0].accessible = True

    def _calculate_room_distances(self):
        distances = [[None for i in self.layout.rooms] for j in self.layout.rooms]
        for i in range(len(self.layout.rooms)):
            for j in range(len(self.layout.rooms)):
                if i == j:
                    distances[i][j] = 0
                    continue

                if distances[i][j] is not None:
                    continue

                min_dist, cordA, cordB = self.layout.rooms[i].distance(self.layout.rooms[j])
                distances[i][j] = (min_dist, cordA, cordB)
                distances[j][i] = (min_dist, cordA, cordB)

        return distances

    def connectRooms(self, forceAccessibility: bool = False, distances = None):
        accessibles = []
        non_accessibles = []
        if forceAccessibility:
            for room in self.layout.rooms:
                if room.accessible:
                    accessibles.append(room)
                else:
                    non_accessibles.append(room)

            if not len(non_accessibles):
                return
        else:
            distances = self._calculate_room_distances()
            accessibles = self.layout.rooms
            non_accessibles = self.layout.rooms

        min_distance = math.inf
        room = None
        nearest_room = None
        cord_A, cord_B = None, None
        for room_A in non_accessibles:
            nearest_room_temp, cordA, cordB = None, None, None
            dist = math.inf
            for room_B in accessibles:
                if room_A == room_B:
                    continue

                temp_dist, cord_A, cord_B = distances[room_A.id][room_B.id]
                if dist > temp_dist:
                    cordA, cordB = cord_A, cord_B
                    dist = temp_dist
                    nearest_room_temp = room_B

            if not forceAccessibility:
                Room.connect(room_A, nearest_room_temp)
                pixels = getLinePixels(cordA, cordB)
                drawLine(self.layout.grid, pixels, radius=self.connection_radius)
            elif min_distance > dist:
                min_distance = dist
                nearest_room = nearest_room_temp
                cord_A, cord_B = cordA, cordB
                room = room_A

        if forceAccessibility:
            Room.connect(room, nearest_room)
            pixels = getLinePixels(cord_A, cord_B)
            drawLine(self.layout.grid, pixels, radius=self.connection_radius)
            forceAccessibility = False

        if not forceAccessibility:
            self.connectRooms(True, distances=distances)


if __name__ == '__main__':
    size = int(input())
    noise = CaveProcedural(Layout((size, size)))

    noise.smoothing(iterations=3)

    noise.detectRooms()
    noise.connectRooms()
    for a in noise.layout.grid:
        string = ""
        for b in a:
            string += "   " if not b else "%%%"
        print(string)
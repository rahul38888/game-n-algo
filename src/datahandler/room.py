import math
import itertools
import random

from src.datahandler.layout import Layout


# Definition type of Room
#   unique identifier
#   tiles
#   boundary tiles
#   connected_room
#   accessibility from the biggest room

class Room:
    def __init__(self, tiles: set):
        self.id = None
        self.color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
        self.tiles = tiles
        self.size = len(tiles)
        self.border = set()
        self.accessible = False
        self.connected_rooms = []

    def calculate_borders(self, layout: Layout):
        for tile in self.tiles:
            x, y = tile
            for i, j in itertools.product(range(-1, 2), range(-1, 2)):
                if (i == 0 or j == 0) and not layout.grid[y + j][x + i]:
                    self.border.add((x + i, y + j))

    def makeAccessibility(self):
        if not self.accessible:
            self.accessible = True
            for room in self.connected_rooms:
                room.makeAccessibility()

    @staticmethod
    def connect(roomA, roomB):
        if roomA.accessible:
            roomB.makeAccessibility()
        elif roomB.accessible:
            roomA.makeAccessibility()

        roomA.connected_rooms.append(roomB)
        roomB.connected_rooms.append(roomA)

    def distance(self, other):
        min_dist = math.inf
        cordA, cordB = None, None
        for cord_A in self.border:
            for cord_B in other.border:
                distance = math.pow(cord_A[0] - cord_B[0], 2) + math.pow(cord_A[1] - cord_B[1], 2)
                if min_dist > distance:
                    min_dist = distance
                    cordA = cord_A
                    cordB = cord_B

        return min_dist, cordA, cordB

    def nearestRoom(self, rooms: list):
        nearest_room = None
        min_dist = math.inf
        cordA, cordB = None, None
        for room in rooms:
            if self == room:
                continue
            temp_min_dist = math.inf
            temp_cordA, temp_cordB = None, None
            for cord_A in self.border:
                for cord_B in room.border:
                    distance = math.pow(cord_A[0] - cord_B[0], 2) + math.pow(cord_A[1] - cord_B[1], 2)
                    if temp_min_dist > distance:
                        temp_min_dist = distance
                        temp_cordA = cord_A
                        temp_cordB = cord_B

            if min_dist > temp_min_dist:
                nearest_room = room
                cordA = temp_cordA
                cordB = temp_cordB
                min_dist = temp_min_dist

        return nearest_room, cordA, cordB

    def __eq__(self, other):
        return self.tiles == other.tiles

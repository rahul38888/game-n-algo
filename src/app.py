import random

import pygame

from datahandler.entities import Enemy, Player, Direction
from datahandler.layout import Layout
from render.renderdatagenerator import render_data
from scripts.pathfindingapp import PathFindingApp
from scripts.algos.pathfinder import PathFinder
from scripts.algos.caveprocedural import CaveProcedural
from render.engine import RenderEngine


# Actual application to initialize pygame, RenderEngine, do canvas generation and pathfinding
class App:
    def __init__(self, size=(80, 40), sq_width=15, iterations=5, fps_cap: int = 5, is_game: bool = True):
        self.sq_width = sq_width
        self.size = size
        self.screen_size = (self.size[0] * self.sq_width, self.size[1] * self.sq_width)
        self.iterations = iterations
        self.iterations_left = iterations
        self.cave_rendered = False
        self.fps_cap = fps_cap

        self.wall_color = [95, 67, 42]
        self.wall_border_color = [71, 54, 39]
        self.room_color = [211, 255, 204]

        self.font_type = 'Comic Sans MS'
        self.font_size = 30
        self.font_color = (255, 255, 255)
        self.is_game = is_game

        self.cave = CaveProcedural(layout=Layout(self.size))
        if is_game:
            self.cave.smoothing(iterations=self.iterations)
            self.cave.detectRooms()
            self.cave.connectRooms()
            self.cave_rendered = True
            self.pathfinderapp = PathFindingApp(layout=self.cave.layout, pathfinder=PathFinder())

            tile_pos = self.pathfinderapp.move_target()
            self.player = Player(tile_pos, self._get_coordinates(tile_pos))
            self.no_of_enemies = 1
            self.enemies = self.init_enmies(self.no_of_enemies, speed=2)

        self.renderEngine = self.init(is_game)

    def _get_coordinates(self, tile_pos: tuple):
        x, y = tile_pos
        return (x + 0.5) * self.sq_width, (y + 0.5) * self.sq_width

    def init_enmies(self, count: int, speed: int):
        enemies = []
        for i in range(count):
            enemy_pos = self.pathfinderapp.new_follower(
                ignore=[self.player.position] + list(map(lambda p: p.position, enemies)))
            if enemy_pos:
                enemies.append(Enemy(enemy_pos, speed=speed))
        return enemies

    def keymapHandler(self):
        def keymap(event):
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player_tile = self.pathfinderapp.move_target(
                    ignore=[self.player.position] + list(map(lambda e: e.position, self.enemies)))
                self.player.position = player_tile
                self.player.coordinate = self._get_coordinates(player_tile)
                self.player.directions = [Direction.NONE, Direction.NONE, Direction.NONE, Direction.NONE]

            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    if event.type == pygame.KEYDOWN:
                        self.player.directions[0] = Direction.UP
                    elif event.type == pygame.KEYUP:
                        self.player.directions[0] = Direction.NONE
                if event.key == pygame.K_RIGHT:
                    if event.type == pygame.KEYDOWN:
                        self.player.directions[1] = Direction.RIGHT
                    elif event.type == pygame.KEYUP:
                        self.player.directions[1] = Direction.NONE
                if event.key == pygame.K_DOWN:
                    if event.type == pygame.KEYDOWN:
                        self.player.directions[2] = Direction.DOWN
                    elif event.type == pygame.KEYUP:
                        self.player.directions[2] = Direction.NONE
                if event.key == pygame.K_LEFT:
                    if event.type == pygame.KEYDOWN:
                        self.player.directions[3] = Direction.LEFT
                    elif event.type == pygame.KEYUP:
                        self.player.directions[3] = Direction.NONE

        return keymap

    def updateHandler(self):
        def update():
            if not self.is_game:
                if self.iterations_left:
                    self.cave.smoothing(1)
                    self.iterations_left -= 1
                    return
                if not self.cave_rendered:
                    self.cave.detectRooms()
                    self.cave.connectRooms()

                return

            new_position = self.player.position
            pos = None
            for direction in self.player.directions:
                pos = new_position[0] + direction.value[0], new_position[1] + direction.value[1]
                pos = self.pathfinderapp.move_target(position=pos)
                if not pos:
                    pos = new_position
                else:
                    new_position = pos

            if pos:
                self.player.position = pos

            for i in range(len(self.enemies)):
                next_step = self.pathfinderapp.get_next_step(self.enemies[i].position)
                if next_step is not self.player.position:
                    self.enemies[i].position = next_step

        return update

    def _rendertext(self, display, text: str, position: tuple):
        font = pygame.font.SysFont(self.font_type, self.font_size)
        textsurface = font.render(text, False, self.font_color)
        display.blit(textsurface, position)

    def renderHandler(self):
        def render(display):
            triangles, tags = render_data(self.cave.layout.grid, self.sq_width)
            # display.fill(self.room_color)
            pygame.draw.rect(display, self.room_color, rect=[0, 0, self.screen_size[0], self.screen_size[1]])
            pygame.draw.rect(display, tuple(map(lambda x: (x - 20) % 255, self.wall_color)),
                             [0, (self.size[1]) * self.sq_width, self.screen_size[0], 200])

            if self.is_game and self.player:
                color = (0, 255, 0)
                x, y = self.player.position
                pygame.draw.circle(display, color,
                                   ((x + 0.5) * self.sq_width, (y + 0.5) * self.sq_width), self.sq_width / 2, width=0)
            if self.is_game and self.enemies:
                color = (255, 0, 0)
                for enemy in self.enemies:
                    x, y = enemy.position
                    pygame.draw.circle(display, color,
                                       ((x + 0.5) * self.sq_width, (y + 0.5) * self.sq_width), self.sq_width / 2,
                                       width=0)

            for i in range(len(triangles)):
                tri = triangles[i]
                tag = tags[i]
                pygame.draw.polygon(display, self.wall_color, list(tri), width=0)

            render_text = " | Interation Left: " + str(self.iterations_left)
            render_text += " | Rooms connected: " + str(self.cave_rendered)

            text = "World size: " + str(self.size) + ("" if self.is_game else render_text)
            self._rendertext(display, text, (20, (self.size[1] + 2) * self.sq_width))

            pygame.display.flip()

        return render

    def init(self, is_game: bool = True):
        return RenderEngine(list((1200, 600)), self.updateHandler(),
                            self.renderHandler(), self.keymapHandler(), self.fps_cap, is_game)

    def start(self):
        self.renderEngine.start()

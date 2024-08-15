import pygame


# Generalized render engine wrapper
class RenderEngine:
    def __init__(self, dimensions: list, update, render, keymap, frame_rate: int = 10, is_game: bool = True):
        self.dimensions = dimensions

        pygame.init()
        self.display = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
        pygame.display.set_caption("Caves")
        # pygame.display.toggle_fullscreen()

        self.keymap = keymap
        self.render = render
        self.update = update
        self.frame_rate = frame_rate

        self.clock = pygame.time.Clock()
        self.is_game =  is_game

    def render_once(self):
        self.clock.tick(self.frame_rate)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            if self.keymap and not self.is_game:
                self.keymap(event)

        if self.render:
            self.render(self.display)
        if self.update:
            self.update()

    def start(self):
        running = True

        while running:
            self.render_once()

        pygame.quit()

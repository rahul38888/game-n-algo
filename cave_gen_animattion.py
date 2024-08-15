from app import App
from src.datahandler.layout import Layout
from render.engine import RenderEngine
from src.scripts.algos.caveprocedural import CaveProcedural

size = (120, 59)
sq_width = 13.66
iterations = 20
fps_cap = 5

if __name__ == '__main__':
    app = App(size=size, sq_width=sq_width, iterations=iterations, fps_cap=2, is_game=False)
    app.start()

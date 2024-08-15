

from src.datahandler.layout import Layout
from src.scripts.algos.pathfinder import PathFinder


# Pathfinder application uril to handle layout and pathfinder util
class PathFindingApp:
    def __init__(self, layout: Layout, pathfinder: PathFinder):
        self.layout = layout
        self.pathfinder = pathfinder

    def recalculate(self, target: tuple):
        if target is None:
            return

        self.pathfinder.recalculate(target[0], target[1], self.layout)

    def move_target(self, position: tuple = None, ignore: list = []):
        target = self.layout.move_target(position=position)
        if target:
            self.recalculate(target)

        return target

    def new_follower(self, ignore: list = []):
        return self.layout.new_source(ignore=ignore)

    def get_next_step(self, position: tuple) -> tuple:
        return self.pathfinder.prev[position[1]][position[0]]

    def get_path(self, target: tuple, source: tuple) -> list:
        path = []
        cur = source
        while True:
            path.append(cur)
            if cur == target:
                break
            if not cur:
                return []

            cur = self.pathfinder.prev[cur[1]][cur[0]]

        return path


if __name__ == '__main__':
    a = 10
    l = Layout((a, a))
    pf = PathFinder()

    p_app = PathFindingApp(layout=l, pathfinder=pf)

    target = (a-2, a - 1)
    source = (0, 0)
    p_app.move_target(position=target)

    print(p_app.get_path(source=source, target=target))
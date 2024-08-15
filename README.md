# Caves
#### Using [pygame](https://www.pygame.org) as render engine
* Procedural cave generation 
* Dijkstra's Algorithm to detect the shortest path 
* Flood fill algorithm to detect regions (rooms)
* Line algorithm me connect isolated regions

## Snapshot
<img src="https://github.com/rahul38888/game-n-algo/blob/main/media/terminal_caves.jpg?raw=true" alt="drawing" width="500"/>

New cave is generated every time the app is initialized. Following animation shows how noise transforms into cave

<img src="https://github.com/rahul38888/game-n-algo/blob/main/media/CaveGen.gif?raw=true" alt="drawing" width="500"/>

The Red keep following the Green around using Dijkstra's Algorithm (for Green) until it caches it

<img src="https://github.com/rahul38888/game-n-algo/blob/main/media/Cave_the_game.gif?raw=true" alt="drawing" width="500"/>

## Controls
| Key        | Function                               |
|------------|----------------------------------------|
| Space      | New random position for Green (target) |
| Arrow Keys | To move Green around the caves         |
| Esc        | Exist                                  |

### Enjoy!
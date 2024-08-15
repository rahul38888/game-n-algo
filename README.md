# Caves
#### Using [pygame](https://www.pygame.org) as render engine
* Procedural cave generation 
* Dijkstra's Algorithm to detect the shortest path 
* Flood fill algorithm to detect regions (rooms)
* Line algorithm me connect isolated regions

## Snapshot
![welcome.png](https://github.com/rahul38888/game-n-algo/blob/main/media/terminal_caves.jpg?raw=true)

New cave is generated every time the app is initialized. Following animation shows how noise transforms into cave
![animation.png](https://github.com/rahul38888/game-n-algo/blob/main/media/CaveGen.gif?raw=true)

The Red keep following the Green around using Dijkstra's Algorithm (for Green) until it caches it

## Controls
| Key        | Function                               |
|------------|----------------------------------------|
| Enter      | New random position for Green (target) |
| Arrow Keys | To move Green around the caves         |
| Esc        | Exist                                  |

### Enjoy!
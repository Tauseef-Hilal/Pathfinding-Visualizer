# Pathfinding Visualizer
A pathfinding visualizer made in Python and Pygame. This project aims to provide a fun and interactive way to learn about popular pathfinding algorithms such as Dijkstra's, A* and other [supported algorithms](#supported-algorithms).

https://user-images.githubusercontent.com/67793598/218127466-38274684-5eb6-44e9-b842-29720a26dd54.mp4

## Screenshots
<table border='0px'>
    <tr>
        <td>
            <img src='screenshots/AStar.png?raw=true' 
                 alt="A* Search"
                 width='360'>
        </td>
        <td>
            <img src='screenshots/Dijkstras.png?raw=true' 
                 alt="Dijkstra's Search"
                 width='360'>
        </td>
    </tr>
    <tr>
        <td>
            <img src='screenshots/GreedyBFS.png?raw=true' 
                 alt="Greedy Best-First Search"
                 width='360'>
        </td>
        <td>
            <img src='screenshots/BFS.png?raw=true' 
                 alt="Breadth-First Search"
                 width='360'>
        </td>
    </tr>
    <tr>
        <td>
            <img src='screenshots/DFS.png?raw=true' 
                 alt="Depth-First Search"
                 width='360'>
        </td>
        <td>
            <img src='screenshots/Results.png?raw=true' 
                 alt="Results"
                 width='360'>
        </td>
    </tr>
</table>

## Features
* Visualizes popular pathfinding algorithms such as Dijkstra's and A*.
* Visualizes popular maze generation algorithms like Recursive division and Prim's algorithm.
* Feature to run all algorithms b2b to compare their performance.
* Step-by-step animation of the search process, allowing you to see how the algorithms work.
* Option to place obstacles on the grid to create custom maps.
* Selectable starting and ending points on the grid.
* Configurable speed of the animation. 
* Configurable grid size
* Clean and intuitive user interface.

## Supported Algorithms
The following pathfinding algorithms are currently supported in this visualizer:

1. Depth First Search (DFS): A traversal-based algorithm that goes as far as possible along each branch before backtracking. Not commonly used for pathfinding.
2. Breadth First Search (BFS): A traversal-based algorithm that explores all neighbors of a node before moving on to the next level. Guaranteed to find the shortest path in unweighted graphs.
3. Greedy Best First Search: A heuristic search algorithm that prioritizes visiting nodes closest to the goal. Not guaranteed to find the shortest path, but often faster.
4. A* Search: A heuristic search algorithm that combines the strengths of BFS and greedy best first search. Efficient for many types of graphs.
5. Dijkstra's Search: A shortest path algorithm that uses a priority queue to prioritize visiting nodes with the smallest known cost. Guaranteed to find the shortest path in weighted graphs.

Each algorithm uses a different approach to finding the shortest path between two points on a graph. Choose the one that best fits your use case and watch it in action.

## Requirements
* Python 3.10 and above: You can download the latest version of Python from the official website (https://www.python.org/downloads/).
* Pygame: You can install Pygame by running 'pip install pygame' in your terminal.

## Usage
- Download the project repository to your local machine. 
- Navigate to the project directory.
- Run `python3 run.pyw` if on Linux or Mac
- Run `python run.pyw` if on Windows

## Command Line Arguments
1. `--cell-size`
Usage: `python run.pyw --cell-size:<int>`

## Contributing
This project is open to contributions, bug reports, and suggestions. If you've found a bug or have a suggestion, please open an issue.

# License
This project is licensed under the MIT License.

Enjoy visualizing pathfinding algorithms!

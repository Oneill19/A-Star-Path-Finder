# A Star Path Finder
##### A* Path Finder algorithm visualization made in python.

A* algorithm is a BFS algorithm to find the optimal path from the start node to the goal node.
This algorithm is an expansion of the Dijkstra algorithm.
The algorithm uses a priority queue to choose the lowest f cost from all the node of every neighbour to continue the search.

The f cost is calculated by: ```f(n) = g(n) + h(n)```
- g(n) is the distance between the start node and n.
- h(n) is the heuristic function that calculates the distance between n and the goal node.

The code use the pygame library to visualize the steps of the algorithm and show the opening and closing node process until finding the goal node.
After finiding the goal node, the program draw the optimal path between the start node and the goal node.

##### Instructions:
- The first left click will set the start node.
- The second left click will set the goal node.
- Every other left click after setting the start and goal nodes will be a wall.
- Right click on a node to reset it back to white.
- If you reset a start or goal node, the next left click will set the start or goal node.
- Press SPACE to start the algorithm.
- Press BACKSPACE to reset the grid.
- If the algorithm didn't find any path, the user can edit the grid without reset it.

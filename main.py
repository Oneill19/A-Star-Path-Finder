# A* path finder algorithm visualizations
import pygame
import sys
from queue import PriorityQueue

pygame.init()
pygame.display.set_caption("A* Path Finder Algorithm")


# =====================================================================================================================
# constants
# =====================================================================================================================


WIN_SIZE = 1000
GRID_SIZE = 50
BLACK = (47, 45, 46)      # walls and grid color
WHITE = (255, 255, 255)   # initialized node color
DARK_BLUE = (46, 64, 87)  # closed node color
BLUE = (4, 139, 168)      # open node color
CRIMSON = (220, 20, 60)   # start node color
ORANGE = (241, 143, 1)    # goal node color
GOLD = (255, 215, 0)      # path node color
WIN = pygame.display.set_mode((WIN_SIZE, WIN_SIZE))


# =====================================================================================================================
# upgraded priority queue
# =====================================================================================================================


# data structure that support add, empty, get, and in commands
class UPQ:
    # constructor
    def __init__(self, start_node):
        self.open_queue = PriorityQueue()
        self.open_set = {start_node}


    # add a node to the upgraded priority queue
    def add(self, f_score, count, node):
        self.open_queue.put((f_score, count, node))
        self.open_set.add(node)


    # check if the queue is empty
    def empty(self):
        return self.open_queue.empty()


    # return the first node in the queue
    def get(self):
        return_node = self.open_queue.get()[2]
        self.open_set.remove(return_node)
        return return_node


    # implement the in command
    def __contains__(self, node):
        return node in self.open_set


# =====================================================================================================================
# node class
# =====================================================================================================================


# class to represent every node on the grid
class Node:
    # constructor
    def __init__(self, row, col, size):
        self.row = row
        self.col = col
        self.x = row * size
        self.y = col * size
        self.f_score = float("inf")  # initialize the value of the f score
        self.g_score = float("inf")  # initialize the value of the g score
        self.size = size
        self.color = WHITE
        self.neighbours = []


    # return the position of the node in the grid
    def get_pos(self):
        return self.row, self.col


    # return the f score of the node
    def get_f_score(self):
        return self.f_score


    # return the g score of the node
    def get_g_score(self):
        return self.g_score


    # return the neighbours of the node
    def get_neighbours(self):
        return self.neighbours


    # set the f score of the node
    def set_f_score(self, f_score):
        self.f_score = f_score


    # set the g score of the node
    def set_g_score(self, g_score):
        self.g_score = g_score


    # set the color of the node
    def set_color(self, color):
        self.color = color


    # return true if the node is a wall
    def is_wall(self):
        return self.color == BLACK


    # reset the neighbours list
    def reset_neighbours(self):
        self.neighbours = []


    # draw the node on the window
    def draw(self):
        pygame.draw.rect(WIN, self.color, (self.x, self.y, self.size, self.size))


    # check if two variables are in the range
    @staticmethod
    def check_range(i, j):
        return i >= 0 and i < GRID_SIZE and j >= 0 and j < GRID_SIZE


    # create the neighbours list
    def create_neighbours(self, grid):
        self.neighbours = []
        if self.check_range(self.row + 1, self.col) and not grid[self.row + 1][self.col].is_wall():  # upper node
            self.neighbours.append(grid[self.row + 1][self.col])
        if self.check_range(self.row - 1, self.col) and not grid[self.row - 1][self.col].is_wall():  # down node
            self.neighbours.append(grid[self.row - 1][self.col])
        if self.check_range(self.row, self.col + 1) and not grid[self.row][self.col + 1].is_wall():  # right node
            self.neighbours.append(grid[self.row][self.col + 1])
        if self.check_range(self.row, self.col - 1) and not grid[self.row][self.col - 1].is_wall():  #left node
            self.neighbours.append(grid[self.row][self.col - 1])


    # equality method for node
    def __eq__(self, other):
        if other is None:
            return False
        return self.row == other.row and self.col == other.col


    # hash method for node to use in a set
    def __hash__(self):
        if self.row > self.col:
            return 4 * self.row * self.row - 3 * self.row + self.col + 1
        return 4 * self.col * self.col - self.col - self.row + 1


# =====================================================================================================================
# grid class
# =====================================================================================================================


# class the represent a matrix of nodes
class Grid:
    # constructor
    def __init__(self, size):
        self.start = None
        self.goal = None
        self.size = size  # size of the grid
        self.grid = self.create_grid()  # create a matrix of size*size nodes


    # return true if there is a start node
    def has_start(self):
        return self.start is not None


    # return true if there is a goal node
    def has_goal(self):
        return self.goal is not None


    # return the start node
    def get_start(self):
        return self.start


    # return the goal node
    def get_goal(self):
        return self.goal


    # return the grid
    def get_grid(self):
        return self.grid


    # set the start node
    def set_start(self, start):
        self.start = start
        self.start.set_color(CRIMSON)


    # set the goal node
    def set_goal(self, goal):
        self.goal = goal
        self.goal.set_color(ORANGE)


    # set a node to be a wall
    @staticmethod
    def set_wall(node):
        node.set_color(BLACK)


    # set a node to be open
    def set_open(self, node):
        if node != self.start and node != self.goal:
            node.set_color(BLUE)


    # set a node to be closed
    def set_closed(self, node):
        if node != self.start and node != self.goal:
            node.set_color(DARK_BLUE)


    # reset a node
    def reset_node(self, node):
        if node == self.start:
            self.start = None
        if node == self.goal:
            self.goal = None
        node.set_f_score(float("inf"))  # initialize the f score
        node.set_g_score(float("inf"))  # initialize the g score
        node.reset_neighbours()  # initialize the neighbours
        node.set_color(WHITE)


    # create the grid
    def create_grid(self):
        grid = []
        node_size = WIN_SIZE // self.size
        for i in range(self.size):
            grid.append([])
            for j in range(self.size):
                node = Node(i, j, node_size)
                grid[i].append(node)
        return grid


    # reset the grid
    def reset_grid(self):
        for row in self.grid:
            for node in row:
                self.reset_node(node)


    # draw the grid on the window
    def draw(self):
        for row in self.grid:   # draw the nodes
            for node in row:
                node.draw()
        node_size = WIN_SIZE // self.size
        for i in range(self.size):  # draw the grid lines
            pygame.draw.line(WIN, BLACK, (0, i * node_size), (WIN_SIZE, i * node_size))
            for j in range(self.size):
                pygame.draw.line(WIN, BLACK, (j * node_size, 0), (j * node_size, WIN_SIZE))
        pygame.display.update()


    # get the node where the user clicked with the mouse
    def get_clicked_node(self, pos):
        node_size = WIN_SIZE // self.size
        y, x = pos  # unpack the position of the mouse click
        row = y // node_size  # get the row by get the floor of dividing the y of the position of the mouse by the node size
        col = x // node_size  # get the col by get the floor of dividing the x of the position of the mouse by the node size
        return self.grid[row][col]


# =====================================================================================================================
# functions
# =====================================================================================================================


# heuristic function for calculating the f score
def heuristic(first, second):
    first_x, first_y = first
    second_x, second_y = second
    return abs(first_x - second_x) + abs(first_y - second_y)


# draw the path
def reconstruct_path(came_from,node, grid):
    while node in came_from:
        node = came_from[node]
        if node != grid.get_start() and node != grid.get_goal():
            node.set_color(GOLD)
        grid.draw()


# a star algorithm
def a_star(grid):
    count = 0  # variable for the priority queue, if couple nodes have the same f score
    start_node = grid.get_start()
    goal_node = grid.get_goal() 
    open_nodes = UPQ(start_node)  # priority queue to get the lowest f score node first
    came_from = {}  # dictionary to show the node and his parent
    start_node.set_g_score(0)  # set the start node g score
    start_node.set_f_score(heuristic(start_node.get_pos(), goal_node.get_pos()))  # set the start node f score
    open_nodes.add(start_node.get_f_score(), count, start_node)  # add the start node to the queue
    while not open_nodes.empty():
        for event in pygame.event.get():  # option to quit the program during a session
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        current_node = open_nodes.get()  # get the first node from the priority queue
        current_node.create_neighbours(grid.get_grid())  # create the neighbours of this node
        if current_node == goal_node:  # if the node is the goal node draw the path and return true
            reconstruct_path(came_from, goal_node, grid)
            return True
        for neighbour in current_node.get_neighbours():  # for every neighbour
            tentative_g_score = current_node.get_g_score() + 1  # every neighbour g score is bigger by one from the current node g score
            if tentative_g_score < neighbour.get_g_score():  # if the tentative g score smaller the the neighbour current g score
                came_from[neighbour] = current_node  # update the parent of the neighbour node
                neighbour.set_g_score(tentative_g_score)  # set the g score of the neighbour
                neighbour.set_f_score(tentative_g_score + heuristic(neighbour.get_pos(), goal_node.get_pos()))  # set the f score of the neigbour
                if neighbour not in open_nodes:  # if the neigbour not opened yet
                    count += 1
                    open_nodes.add(neighbour.get_f_score(), count, neighbour)  # add it to the queue
                    grid.set_open(neighbour)  # set the neighbour color to open
        grid.draw()  # update the grid on the window
        if current_node != start_node:  # after checking the neighbours close the current node and move to the next lowest f score node
            grid.set_closed(current_node)
    return False  # if not found return false


# =====================================================================================================================
# main function
# =====================================================================================================================


def main():
    run = True
    started = True
    grid = Grid(GRID_SIZE)  # initialize grid object
    while run:
        grid.draw()  # draw the grid
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # exit the program
                run = False
            if pygame.mouse.get_pressed()[0] and started:  # if the session started and the user clicked on the left button
                pos = pygame.mouse.get_pos()
                node = grid.get_clicked_node(pos)  # get the node the user clicked on
                if not grid.has_start() and node != grid.get_goal():  # if there is no start node and the node is not the goal node
                    grid.set_start(node)  # set the node to be the start
                elif not grid.has_goal() and node != grid.get_start():  # if there is no goal node and the node is node the start node
                    grid.set_goal(node)  # set the node to be the goal
                elif node != grid.get_start() and node != grid.get_goal():  # if the node is not the start and not the goal
                    grid.set_wall(node)  # set the node to be a wall
            elif pygame.mouse.get_pressed()[2] and started:  # if the session started and the user clicked on the right button
                pos = pygame.mouse.get_pos()
                node = grid.get_clicked_node(pos)  # get the node the user clicked on
                grid.reset_node(node)  # reset the node
            elif event.type == pygame.KEYDOWN:  # if the user pressed a key on the keyboard
                if event.key == pygame.K_SPACE and grid.has_start() and grid.has_goal():  # if pressed SPACE and there is start and goal nodes
                    if a_star(grid):  # start the algorithm
                        started = False  # if there is a path, the user can start a new session, else he can fix the nodes he want and redo the algorithm
                    else:
                        for row in grid.get_grid():  # reset the f score and g score
                            for node in row:
                                node.set_g_score(float("inf"))
                                node.set_f_score(float("inf"))
                if event.key == pygame.K_BACKSPACE:  # if pressed BACKSPACE reset the grid and start a new session
                    grid.reset_grid()
                    started = True
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()

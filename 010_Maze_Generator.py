from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.graphics import Line, Rectangle, Color
from kivy.clock import Clock
import random

'''
    ---------------------------------------------
    Coding Challenge #10: Maze Generator
    ---------------------------------------------

    This is a python version of the coding challenge from Daniel Shiffman on The Coding Train

    Original coding challenge: 
        https://www.youtube.com/watch?v=jxGS3fKPKJA&index=6&list=PLRqwX-V7Uu6ZiZxtDDRCi6uhfTH4FilpH

    Modifications:
        - I added a green color to cells which are still in the stack
        - I used different methods to calculate the indices of the neighbors of each cell
'''

CELL_SIZE = 100     # size of the side of each cell
Window.size = (800, 800)
COLS = Window.size[0] // CELL_SIZE  # number of columns of the grid
ROWS = Window.size[1] // CELL_SIZE  # number of rows of the grid
CELL_STROKE = 1

class MazeGeneratorApp(App):
    def build(self):
        return MazeGenerator()

'''
    Class that displays the application
'''
class MazeGenerator(BoxLayout):
    def __init__(self, **kwargs):
        super(MazeGenerator, self).__init__(**kwargs)
        # Create the cells and add it to the grid
        self.create_cells()
        # Index of the current visited cell
        self.current_index = 0
        # number of visited cells
        self.visited_cells = 0
        # controls the spped of the maze (the smaller the time, the faster the maze is generated)
        self.TIME = 0.5
        # Stack that will contain the visited cells
        self.stack = []
        # Stacrt the clock and at each iteration, generate and draw the maze
        Clock.schedule_interval(self.generate_and_draw, self.TIME)

    '''
        Loops through the grid and creates the cells
    '''
    def create_cells(self):
        self.cells = []
        for row in range(ROWS):
            for col in range(COLS):
                self.cells.append(Cell(row, col))

    '''
        Generates and draws the maze at each itertion
    '''
    def generate_and_draw(self, time):
        self.generate_maze()
        self.draw_cells()

    '''
        Displays each cell with its updated properties (walls, isVisited, etc)
    '''
    def draw_cells(self):
        self.canvas.before.clear()
        with self.canvas.before:
            cell_index = 0
            for cell in self.cells:
                # Display the walls
                lines = cell.display()
                for line in lines:
                    line
                # Display the cells in the stack in green
                if cell_index in self.stack:
                    Color(0.1, 0.7, 0.2, 1)
                    Rectangle(pos=cell.get_cell_position(), size=(CELL_SIZE, CELL_SIZE))
                    Color(1, 1, 1, 1)
                # Display the cells not to be visited again in purple
                elif cell.visited:
                    Color(0.5, 0.1, 0.8, 1)
                    Rectangle(pos = cell.get_cell_position(), size = (CELL_SIZE, CELL_SIZE))
                    Color(1, 1, 1, 1)
                cell_index = cell_index + 1
            # Display the current visited cell
            Color(0.1, 0.1, 0.9, 1)
            Rectangle(pos = self.cells[self.current_index].get_cell_position(), size = (CELL_SIZE, CELL_SIZE))
            Color(1, 1, 1, 1)

    '''
        Implementation of the maze generator
    '''
    def generate_maze(self):
        self.cells[self.current_index].visited = True
        # Get a random unvisited neighbor
        next_index = self.get_unvisited_neighbor_index(self.current_index)
        # If a neighbor is found, remove the walls between it and the current cell, then
        #   add the current cell to the stack
        if next_index != -1:
            self.stack.append(self.current_index)
            self.remove_wall(self.current_index, next_index)
            self.current_index = next_index
        else:
            # If no neighbor is found, move back to a cell in the stack and look for its neighbors
            #   in the next iteration
            if len(self.stack) > 0:
                self.current_index = self.stack.pop()

    '''
        Removes the walls between two adjacent cells
    '''
    def remove_wall(self, i, j):
        # if cell j is at the top of cell i
        if j == i + 1:
            # remove top wall of cell i
            self.cells[i].walls['top'] = False
            # remove bottom wall of cell j
            self.cells[j].walls['bottom'] = False

        # if cell j is at the right of cell i
        if j == i + ROWS:
            # remove right wall of i
            self.cells[i].walls['right'] = False
            # remove left wall of j
            self.cells[j].walls['left'] = False

        # if cell j is at the bottom of cell i
        if j == i - 1:
            # remove bottom wall of cell i
            self.cells[i].walls['bottom'] = False
            # remove top wall of cell j
            self.cells[i].walls['top'] = False

        # if cell j is at the left of cell i
        if j == i - ROWS:
            # remove left wall of cell i
            self.cells[i].walls['left'] = False
            # remove right wall of cell j
            self.cells[j].walls['right'] = False

    '''
        Finds a random unvisited neighbor to the current cell and returns its index, or -1
        if the cell has not visited neighbor
    '''
    def get_unvisited_neighbor_index(self, i):
        neighbors_indices = []
        # top
        index = i + 1   # index of the cell at the top of cell i
        # the cells at the top row have the indices rows - 1, 2 * rows - 1, 3 * rows - 1, ...
        #   so in order for a cell to have a top neighbor, it shouldn't be on the top,
        #   hence (i + 1) % rows != 0
        if (i + 1) % ROWS != 0 and not self.cells[index].visited:
            neighbors_indices.append(index)

        # right
        index = i + ROWS    # index of the cell at the right of cell i
        # cols * rows - 1 is the index of the last cell
        #   thus, (cols * rows - 1) - (rows - 1) is the index of the first cell of the last upper row
        #   simplified we get (cols * rows - 1) - (cols - 1) = rows * (cols - 1)
        #   so in order for cell i to have a right neighbor, we should have i < rows * (cols - 1)
        if i < ROWS * (COLS - 1) and  not self.cells[index].visited:
            neighbors_indices.append(index)

        # bottom
        index = i - 1   # index of the cell at the bottom of i
        # the cells at the bottom row have the indices 0, rows, 2 * rows, ...
        #   so in order for a cell to have a bottom neighbor, i shouldn't be a multiple
        #   of rows, hence i % rows != 0
        if i % ROWS != 0 and not self.cells[index].visited:
            neighbors_indices.append(index)

        # left
        index = i - ROWS    # index of the cell at the left of cell i
        # the cells of the left column have indices from 0 to rows - 1
        #   so in order for a cell to have a bottom neighbor, it shouldn't be on that left column,
        #   hence i >= rows
        if i >= ROWS and not self.cells[index].visited:
            neighbors_indices.append(index)

        if len(neighbors_indices):
            r = random.randint(0, len(neighbors_indices) - 1)
            return neighbors_indices[r]
        else:
            return -1


'''
    Represents a Cell and the operations associated with it (coordinates, walls, isvisited)
'''
class Cell:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.walls = {'top': True, 'right': True,
                      'bottom': True, 'left': True}
        self.visited = False

    def display(self):
        # x4, y4 --------------------- x3, y3           x2 = x1 + CELL_SIZE, y2 = y1
        #   |                            |
        #   |                            |              x3 = x1 + CELL_SIZE, y3 = y1 + CELL_SIZE
        #   |                            |
        #   |                            |              x4 = x1            , y4 = y1 + CELL_SIZE
        #   |                            |
        #   |                            |
        #   |                            |
        # x1, y1 --------------------- x2, y2

        x1, y1 = self.i * CELL_SIZE, self.j * CELL_SIZE
        x2, y2 = x1 + CELL_SIZE, y1
        x3, y3 = x1 + CELL_SIZE, y1 + CELL_SIZE
        x4, y4 = x1, y1 + CELL_SIZE

        lines = []
        if self.walls['top']:
            lines.append(Line(points = [x3, y3, x4, y4], width = CELL_STROKE))
        if self.walls['right']:
            lines.append(Line(points = [x2, y2, x3, y3], width = CELL_STROKE))
        if self.walls['bottom']:
            lines.append(Line(points = [x1, y1, x2, y2], width = CELL_STROKE))
        if self.walls['left']:
            lines.append(Line(points = [x1, y1, x4, y4], width = CELL_STROKE))
        return lines

    '''
        Returns the coordinates of the bottom left corner of the cell
    '''
    def get_cell_position(self):
        return [self.i * CELL_SIZE, self.j * CELL_SIZE]


MazeGeneratorApp().run()

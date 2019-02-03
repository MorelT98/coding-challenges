from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.graphics import Ellipse, Color
from kivy.clock import Clock
import random
import math

'''
    ---------------------------------------------
    Coding Challenge #6: Mitosis
    ---------------------------------------------

    This is a python version of the coding challenge from Daniel Shiffman on The Coding Train

    Original coding challenge: 
        https://www.youtube.com/watch?v=jxGS3fKPKJA&index=6&list=PLRqwX-V7Uu6ZiZxtDDRCi6uhfTH4FilpH

    Modifications:
        
'''

'''
    Calculates the euclidian distance between two points (x1, y1) and (x2, y2)
'''
def distance(x1, y1, x2, y2):
    return math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))

class MitosisApp(App):
    def build(self):
        return Mitosis()

'''
    Class displaying the whole application
'''
class Mitosis(BoxLayout):
    TIME = 0.1  # Update time (The smaller, the faster the cells vibrate)
    CELL_SIZE = 50  # Diameter of the initial cell

    def __init__(self, **kwargs):
        super(Mitosis, self).__init__(**kwargs)
        Window.size = (700, 700)
        self.canvas.before.clear()
        self.cells = []

        # Create two cells to start
        self.cells.append(Cell(Window.size, self.CELL_SIZE))
        self.cells.append(Cell(Window.size, self.CELL_SIZE))

        # Start the clock
        Clock.schedule_interval(self.update_cell, self.TIME)

    '''
        This method vibrates the cells
    '''
    def update_cell(self, time):
        self.canvas.before.clear()
        with self.canvas.before:
            for cell in self.cells:
                # Vibrate each cell
                cell.move()
                Color(*cell.rgb, 0.39)
                cell.show()

    '''
        This method splits each clicked cell into two cells of smaller size
    '''
    def on_touch_down(self, touch):
        for i in range(len(self.cells) - 1, -1, -1):
            if self.cells[i].isClicked(touch.pos[0], touch.pos[1]):
                # Split the clicked cell into cell_A and cell_B, then erase the actual cell
                cell_A, cell_B = self.cells[i].split()
                self.cells.append(cell_A)
                self.cells.append(cell_B)
                self.cells.remove(self.cells[i])

'''
    Class representing a cell object and the behaviours associated with it
        (move, check whether or not the cell is clicked, etc)
'''
class Cell:
    def __init__(self, window_size, r):
        self.window_size = window_size
        # Create the cell at a random location
        self.x = random.uniform(r, window_size[0] - r)
        self.y = random.uniform(r, window_size[1] - r)
        # random color between pink and purple
        self.rgb = (random.uniform(0.39, 1), 0, random.uniform(0.39, 1))
        self.r = r

    # Move the cell by a small vector (dx, dy)
    def move(self):
        d = min(self.x, self.y) / 100
        dx = random.uniform(-d, d)
        dy = random.uniform(-d, d)
        self.x += dx
        self.y += dy

    # Split the cell into two small cells
    def split(self):
        cell_A = Cell(self.window_size, self.r)
        cell_A.x = self.x + self.r / 2
        cell_A.y = self.y
        cell_A.rgb = self.rgb
        cell_A.r = self.r * 0.8

        cell_B = Cell(self.window_size, self.r)
        cell_B.x = self.x - self.r / 2
        cell_B.y = self.y
        cell_B.rgb = self.rgb
        cell_B.r = self.r * 0.8

        return cell_A, cell_B

    # Display the cell
    def show(self):
        return Ellipse(pos = (self.x, self.y), size = (self.r, self.r))

    # Given the nouse location, checks whether or not the cell was clicked
    def isClicked(self, mouse_x, mouse_y):
        return distance(self.x, self.y, mouse_x, mouse_y) < self.r


MitosisApp().run()
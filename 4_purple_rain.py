from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Line
from kivy.core.window import Window
from kivy.clock import Clock
import random

'''
    ---------------------------------------------
    Coding Challenge #4: Purple Rain:
    ---------------------------------------------

    This is a python version of the coding challenge from Daniel Shiffman on The Coding Train

    Original coding challenge: 
        https://www.youtube.com/watch?v=KkyIDI6rQJI&index=4&list=PLRqwX-V7Uu6ZiZxtDDRCi6uhfTH4FilpH

    Modifications:
        I added the splashes at the bottom
'''

'''
    Maps the number x from the range [x1, x2] to a corresponding number in the range [y1, y2]
'''
def map(x, x1, x2, y1, y2):
    return y1 + x * (y2 - y1) / (x2 - x1)

'''
    Class that displays everything
'''
class PurpleRain(BoxLayout):

    def __init__(self):
        super(PurpleRain, self).__init__()
        Window.size = (640, 360)
        Window.clearcolor = (0.91, 0.91, 0.98, 1)

        # create the drops
        self.drops = [Drop(*Window.size) for i in range(100)]

        # start the clock
        Clock.schedule_interval(self.update_drops, 0.05)

    '''
        Updates the drops locations and displays them
    '''
    def update_drops(self, time):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.54, 0.17, 0.89)
            for drop in self.drops:
                drop.fall()
                drop.show()

'''
    This class represents a single drop, and provides behaviours such 
    as falling
'''
class Drop:
    def __init__(self, width, height):
        # get the window's dimensions
        self.window_width = width
        self.window_height = height

        # pick a random location for the drop
        self.x = random.randint(0, width)
        self.y = random.randint(height, height + 500)  # the drop will start out of the screen
        self.z = random.randint(0, 20)  # represents the depth (in an attempt to make the simulation 3D)

        # The closer to the screen, the higher the gravity, the faster the drop is, the
        #   longer and thicker it is as well
        self.gravity = map(self.z, 0, 20, 0, 0.5)
        self.yspeed = map(self.z, 0, 20, 4, 10)
        self.length = map(self.z, 0, 20, 10, 20)
        self.thickness = map(self.z, 0, 20, 1, 1.5)

    '''
        Moves the drop down, and relocates it if the drop hits the bottom
    '''
    def fall(self):
        # Move the drop down faster with gravity
        self.y -= self.yspeed
        self.yspeed += self.gravity

        # If the drop hits the bottom, create the splash, pop it, then relocate the drop
        if self.y - self.length < 0:
            # relocating
            self.y = random.randint(self.window_height, self.window_height + 100)
            self.z = random.randint(0, 20)

            # creating and poping splash
            splash = Splash(self.x, 0, self.length)
            for splashline in splash.get_splashlines():
                Line(points = splashline, width = self.thickness)
            self.yspeed = map(self.z, 0, 20, 4, 10)

    '''
        Displays the drop
    '''
    def show(self):
        return Line(points = (self.x, self.y, self.x, self.y - self.length), width = self.thickness)

'''
    Splash representation (two lines in symmetric and diagonal directions)
'''
class Splash:
    def __init__(self, x, y, drop_length):
        # location of the drop
        self.x = x
        self.y = y

        # keeps track of whether or not the splash ocuured already, in which case don't splash again
        self.splashed = False

        # the splash lines length are proportional to the drop length, but smaller
        self.length = drop_length / 15

        # make the splash lines inclined and symmetric
        self.splashlines = [
            (x + 5, y + 10, x + 5 + self.length,  y + 10 + self.length),
            (x - 5, y + 10, x - 5 - self.length, y + 10 + self.length),
        ]

    '''
        returns the splash lines
    '''
    def get_splashlines(self):
        if not self.splashed:
            return self.splashlines
        else:
            return []

class PurpleRainApp(App):
    def build(self):
        return PurpleRain()

PurpleRainApp().run()
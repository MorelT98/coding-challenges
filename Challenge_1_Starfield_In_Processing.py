from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse, Line
from kivy.clock import Clock
import random
from math import sqrt, pow

'''
    ---------------------------------------------
    Coding Challenge #1: Star Field in Processing:
    ---------------------------------------------
    
    This is a python version of the coding challenge from Daniel Shiffman on The Coding Train
    
    Original coding challenge: 
        https://www.youtube.com/watch?v=17WoOqgXsRM&list=PLRqwX-V7Uu6ZiZxtDDRCi6uhfTH4FilpH
        
    Modifications:
        1)  Instead of using the z variable (which I didn't really understand, so feel free to explain it to me),
            I kept track of the the vector from the center of the window to the current location of the star, and
            I moved the star along that vector
            
        2)  I added colors, because everything is just more beautiful with colors
        
        3)  I don't have an option to accelerate using the mouse (Not very important)
'''
class StarfieldApp(App):

    def build(self):
        return Starfield()

class Starfield(BoxLayout):
    NUM_STARS = 100
    TIME = 0.005    # Update time: the smaller, the faster the star move

    # The stars don't actually move in a continuous way, so the bigger the expanding ratio,
    #   the bigger gaps will the stars take to get to the next location
    EXPANDING_RATIO = 100

    # Maximum size of a star, i.e size it will have when it gets to the edge
    MAX_SIZE = 10

    # Ratio controlling the length of the trail of each star. The smaller the ratio, the longer the
    #   trail will be
    TRAIL_RATIO = 10

    def __init__(self, **kwargs):

        super(Starfield, self).__init__(**kwargs)
        Window.size = (400, 400)
        self.size = (400, 400)
        self.stars = [] # Contains all the star objects
        self.initial_locations = [] # Save the initial locations to get the trail later
        self.star_colors = []   # Save the original colors so that the trail can have the same colors

        for i in range(self.NUM_STARS):
            # Create the stars at the center of the window, so that they only appear
            #   a quarter of the width away from the center horizontally, and
            #   a quarter of the height away from the center vertically
            x = random.randint(int(self.size[0] * 3 / 8), int(self.size[0] * 5 / 8))
            y = random.randint(int(self.size[1] * 3 / 8), int(self.size[1] * 5 / 8))

            # Get the distance from the center to figure out the corresponding size of the star
            distance_from_center = self.distance(x, y, self.size[0] / 2, self.size[1] / 2)

            # Create star, save it and its location
            star = Star(x, y, self.get_star_size(distance_from_center))
            self.stars.append(star)
            self.initial_locations.append((x + star.size / 2, y + star.size / 2))

        # Draw the stars
        self.canvas.before.clear()
        with self.canvas.before:
            # For each star, get a random color, save it and draw the stars with that color
            for star in self.stars:
                r = random.uniform(0, 1)
                g = random.uniform(0, 1)
                b = random.uniform(0, 1)
                Color(r, g, b)
                self.star_colors.append((r, g, b))
                star.draw_star()

        # Start the stars movement
        Clock.schedule_interval(self.update_stars, self.TIME)

    '''
        This function determines the size of the star by mapping its 
            distance from the center from the distances range to the
            sizes range
    '''
    def get_star_size(self, distance_from_center):
        max_distance = self.distance(0,0, self.size[0] / 2, self.size[1] / 2)
        return self.map(distance_from_center, 0, max_distance, 0, self.MAX_SIZE)


    '''
        Returns the distance between two points
    '''
    def distance(self, x1, y1, x2, y2):
        Dx = x1 - x2
        Dy = y1 - y2
        return sqrt(pow(Dx, 2) + pow(Dy, 2))

    '''
        This function does the main job, which is, moving the stars, 
            checking if they're still inbounds, and if they are, 
            relocating them
    '''
    def update_stars(self, time):

        self.canvas.before.clear()
        center = (self.size[0] / 2, self.size[1] / 2)

        with self.canvas.before:
            for i in range(len(self.stars)):
                # Check if the star is in bounds
                if self.in_bounds(self.stars[i]):

                    # Find the expanding vector, which is the vector from the center of the window to the star
                    expanding_vector = self.vector(center[0], center[1], self.stars[i].x, self.stars[i].y)

                    # Divide the vector by the expanding ratio, to make the star take smaller gaps when it moves
                    expanding_vector[0] /= self.EXPANDING_RATIO
                    expanding_vector[1] /= self.EXPANDING_RATIO

                    # Move the star
                    self.stars[i].translate(expanding_vector)

                    # Update the size of the star, since it moved
                    size = self.get_star_size(self.distance(self.stars[i].x, self.stars[i].y,
                                                                center[0], center[1]))
                    self.stars[i].size = size
                else:

                    # If the star is not in bounds, relocate it
                    x = random.randint(int(self.size[0] * 3 / 8), int(self.size[0] * 5 / 8))
                    y = random.randint(int(self.size[1] * 3 / 8), int(self.size[1] * 5 / 8))
                    distance_from_center = self.distance(x, y, self.size[0] / 2, self.size[1] / 2)
                    self.stars[i].update(x, y, self.get_star_size(distance_from_center))

                    # Update the initial location of the star, necessary for the trail
                    self.initial_locations[i] = (x, y)

                    # Update the color of the star (makes it less boring)
                    r = random.uniform(0, 1)
                    g = random.uniform(0, 1)
                    b = random.uniform(0, 1)
                    self.star_colors[i] = (r, g, b)

                # Draw the star and the trailing line with the original color of te star
                Color(*self.star_colors[i])
                self.stars[i].draw_star()
                self.draw_line(i)
    '''
        Returns the vector from the starting point (x1, y1) to the 
            ending point (x2, y2)
    '''
    def vector(self, x1, y1, x2, y2):
        return [x2 - x1, y2 - y1]

    '''
        Creates the trail of the star
    '''
    def draw_line(self, i):
        # Set the ending point of the line to the center of the star
        #   (Not the bottom left edge, which explains the self.stars[i].size / 2)
        line_ending_point = (self.stars[i].x + self.stars[i].size / 2,
                             self.stars[i].y + self.stars[i].size / 2)
        initial_point = self.initial_locations[i]

        # Get the starting point of the trail, since its not necessarily the
        #   starting point of the star
        line_starting_point = self.get_line_starting_point(line_ending_point, initial_point)

        # Return the line object
        star_line = (line_ending_point[0], line_ending_point[1],
                     line_starting_point[0], line_starting_point[1])
        return Line(points=star_line, width=1)

    '''
        This functions finds the starting point of the trail, using the trail ratio
    '''
    def get_line_starting_point(self, line_ending_point, initial_point):
        # Vector from initial location of the star to the current location
        vector = self.vector(initial_point[0], initial_point[1], line_ending_point[0], line_ending_point[1])

        # Divide the vector by the trail ratio to get a smaller trail
        vector[0] /= self.TRAIL_RATIO
        vector[1] /= self.TRAIL_RATIO

        # The starting vector becomes the star's current location shifted back by the previous vector
        return (line_ending_point[0] - vector[0], line_ending_point[1] - vector[1])

    '''
        Maps a number x in a range [min_1, max_1] to a corresponding number in the range [min_2, max_2]
    '''
    def map(self, x, min_1, max_1, min_2, max_2):
        return x * (max_2 - min_2) / (max_1 - min_1)

    '''
        Checks if the star is in bounds
    '''
    def in_bounds(self, star):
        return 0 < star.x < self.size[0] and  0 < star.y < self.size[1]


'''
    Class representing a star, providing methods to change its location and draw it
'''
class Star():

    def __init__(self, x, y,size):
        self.update(x, y, size)

    def update(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

    def translate(self, vector):
        self.x += vector[0]
        self.y += vector[1]


    def draw_star(self):
        return Ellipse(pos = (self.x, self.y), size = (self.size, self.size))

StarfieldApp().run()
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rectangle, Color, Ellipse
from kivy.clock import Clock
from kivy.uix.label import Label
import random

'''
    ---------------------------------------------
    Coding Challenge #3: Snake Game:
    ---------------------------------------------

    This is a python version of the coding challenge from Daniel Shiffman on The Coding Train

    Original coding challenge: 
        https://www.youtube.com/watch?v=AaGK-fj-BAM&list=PLRqwX-V7Uu6ZiZxtDDRCi6uhfTH4FilpH&index=3

    Modifications:
        1)  I checked the borders
        
        2)  I prevented the user from going backwards

        3)  After the game is over, instead of starting over directly, I displayed the score
            and gave the user the option to restart by pressing enter

        4)  I changed the boxes into circles
        
        5) I randomized the color of the food
'''

WINDOW_SIZE = (600, 400)
FOOD_SIZE = 10
TIME = 0.1  # Refresh time (The smaller it is, the faster the game)


'''
    This class contains the whole game layout, 
    and is responsible for the display of the game
'''
class SnakeGame(BoxLayout):

    def __init__(self):
        super(SnakeGame, self).__init__()

        self.game_over = False  # keeps track of whether or not the game is over
        self.start()
        self.color = (0.8, 0.1, 0.1, 1) # initial color of the food (red)
        self.previous_key = ''

    '''
        This method creates the snake, displays the first food item and starts the game
    '''
    def start(self):
        self.size = WINDOW_SIZE
        Window.size = self.size

        # randomize the initial position of the snake
        snake_head = self.random_box()
        self.snake = Snake(snake_head[0], snake_head[1])

        # keyboard listener setup
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        # create food for the first time and draw it
        self.create_food()
        self.canvas.before.clear()
        with self.canvas.before:
            Color(random.uniform(0,1), random.uniform(0, 1), random.uniform(0, 1), 1)
            self.show_food()

        # start the clock
        self.event = Clock.schedule_interval(self.draw, TIME)

    '''
        Closes the listener when necessary
    '''
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down = self._on_keyboard_down)
        self._keyboard = None

    '''
        Depending on the key, this function allows the user to move the snake, 
        or restart the game when game over
    '''
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        key = keycode[1]
        # if the game is over, pressing enter restarts the game
        if key == 'enter' and self.game_over:
            self.restart()
            return

        # when the snake hasn't eaten yet, all movements are possible
        if self.previous_key == '' or len(self.snake.body) == 1:
            if key == 'w': self.snake.change_speed(0, FOOD_SIZE)
            if key == 's': self.snake.change_speed(0, -FOOD_SIZE)
            if key == 'a': self.snake.change_speed(-FOOD_SIZE, 0)
            if key == 'd': self.snake.change_speed(FOOD_SIZE, 0)

        # Once the snake starts eating, do not allow backwards movements
        else:
            if key == 'w' and not self.previous_key in ['s', 'w']: self.snake.change_speed(0, FOOD_SIZE)
            if key == 's' and not self.previous_key in ['w', 's']: self.snake.change_speed(0, -FOOD_SIZE)
            if key == 'a' and not self.previous_key in ['d', 'a']: self.snake.change_speed(-FOOD_SIZE, 0)
            if key == 'd' and not self.previous_key in ['a', 'd']: self.snake.change_speed(FOOD_SIZE, 0)

        # save the previous movement
        self.previous_key = key

    '''
        This method updates the movement of the snake, the location of the food and the status of the game
    '''
    def draw(self, time):
        # check if the snake is dead
        self.game_over = self.snake.dies(*self.size)

        if self.game_over:
            # stop the game and output the score
            self.event.cancel()
            self.add_widget(Label(text = "Game Over! Score: {}. Press Enter to Restart".format(len(self.snake.body) - 1)))
        if not self.game_over:
            # update the movement of the snake
            self.canvas.before.clear()
            with self.canvas.before:
                self.snake.update(*self.size)
                self.snake.show_head()
                self.snake.show_body()
                # grow the snake if it eats food, then create a new food item
                if self.snake.ate(self.food):
                    self.snake.grow()
                    self.create_food()
                    self.color = (random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1), 1)
                Color(*self.color)
                self.show_food()

        return not self.game_over

    '''
        Clears the window when the game is over, then restarts it
    '''
    def restart(self):
        self.clear_widgets()
        self.start()

    '''
        returns a random possible location of the snake (or food) on the grid
    '''
    def random_box(self):
        # divide the window into squares, and pick a random square
        max_x = self.size[0] // FOOD_SIZE
        max_y = self.size[1] // FOOD_SIZE

        # 1 and -1 are to avoid the edges
        # multiply back by FOOD_SIZE to get the actual location
        x = random.randint(1, max_x - 1) * FOOD_SIZE
        y = random.randint(1, max_y - 1) * FOOD_SIZE

        return x, y

    '''
        creates food at a random location
    '''
    def create_food(self):
        x, y = self.random_box()
        self.food = [x, y]

    '''
        Display the food
    '''
    def show_food(self):
        return Ellipse(pos = (self.food[0], self.food[1]), size = (FOOD_SIZE, FOOD_SIZE))


'''
    This class represents a Snake, and the behaviours associated with it: moving the snake, 
        checking if it is in bounds, checking if he bit itself, etc
'''
class Snake:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
        self.xspeed = FOOD_SIZE
        self.yspeed = 0
        # add the head of the snake to the body
        self.body = [[self.x, self.y]]

    '''
        Moves the snake in the direction given by the xspeed and yspeed 
        (moves the body of the snake as well)
    '''
    def update(self, width, height):
        self.x += self.xspeed
        self.y += self.yspeed
        self.move_body()

    '''
        Changes the direction of the snake
    '''
    def change_speed(self, xspeed, yspeed):
        self.xspeed = xspeed
        self.yspeed = yspeed

    '''
        Moves the snake's body
    '''
    def move_body(self):
        # Set the location of each body part to the location of the body part before him
        for i in range(len(self.body) - 1):
            self.body[i][0] = self.body[i + 1][0]
            self.body[i][1] = self.body[i + 1][1]
        if len(self.body) > 0:
            # Sets the location of the first body part to the current location of the snake (since the first
            #    body part is the head in my design)
            self.body[-1][0] = self.x
            self.body[-1][1] = self.y

    '''
        Grows the snake, i.e. adds the newly consumed food to the snake's body
    '''
    def grow(self):
        self.body.append([self.x , self.y])


    '''
        Checks whether or not the snake ate the food
    '''
    def ate(self, food):
        # The snake ate the food if they are at the same location
        return self.x == food[0] and self.y == food[1]

    '''
        draw the head of the snake
    '''
    def show_head(self):
        return Ellipse(pos = (self.x, self.y), size = (FOOD_SIZE, FOOD_SIZE))

    '''
        draw the body of the snake
    '''
    def show_body(self):
        body = []
        for bodypart in self.body:
            body.append(Ellipse(pos = bodypart, size = (FOOD_SIZE, FOOD_SIZE)))
        return body

    '''
        Checks if the snake dies
    '''
    def dies(self, width, height):
        return self.eats_itself() or self.out_of_bounds(width, height)

    '''
        Checks if the snake eats itself
    '''
    def eats_itself(self):
        for i in range(len(self.body) - 2):
            if self.x == self.body[i][0] and self.y == self.body[i][1]:
                return True
        return False

    '''
        checks if the snake is out of bounds
    '''
    def out_of_bounds(self, width, height):
        return self.x < 0 or self.x > width - FOOD_SIZE or \
                self.y < 0 or self.y > height - FOOD_SIZE



class SnakeApp(App):
    def build(self):
        return SnakeGame()

SnakeApp().run()


"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao

File: breakoutgraphics.py
Name: Jim Chan
----------------------
The idea of drawing is to compensate my gf for giving her less attention because I was busy finishing this week's assignment lol

"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random

BRICK_SPACING = 5      # Space between bricks (in pixels). This space is used for horizontal and vertical spacing.
BRICK_WIDTH = 40       # Height of a brick (in pixels).
BRICK_HEIGHT = 15      # Height of a brick (in pixels).
BRICK_ROWS = 10        # Number of rows of bricks.
BRICK_COLS = 10        # Number of columns of bricks.
BRICK_OFFSET = 50      # Vertical offset of the topmost brick from the window top (in pixels).
BALL_RADIUS = 10   # Radius of the ball (in pixels).
PADDLE_WIDTH = 75      # Width of the paddle (in pixels).
PADDLE_HEIGHT = 15     # Height of the paddle (in pixels).
PADDLE_OFFSET = 50     # Vertical offset of the paddle from the window bottom (in pixels).

INITIAL_Y_SPEED = 7  # Initial vertical speed for the ball.
MAX_X_SPEED = 5        # Maximum initial horizontal speed for the ball.



class BreakoutGraphics:

    def __init__(self, ball_radius = BALL_RADIUS, paddle_width = PADDLE_WIDTH,
                 paddle_height = PADDLE_HEIGHT, paddle_offset = PADDLE_OFFSET,
                 brick_rows = BRICK_ROWS, brick_cols = BRICK_COLS,
                 brick_width = BRICK_WIDTH, brick_height = BRICK_HEIGHT,
                 brick_offset = BRICK_OFFSET, brick_spacing = BRICK_SPACING,
                 title='Breakout',num_lives = 3):
        self.ball = GOval(ball_radius * 2, ball_radius * 2)
        self.brick_r = brick_rows
        self.num_lives = num_lives
        self.ready = True
        self.num_of_bricks_broke = 0

        # Create a graphical window, with some extra space
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=window_width, height=window_height, title=title)


        # Create a paddle
        self.paddle = GRect(width=paddle_width, height=paddle_height)#paddle_width / self.window.width
        self.paddle.filled = True
        self.paddle.fill_color = 'black'
        self.paddle_offset = paddle_offset
        self.window.add(self.paddle, x=(self.window.width - self.paddle.width) / 2, y=self.window.height - self.paddle_offset)

        # Center a filled ball in the graphical window
        # Default initial velocity for the ball
        self.ball_radius = BALL_RADIUS
        self.reset_ball()

        # Initialize our mouse listeners
        onmousemoved(self.paddle_position)

        # Draw bricks
        y = brick_offset
        for j in range(brick_rows):
            color = self.which_color(j)
            brick_x = 0
            for i in range((self.window.width-brick_width)//(brick_width+brick_spacing)+1):
                brick = GRect(brick_width,brick_height)
                brick.filled = True
                brick.fill_color = color
                brick.color = color
                self.window.add(brick, x=brick_x+i*(brick_width+brick_spacing), y=y)
            y += brick_height+brick_spacing
        # Create scoreboard
        self.score = GLabel('Score : ' )
        self.window.add(self.score,x=0, y=self.window.height)

        onmouseclicked(self.detect_did_the_game_stop_and_start_new_ball)

    def detect_did_the_game_stop_and_start_new_ball(self, event):
        """
        :param event: location of the mouse
        """
        obj = self.window.get_object_at((self.window.width - self.ball.width) / 2, (self.window.height - self.ball.height) / 2)
        if obj is None:
            self.ready = False
        else:
            self.ready = True

    def reset_game(self):
        """
        trigger of resetting the game when the ball runs out of window
        :return: bool. True
        """
        self.ready = True

    # def live_count(self, lives_in_game):
    #     self.lives_in_games = lives_in_game

    def reset_ball(self):
        """
        reset the ball when the ball runs out of the window
        """
        self.ball.filled = True
        self.ball.fill_color = 'black'
        self.ball.color = 'black'
        self.window.add(self.ball, x=(self.window.width - self.ball.width) / 2, y=(self.window.height - self.ball.height) / 2)
        self.set_velocity()

    def set_velocity(self):
        """
        set the original velocity of the ball when the ball is reset
        """
        self.__dx = random.randint(1, MAX_X_SPEED)
        self.__dy = INITIAL_Y_SPEED
        if random.random() > 0.5:
            self.__dx = -self.__dx

    def reverse_xv(self, new_xv):
        """
        :param new_xv: getter of the latest x velocity of the ball
        assign an opposite x-direction velocity to the ball
        """
        self.__dx = -new_xv

    def reverse_yv(self, new_yv):
        """
        :param new_xv: getter of the latest y velocity of the ball
        assign an opposite y-direction velocity to the ball
        """
        self.__dy = -new_yv

    dx = 0
    dy = 0

    def ball_move(self,dx,dy):
        self.ball.move(dx, dy)

    def get_dx(self):
        return self.__dx

    def get_dy(self):
        return self.__dy

    def paddle_position(self,m):
        """
        Moving the paddle with the mouse
        :param m: location of the mouse
        """
        middle_of_paddle = m.x-self.paddle.width*0.5
        if 0 <= middle_of_paddle <= self.window.width-self.paddle.width:
            self.paddle.x = middle_of_paddle

    def which_color(self, j):
        """
        :param j: the specific roll of brick
        :return: the specific color for each roll of bricks
        """
        if 0 <= j % 10 <= 1:
            brick_color = 'red'
        if 2 <= j % 10 <= 3:
            brick_color = 'orange'
        if 4 <= j % 10 <= 5:
            brick_color = 'yellow'
        if 6 <= j % 10 <= 7:
            brick_color = 'green'
        if 8 <= j % 10 <= 9:
            brick_color = 'navy'
        return brick_color

    def whether_ball_touch_object(self):
        """
        detecting whether the ball touches any object with four corners of its circumscribed square
        """

        obj_lefttop = self.window.get_object_at(self.ball.x-1,self.ball.y-1)
        obj_righttop = self.window.get_object_at(self.ball.x+2*self.ball_radius+1,self.ball.y-1)
        obj_leftbot = self.window.get_object_at(self.ball.x-1, self.ball.y+2*self.ball_radius+1)
        obj_rightbot = self.window.get_object_at(self.ball.x+(2*self.ball_radius)+1, self.ball.y+(2*self.ball_radius+1)+1)
        if self.ball.y <= self.window.height-50:
            self.checkpointtop(obj_lefttop,obj_righttop,obj_leftbot,obj_rightbot)

    def checkpointtop(self, obj, obj2 , obj3, obj4):
        if obj is not None and obj2 is not None and obj3 is None and obj4 is None:
            if self.window.get_object_at(self.ball.x+self.ball_radius,self.ball.y) is not None:
                print('middle upper +1')
                self.window.remove(obj)
                self.num_of_bricks_broke += 1
                self.score.text = ('Score :' + str(self.num_of_bricks_broke))
                self.__dy *= -1
            else:
                self.window.remove(obj)
                self.window.remove(obj2)
                self.num_of_bricks_broke += 2
                print('middle upper +2')
                self.score.text = ('Score :' + str(self.num_of_bricks_broke))
                self.__dy *= -1
        if obj is not None and obj2 is None and obj3 is None and obj4 is None:
            self.window.remove(obj)
            self.num_of_bricks_broke += 1
            print('Upper left + 1')
            self.score.text = ('Score :' + str(self.num_of_bricks_broke))
            self.__dy *= -1
        if obj2 is not None and obj is None and obj3 is None and obj4 is None:
            self.window.remove(obj2)
            self.num_of_bricks_broke += 1
            print('upper right +1')
            self.score.text = ('Score :' + str(self.num_of_bricks_broke))
            self.__dy *= -1

    # def checkpointbot(self, obj3,obj4):
        if self.ball.y <= self.window.height / 2: #paddle不會被移除
            if obj3 is not None and obj4 is not None and obj is None and obj2 is None:
                if self.window.get_object_at(self.ball.x + self.ball_radius, self.ball.y+2*self.ball_radius) is not None:
                    self.window.remove(obj3)
                    self.num_of_bricks_broke += 1
                    print('bot mid +1')
                    self.score.text = ('Score :' + str(self.num_of_bricks_broke))
                    self.__dy *= -1
                else:
                    self.window.remove(obj3)
                    self.window.remove(obj4)
                    self.num_of_bricks_broke += 2
                    print('bot both +2')
                    self.score.text = ('Score :' + str(self.num_of_bricks_broke))
                    self.__dy *= -1
            if obj3 is not None and obj4 is None and obj is None and obj2 is None:
                self.window.remove(obj3)
                self.num_of_bricks_broke += 1
                self.score.text = ('Score :' + str(self.num_of_bricks_broke))
                self.__dy *= -1
            if obj4 is not None and obj3 is None and obj is None and obj2 is None:
                self.window.remove(obj4)
                self.num_of_bricks_broke += 1
                print('bot right +1')
                self.score.text = ('Score :' + str(self.num_of_bricks_broke))
                self.__dy *= -1
        else:
            if obj3 is not None or obj4 is not None:
                self.__dy *= -1

    # def checkpointleftside(self, obj, obj3): #左上 左下
        if obj is not None and obj3 is not None and obj2 is None and obj4 is None:
            if self.window.get_object_at(self.ball.x-1,self.ball.y+self.ball_radius) is not None:
                obj_middle = self.window.get_object_at(self.ball.x-1,self.ball.y+self.ball_radius)
                self.window.remove(obj_middle)
                self.num_of_bricks_broke += 1
                print(' left +1')
                self.score.text = ('Score :' + str(self.num_of_bricks_broke))
                self.__dx *= -1
            else:
                self.window.remove(obj)
                self.window.remove(obj3)
                self.num_of_bricks_broke +=1
                print(' left +1')
                self.score.text = ('Score :' + str(self.num_of_bricks_broke))
                self.__dx *= -1


    # def checkpointrightside(self, obj2, obj4): #右上 右下
        if obj2 is not None and obj4 is not None and obj is None and obj3 is None:
            if self.window.get_object_at(self.ball.x+self.ball_radius*2+1,self.ball.y+self.ball_radius) is not None:
                obj_middle = self.window.get_object_at(self.ball.x+self.ball_radius*2+1,self.ball.y+self.ball_radius)
                self.window.remove(obj_middle)
                self.num_of_bricks_broke += 1
                print(' right +1')
                self.score.text = ('Score :' + str(self.num_of_bricks_broke))
                self.__dx *= -1
            else:
                self.window.remove(obj2)
                self.window.remove(obj4)
                self.num_of_bricks_broke += 1
                print(' right +')
                self.score.text = ('Score :' + str(self.num_of_bricks_broke))
                self.__dx *= -1

        if obj is not None and obj2 is not None and obj3 is not None and obj4 is None:
            self.window.remove(obj2)
            self.window.remove(obj)
            self.window.remove(obj3)
            self.num_of_bricks_broke += 3
            print(' top left corner +3')
            self.__dx *= -1
            self.__dy *= -1

        if obj is not None and obj2 is not None and obj4 is not None and obj3 is None:
            self.window.remove(obj2)
            self.window.remove(obj)
            self.window.remove(obj4)
            self.num_of_bricks_broke += 3
            print(' bot right corner +3')
            self.__dx *= -1
            self.__dy *= -1

        if obj is not None and obj4 is not None and obj3 is not None and obj2 is None:
            self.window.remove(obj3)
            self.window.remove(obj)
            self.window.remove(obj4)
            self.num_of_bricks_broke += 3
            print(' top right corner +3')
            self.__dx *= -1
            self.__dy *= -1

        if obj2 is not None and obj4 is not None and obj3 is not None and obj is None:
            self.window.remove(obj2)
            self.window.remove(obj3)
            self.window.remove(obj4)
            self.num_of_bricks_broke += 3
            print(' top right corner +3')
            self.__dx *= -1
            self.__dy *= -1


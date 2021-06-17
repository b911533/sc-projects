"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

File: breakout.py
Name: Jim Chan
----------------------
The idea of drawing is to compensate my gf for giving her less attention because I was busy finishing this week's assignment lol

"""

from campy.gui.events.timer import pause
from breakoutgraphics2 import BreakoutGraphics

FRAME_RATE = 1000 / 120 # 120 frames per second
NUM_LIVES = 3			# Number of attempts


def main():
    """
    This program conducts a brick-breaking game. User can determine the rows of bricks and the lives he has in the
    game. This game stops when user is out of lives or all the bricks are broken.
    """
    lives = NUM_LIVES
    graphics = BreakoutGraphics(brick_rows = 10 , num_lives = lives)
    while True:
        ready_to_start_new_game = graphics.ready
        if not ready_to_start_new_game:
            graphics.whether_ball_touch_object()
            graphics.ball_move(graphics.get_dx(),graphics.get_dy())
            if graphics.ball.x <= 0 or graphics.ball.x+graphics.ball.width >= graphics.window.width:
                graphics.reverse_xv(graphics.get_dx())
            if graphics.ball.y <= 0:
                graphics.reverse_yv(graphics.get_dy())
            if graphics.ball.y + graphics.ball.height >= graphics.window.height:
                lives -= 1
                graphics.window.remove(graphics.ball)
                graphics.reset_ball()
                graphics.reset_game()
            if lives == 0 or graphics.num_of_bricks_broke == 10 * graphics.brick_r:
                graphics.window.remove(graphics.ball)
                graphics.reset_ball()
                break
            pause(FRAME_RATE)
        else:
            pause(10)


if __name__ == '__main__':
    main()

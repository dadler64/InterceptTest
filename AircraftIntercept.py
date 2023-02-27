"""
    2D aircraft intercept demo
"""

from sprites import Factory, Plane, Side
from vectors import Vec2D
import math
import arcade

# Set up the constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Aircraft Intercept Example"


class AircraftIntercept(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.count: int = 0

        self.paused: bool = False
        self.aircraft_intercepted: bool = False
        self.step_mode: bool = False
        self.step: bool = False

        self.intercept_pos: Vec2D = None
        self.intercept_time: str = None

        # Create the item instance
        self.blue_plane: Plane = None
        self.red_plane: Plane = None
        self.blue_factory: Factory = None
        self.mouse_x = 0
        self.mouse_y = 0

        self.sprite_list = arcade.SpriteList()

        self.debug_lines = True

        # Set background color
        arcade.set_background_color(arcade.color.BLACK)

    # Used to help set up and restart the demo
    def setup(self):
        self.sprite_list.clear()

        self.count = 0

        self.paused = False
        self.aircraft_intercepted = False
        self.step_mode = False
        self.step = True

        self.intercept_pos: Vec2D = None
        self.intercept_time = "???"

        # Create the item instance
        self.blue_plane = Plane(side=Side.BLUE)
        self.red_plane = Plane(side=Side.RED)
        self.blue_factory = Factory(side=Side.BLUE, scale=0.1)

        # Position the items
        self.blue_plane.center_x = 200
        self.blue_plane.center_y = 50
        self.red_plane.center_x = 50
        self.red_plane.center_y = 450

        self.blue_factory.center_x = 750
        self.blue_factory.center_y = 450

        self.red_plane.angle = 270
        """ TESTING ONLY """
        self.blue_plane.speed = 1.25

        # Add the item to the lists
        self.sprite_list.append(self.blue_plane)
        self.sprite_list.append(self.red_plane)
        self.sprite_list.append(self.blue_factory)

        # Red plane will travel towards the factory
        self.red_plane.destination_point = Vec2D(self.blue_factory.center_x,
                                                 self.blue_factory.center_y)
        # Blue plane will initially go to the factory but will in reality follow intercept path
        self.blue_plane.destination_point = Vec2D(self.blue_factory.center_x,
                                                  self.blue_factory.center_y)

    def on_update(self, delta_time):
        if not self.paused or self.aircraft_intercepted:
            if self.step:
                self.calc_intercept()

                self.blue_plane.destination_point = self.intercept_pos

                self.sprite_list.update()
            if self.step_mode:
                self.step = False

    def on_draw(self):
        if self.paused:
            arcade.draw_text("PAUSED",
                             arcade.get_window().width / 2 - 100, 20,
                             arcade.color.WHITE, 48)
        elif self.aircraft_intercepted:
            arcade.draw_text("INTERCEPTED!",
                             arcade.get_window().width / 2 - 250,
                             arcade.get_window().height - 75,
                             arcade.color.WHITE, 48)
        else:
            if self.step:
                """ Render the screen. """
                # Clear screen
                self.clear()
                self.sprite_list.draw()

                # Mouse position
                arcade.draw_text(
                    f"mouse x: {int(self.mouse_x)}, y: {int(self.mouse_y)}",
                    10, self.height - 20, arcade.color.WHITE, 12)
                # Time to intercept
                arcade.draw_text(
                    f"Time to Intercept: {round(self.intercept_time) / 10}s",
                    arcade.get_window().width - 200, self.height - 20,
                    arcade.color.WHITE, 12)

                # Red aircraft speed label
                arcade.draw_text(f"Vr: {self.red_plane.speed}",
                                 self.red_plane.center_x - 10,
                                 self.red_plane.center_y + 30,
                                 arcade.color.WHITE, 12)
                # Blue aircraft speed label
                arcade.draw_text(f"Vb: {self.blue_plane.speed}",
                                 self.blue_plane.center_x - 10,
                                 self.blue_plane.center_y - 30,
                                 arcade.color.WHITE, 12)

                if self.debug_lines:
                    # Intercept circle
                    if self.intercept_pos != None:
                        arcade.draw_circle_outline(self.intercept_pos.x,
                                                   self.intercept_pos.y, 20,
                                                   arcade.color.WHITE)
                    # Blue to red line
                    arcade.draw_line(self.blue_plane.center_x,
                                     self.blue_plane.center_y,
                                     self.red_plane.center_x,
                                     self.red_plane.center_y,
                                     arcade.color.GREEN)
                    # Red line to end point
                    arcade.draw_line(self.red_plane.center_x,
                                     self.red_plane.center_y,
                                     self.blue_factory.center_x,
                                     self.blue_factory.center_y,
                                     arcade.color.RED)
                    # Blue line to red intercept
                    if self.blue_plane.destination_point != None:
                        arcade.draw_line(self.blue_plane.center_x,
                                         self.blue_plane.center_y,
                                         self.blue_plane.destination_point.x,
                                         self.blue_plane.destination_point.y,
                                         arcade.color.BLUE)
            if self.step_mode:
                arcade.draw_text("step mode",
                                 arcade.get_window().width / 2 - 100,
                                 arcade.get_window().height - 50,
                                 arcade.color.WHITE, 12)

                self.step = False

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.mouse_x = x
        self.mouse_y = y

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.R:
            self.setup()

        if symbol == arcade.key.L:
            self.debug_lines = True if not self.debug_lines else False

        if symbol == arcade.key.P:
            self.paused = True if not self.paused else False

        # if symbol == arcade.key.M:
        #     self.step_mode = True if not self.step_mode else False

        # if symbol == arcade.key.S:
        #     self.step = True

        if symbol == arcade.key.EQUAL:
            if self.blue_plane.speed < 1.5:
                self.blue_plane.speed += 0.25
        elif symbol == arcade.key.MINUS:
            if self.blue_plane.speed > 0.25:
                self.blue_plane.speed -= 0.25

    def calc_intercept(self):
        blue_pos = Vec2D(self.blue_plane.center_x, self.blue_plane.center_y)
        red_pos = Vec2D(self.red_plane.center_x, self.red_plane.center_y)

        # Check if the red plane has reached the factory (check for collision)
        if self.red_plane.collides_with_sprite(self.blue_factory):
            print("Red plane has Reached the factory!")
            # self.paused = True
            return

        # Check if the red plane has been intercepted (check for collision)
        if self.blue_plane.collides_with_sprite(self.red_plane):
            print("Red plane has been intercepted!")
            self.aircraft_intercepted = True
            return

        if self.blue_plane.speed <= 0:
            return

        vector_from_red: Vec2D = red_pos.subtract(blue_pos.x, blue_pos.y)
        distance_to_red: float = vector_from_red.length()

        if self.red_plane.speed == 0:
            self.intercept_time = distance_to_red / self.blue_plane.speed
            self.intercept_pos = red_pos
        else:
            a: float = self.blue_plane.speed * self.blue_plane.speed - \
                       self.red_plane.speed * self.red_plane.speed
            b: float = 2 * distance_to_red * self.red_plane.speed
            c: float = -distance_to_red * distance_to_red

            if a == 0:
                return

            d: float = (b**2) - (4 * a * c)
            t1: float = (-b + math.sqrt(d)) / (2 * a)
            t2: float = (-b - math.sqrt(d)) / (2 * a)

            # Slow down output for debugging
            if self.count <= 20:
                self.count += 1
            else:
                print(f"Intercept Point: {self.intercept_pos}")
                # print(f"Intercept values are {t1} and {t2}")
                self.count = 0

            # If both values are negative then the intercept would have already happened
            if t1 < 0 and t2 < 0:
                return

            # If both values are positive take the smaller of the two values
            # (TLDR: always try to take the lowest positive value)
            if t1 > 0 and t2 > 0:
                self.intercept_time = min(t1, t2)
            elif t1 > 0 > t2:
                self.intercept_time = t1
            elif t1 < 0 < t2:
                self.intercept_time = t2
            else:
                return

            # TODO: Fix so that the intercept point works on x and y axis
            # Project the intercept position ahead of the red aircraft along the x axis
            self.intercept_pos = Vec2D(
                red_pos.x + self.red_plane.speed * self.intercept_time,
                red_pos.y)


def main():
    """ Main function """
    game = AircraftIntercept(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.center_window()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()

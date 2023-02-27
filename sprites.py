from enum import Enum
from vectors import Vec2D
import arcade
import math

jet_blue_img = "./res/img/Jet Blue.png"
jet_red_img = "./res/img/Jet Red.png"
jet_gray_img = "./res/img/Jet Gray.png"
jet_black_img = "./res/img/Jet Black.png"
factory_img = "./res/img/factory.png"


class Side(Enum):
    UNKNOWN = -1
    NEUTRAL = 0
    BLUE = 1
    RED = 2


class Factory(arcade.Sprite):

    def __init__(self,
                 side: Side = Side.UNKNOWN,
                 scale: float = 0.5,
                 hit_box_algorithm: str = "Simple") -> None:
        # self.filename = jet_grey_img
        self.window = arcade.get_window()
        self.health = 100
        self.hit_box = hit_box_algorithm

        if side == Side.BLUE:
            super().__init__(filename=factory_img, scale=scale)
        elif side == Side.RED:
            super().__init__(filename=factory_img, scale=scale)
        elif side == Side.UNKNOWN:
            super().__init__(filename=factory_img, scale=scale)
        else:
            super().__init__(filename=factory_img, scale=scale)


class Plane(arcade.Sprite):

    def __init__(self, side: Side = Side.UNKNOWN, scale: float = 0.5) -> None:

        self.window = arcade.get_window()
        self.health = 100

        if side == Side.BLUE:
            super().__init__(filename=jet_blue_img, scale=scale)
        elif side == Side.RED:
            super().__init__(filename=jet_red_img, scale=scale)
        elif side == Side.UNKNOWN:
            super().__init__(filename=jet_black_img, scale=scale)
        else:
            super().__init__(filename=jet_gray_img, scale=scale)

        # Destination point is where we are going
        self.destination_point: Vec2D = None

        # Rotation needed so aircraft points in the right direction when moving
        self.image_rotation = -90

        # Default speed
        self.speed = 1.0

        # Max speed we can rotate
        self.rot_speed = 1

    def update(self):
        """
            Movement code borrowed from the "Turn and Move" PyArcade example.
            https://api.arcade.academy/en/latest/examples/turn_and_move.html#turn-and-move
        """
        # If we have no destination, don't go anywhere.
        # if not self.destination_point:
        # if self.destination_point[0] == None or self.destination_point[1] == None:
        if self.destination_point is None:
            self.change_x = 0
            self.change_y = 0
            return

        # Position the start at our current location
        start_x = self.center_x
        start_y = self.center_y

        # Get the destination location
        dest_x = self.destination_point.x
        dest_y = self.destination_point.y

        # Do math to calculate how to get the sprite to the destination.
        # Calculation the angle in radians between the start points
        # and end points. This is the angle the player will travel.
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        target_angle_radians = math.atan2(y_diff, x_diff)
        if target_angle_radians < 0:
            target_angle_radians += 2 * math.pi

        # What angle are we at now in radians?
        actual_angle_radians = math.radians(self.angle - self.image_rotation)

        # How fast can we rotate?
        rot_speed_radians = math.radians(self.rot_speed)

        # What is the difference between what we want, and where we are?
        angle_diff_radians = target_angle_radians - actual_angle_radians

        # Figure out if we rotate clockwise or counter-clockwise
        if abs(angle_diff_radians) <= rot_speed_radians:
            # Close enough, let's set our angle to the target
            actual_angle_radians = target_angle_radians
            clockwise = None
        elif angle_diff_radians > 0 and abs(angle_diff_radians) < math.pi:
            clockwise = False
        elif angle_diff_radians > 0 and abs(angle_diff_radians) >= math.pi:
            clockwise = True
        elif angle_diff_radians < 0 and abs(angle_diff_radians) < math.pi:
            clockwise = True
        else:
            clockwise = False

        # Rotate the proper direction if needed
        if actual_angle_radians != target_angle_radians and clockwise:
            actual_angle_radians -= rot_speed_radians
        elif actual_angle_radians != target_angle_radians:
            actual_angle_radians += rot_speed_radians

        # Keep in a range of 0 to 2pi
        if actual_angle_radians > 2 * math.pi:
            actual_angle_radians -= 2 * math.pi
        elif actual_angle_radians < 0:
            actual_angle_radians += 2 * math.pi

        # Convert back to degrees
        self.angle = math.degrees(actual_angle_radians) + self.image_rotation

        # Are we close to the correct angle? If so, move forward.
        if abs(angle_diff_radians) < math.pi / 4:
            self.change_x = math.cos(actual_angle_radians) * self.speed
            self.change_y = math.sin(actual_angle_radians) * self.speed

        # Fine-tune our change_x/change_y if we are really close to destination
        # point and just need to set to that location.
        traveling = False
        if abs(self.center_x - dest_x) < abs(self.change_x):
            self.center_x = dest_x
        else:
            self.center_x += self.change_x
            traveling = True

        if abs(self.center_y - dest_y) < abs(self.change_y):
            self.center_y = dest_y
        else:
            self.center_y += self.change_y
            traveling = True

        # If we have arrived, then cancel our destination point
        if not traveling:
            self.destination_point = None

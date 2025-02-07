import json
from collections import OrderedDict
from math import atan2, cos, degrees, radians, sin
from time import localtime, ticks_ms

import imu
import ntptime
from events.input import BUTTON_TYPES, Buttons
from system.eventbus import eventbus
from system.patterndisplay.events import PatternDisable
from tildagonos import tildagonos

import app

from .lib.asset_path import ASSET_PATH
from .lib.background import Background
from .lib.emf import EMF
from .lib.gamma import gamma_corrections
from .lib.hand import Hand
from .lib.shapes_list import shapes
from .pikesley.rgb_from_hue.rgb_from_hue import rgb_from_degrees

with open(ASSET_PATH + "conf.json") as j:  # noqa: PTH123
    conf = json.loads(j.read())


class Clock(app.App):
    """Clock."""

    def __init__(self):
        """Construct."""
        eventbus.emit(PatternDisable())
        ntptime.settime()

        self.button_states = Buttons(self)

        # index in the `shapes` list
        self.shapes_index = 0

        # how much screen we use
        self.radius = 118

        # this increments to rotate the spectrum colours
        self.colour_offset = 0
        # by this much each time
        self.colour_increment = 2
        self.rotate_colours_clockwise = True
        self.led_brightness = 0.5

        self.notifiers = {
            "pulse": {"enabled": False, "timer": 0, "duration": 100},
        }

        # how much to rotate the clock face
        self.rotation_offset = 0

        self.new_second = False
        self.previous_seconds = 0
        self.pulse_size = 2
        self.cardinal_point_bump = 4

        self.marker_growth_increment = 2

        self.calculate_marker_offset()

    def update(self, _):
        """Update."""
        self.scan_buttons()

        self.update_notifiers()

        # rotate the colours
        increment = (
            self.colour_increment
            if self.rotate_colours_clockwise
            else (0 - self.colour_increment)
        )
        self.colour_offset = (self.colour_offset + increment) % 360

        acc = imu.acc_read()

        # weighting is zero when badge is laying down flat,
        # so rotation_offset is zeroed-out
        # weight maxes out at one when badge is vertical
        # so we calculate entire offset from tilt
        weighting = min(1.0, int(abs(10 - acc[2])) / 9)
        self.rotation_offset = (degrees(atan2(acc[1], acc[0]))) * weighting

        tildagonos.leds.write()

    def draw(self, ctx):
        """Draw."""
        self.overlays = []

        self.hours, self.minutes, self.seconds = localtime()[3:6]
        self.overlays.append(Background(colour=conf["background-colour"]))

        self.draw_brand()

        self.draw_markers()
        self.light_leds()

        rotations = OrderedDict(
            {
                "hour": ((self.hours * 3600) + (self.minutes * 60) + self.seconds)
                / 120,
                "minute": ((self.minutes * 60) + self.seconds) / 10,
                "second": (self.seconds * 6) + self.overtick,
            }
        )

        for key, rotation in rotations.items():
            self.draw_hand(key, rotation)

        self.draw_overlays(ctx)

    def update_notifiers(self):
        """Update the `notifiers`."""
        for notifier in self.notifiers.values():
            if ticks_ms() - notifier["timer"] > notifier["duration"]:
                notifier["enabled"] = False

    def set_notifier(self, name):
        """Set notifier `name`."""
        self.notifiers[name]["enabled"] = True
        self.notifiers[name]["timer"] = ticks_ms()

    @property
    def overtick(self):
        """Calculate overtick."""
        overtick = 0
        if self.seconds != self.previous_seconds:
            self.new_second = True
            self.previous_seconds = self.seconds
            overtick = conf["overtick-amount"]
        self.new_second = False

        return overtick

    def draw_brand(self):
        """Write `EMF`."""
        centre = (
            -sin(radians(self.rotation_offset)) * conf["brand"]["y-offset"],
            -cos(radians(-self.rotation_offset)) * conf["brand"]["y-offset"],
        )

        scale = conf["brand"]["scale"]
        if self.notifiers["pulse"]["enabled"]:
            scale += self.pulse_size

        self.overlays.append(
            EMF(
                centre=centre,
                colour=rgb_from_degrees(self.colour_offset),
                rotation=-self.rotation_offset,
                scale=scale,
            )
        )

    def draw_hand(self, key, rotation):
        """Draw a hand."""
        rotation = rotation - self.rotation_offset

        colour = rgb_from_degrees(self.colour_offset % 360)
        if conf["full-spectrum"]:
            colour = rgb_from_degrees((180 - rotation + self.colour_offset) % 360)

        self.overlays.append(
            Hand(
                colour=colour,
                filled=True,
                opacity=0.8,
                principal_length=conf["hands"][key]["length"],
                rotation=rotation,
                tail_length=conf["hands-overhang"],
                width=conf["hands"][key]["width"],
            )
        )

    def draw_markers(self):
        """Draw the number-ish bits."""
        for angle in range(0, 360, 30):
            rotation = angle + self.rotation_offset
            pair = (
                sin(radians(rotation)) * self.marker_offset,
                cos(radians(rotation)) * self.marker_offset,
            )

            colour = rgb_from_degrees(self.colour_offset % 360)
            if conf["full-spectrum"]:
                colour = rgb_from_degrees((rotation + self.colour_offset) % 360)

            size = conf["marker-size"]
            if self.notifiers["pulse"]["enabled"]:
                size += self.pulse_size

            if angle in [0, 90, 180, 270]:
                pair = (
                    sin(radians(rotation))
                    * (self.marker_offset - self.cardinal_point_bump),
                    cos(radians(rotation))
                    * (self.marker_offset - self.cardinal_point_bump),
                )
                size += self.cardinal_point_bump

            filled = conf["filled-markers"]

            self.overlays.append(
                shapes[self.shapes_index](
                    centre=pair,
                    colour=colour,
                    filled=filled,
                    rotation=-rotation,
                    size=size,
                )
            )

    def light_leds(self):
        """Light the lights."""
        for i in range(12):
            colour = rgb_from_degrees(self.colour_offset % 360)
            if conf["full-spectrum"]:
                # 30 degrees per light
                # 15 degree offset to be between the markers
                # 180 offset because the goddamn screen is upside-down
                colour = rgb_from_degrees(
                    ((i * 30) + 15 + 180 + self.colour_offset) % 360
                )
            tildagonos.leds[12 - i] = [
                gamma_corrections[int(c * 255 * self.led_brightness)] for c in colour
            ]

    def calculate_marker_offset(self):
        """Recalculate when markers change size."""
        self.marker_offset = self.radius - conf["marker-size"] - 1

    def invert_fill_markers(self):
        """Invert marker-filling."""
        conf["filled-markers"] = not conf["filled-markers"]

    def invert_full_spectrum(self):
        """Invert full-spectrum."""
        conf["full-spectrum"] = not conf["full-spectrum"]

    def increment_shapes_index(self):
        """Increment shapes-index."""
        self.shapes_index = (self.shapes_index + 1) % len(shapes)

    def grow_markers(self):
        """Make the markers bigger."""
        conf["marker-size"] += self.marker_growth_increment
        self.calculate_marker_offset()

    def shrink_markers(self):
        """Make the markers littler."""
        if conf["marker-size"] > self.marker_growth_increment:
            conf["marker-size"] -= self.marker_growth_increment
            self.calculate_marker_offset()

    def scan_buttons(self):
        """Read the buttons."""
        buttons = {
            "CANCEL": self.minimise,
            "CONFIRM": self.invert_fill_markers,
            "UP": self.increment_shapes_index,
            "DOWN": self.invert_full_spectrum,
            "RIGHT": self.grow_markers,
            "LEFT": self.shrink_markers,
        }
        for button, method in buttons.items():
            if self.button_states.get(BUTTON_TYPES[button]):
                self.button_states.clear()
                method()
                self.set_notifier("pulse")


__app_export__ = Clock

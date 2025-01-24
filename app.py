import json
from collections import OrderedDict
from math import cos, radians, sin
from time import localtime, ticks_ms

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
from .lib.rgb_from_rotation import rgb_from_degrees
from .lib.shapes.line import Line
from .lib.shapes_list import shapes

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

        # how far the markers are from the edge
        self.marker_offset = self.radius - conf["marker-size"] - 1

        # this increments to rotate the spectrum colours
        self.colour_offset = 0
        # by this much each time
        self.colour_increment = 2
        self.rotate_colours_clockwise = True
        self.led_brightness = 0.5

        self.notifiers = {
            "rotation": {"enabled": False, "timer": 0, "duration": 1000},
            "pulse": {"enabled": False, "timer": 0, "duration": 100},
        }

        # how much to rotate the clock face
        self.rotation_offset = 0

        self.new_second = False
        self.previous_seconds = 0
        self.pulse_size = 2

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

        scale=conf["brand"]["scale"]
        if self.notifiers["pulse"]["enabled"]:
            scale += self.pulse_size

        self.overlays.append(
            EMF(
                centre=centre,
                scale=scale,
                rotation=radians(-self.rotation_offset),
                colour=rgb_from_degrees(self.colour_offset),
            )
        )

    def draw_hand(self, key, rotation):
        """Draw a hand."""
        rotation = rotation - self.rotation_offset
        coords = {
            "start": (
                sin(radians(rotation)) * -conf["hands-overhang"],
                cos(radians(rotation)) * conf["hands-overhang"],
            ),
            "end": (
                sin(radians(rotation)) * conf["hands"][key]["length"],
                cos(radians(rotation)) * -conf["hands"][key]["length"],
            ),
        }

        colour = rgb_from_degrees(self.colour_offset % 360)
        if conf["full-spectrum"]:
            colour = rgb_from_degrees((180 - rotation + self.colour_offset) % 360)

        self.overlays.append(
            Line(
                start=(coords["start"]),
                end=coords["end"],
                width=conf["hands"][key]["width"],
                colour=colour,
                opacity=0.8,
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

            filled = conf["filled-markers"]

            if self.notifiers["rotation"]["enabled"] and angle == 180:  # noqa: PLR2004
                pair = (
                    sin(radians(rotation)) * (self.marker_offset - size),
                    cos(radians(rotation)) * (self.marker_offset - size),
                )
                size = size * 2

            self.overlays.append(
                shapes[self.shapes_index](
                    centre=pair,
                    size=size,
                    colour=colour,
                    rotation=radians(-rotation),
                    filled=filled,
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

    def invert_fill_markers(self):
        """Invert marker-filling."""
        conf["filled-markers"] = not conf["filled-markers"]

    def invert_full_spectrum(self):
        """Invert full-spectrum."""
        conf["full-spectrum"] = not conf["full-spectrum"]

    def increment_shapes_index(self):
        """Increment shapes-index."""
        self.shapes_index = (self.shapes_index + 1) % len(shapes)

    def invert_clockwise_colour_rotation(self):
        """Invert clockwise colour-rotation."""
        self.rotate_colours_clockwise = not self.rotate_colours_clockwise

    def rotate_clock_face(self):
        """Rotate the clock face."""
        self.rotation_offset = (self.rotation_offset + 30) % 360
        self.set_notifier("rotation")

    def scan_buttons(self):
        """Read the buttons."""
        buttons = {
            "CANCEL": self.minimise,
            "CONFIRM": self.invert_fill_markers,
            "UP": self.increment_shapes_index,
            "DOWN": self.invert_full_spectrum,
            "LEFT": self.rotate_clock_face,
            "RIGHT": self.invert_clockwise_colour_rotation,
        }
        for button, method in buttons.items():
            if self.button_states.get(BUTTON_TYPES[button]):
                self.button_states.clear()
                method()
                self.set_notifier("pulse")


__app_export__ = Clock

import json
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
        self.background_colour = conf["background-colour"]

        # how much hand sticks out beyond the centre
        self.overhang = conf["hands-overhang"]
        self.marker_size = conf["marker-size"]
        self.fill_markers = conf["filled-markers"]

        # rainbow or single-colour
        self.full_spectrum = conf["full-spectrum"]

        self.button_states = Buttons(self)

        # index in the `shapes` list
        self.shapes_index = 0

        # how much screen we use
        self.radius = 118

        # how far the markers are from the edge
        self.marker_offset = self.radius - self.marker_size - 1

        # this increments to rotate the spectrum colours
        self.colour_offset = 0
        # by this much each time
        self.colour_increment = 2
        self.rotate_colours_clockwise = True
        self.led_brightness = 0.5

        # how long to highlight the top marker when we rotate
        self.rotation_notify = False
        self.rotation_notify_timer = 0
        self.rotation_notify_duration = 2000

        # how much to rotate the clock face
        self.rotation_offset = 0

    def update(self, _):
        """Update."""
        self.scan_buttons()

        # check if we've rotation-notified for long enough
        if ticks_ms() - self.rotation_notify_timer > self.rotation_notify_duration:
            self.rotation_notify = False

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

        self.overlays.append(Background())

        self.draw_markers()
        self.light_leds()

        hours, minutes, seconds = localtime()[3:6]

        self.hour_hand(hours, minutes, seconds)
        self.minute_hand(minutes, seconds)
        self.second_hand(seconds)

        self.draw_overlays(ctx)

    def second_hand(self, seconds):
        """Draw the second hand."""
        self.draw_hand("second", seconds * 6)

    def minute_hand(self, minutes, seconds):
        """Draw the minute hand."""
        self.draw_hand("minute", ((minutes * 60) + seconds) / 10)

    def hour_hand(self, hours, minutes, seconds):
        """Draw the minute hand."""
        self.draw_hand("hour", ((hours * 3600) + (minutes * 60) + seconds) / 120)

    def draw_hand(self, key, rotation):
        """Draw a hand."""
        rotation = rotation - self.rotation_offset
        coords = {
            "start": (
                sin(radians(rotation)) * -self.overhang,
                cos(radians(rotation)) * self.overhang,
            ),
            "end": (
                sin(radians(rotation)) * conf["hands"][key]["length"],
                cos(radians(rotation)) * -conf["hands"][key]["length"],
            ),
        }

        colour = rgb_from_degrees(self.colour_offset % 360)
        if self.full_spectrum:
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
            if self.full_spectrum:
                colour = rgb_from_degrees((rotation + self.colour_offset) % 360)

            size = self.marker_size
            filled = self.fill_markers

            if self.rotation_notify and angle == 180:  # noqa: PLR2004
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
            if self.full_spectrum:
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
        self.fill_markers = not self.fill_markers

    def invert_full_spectrum(self):
        """Invert full-spectrum."""
        self.full_spectrum = not self.full_spectrum

    def increment_shapes_index(self):
        """Increment shapes-index."""
        self.shapes_index = (self.shapes_index + 1) % len(shapes)

    def invert_clockwise_colour_rotation(self):
        """Invert clockwise colour-rotation."""
        self.rotate_colours_clockwise = not self.rotate_colours_clockwise

    def rotate_clock_face(self):
        """Rotate the clock face."""
        self.rotation_offset = (self.rotation_offset - 30) % 360
        self.rotation_notify = True
        self.rotation_notify_timer = ticks_ms()

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


__app_export__ = Clock

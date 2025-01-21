import json
from math import cos, radians, sin
from time import localtime

import ntptime
from events.input import BUTTON_TYPES, Buttons
from system.eventbus import eventbus
from system.patterndisplay.events import PatternDisable
from tildagonos import tildagonos

import app

from .lib.asset_path import ASSET_PATH
from .lib.gamma import gamma_corrections
from .lib.rgb_from_rotation import rgb_from_degrees
from .lib.shapes.circle import Circle
from .lib.shapes.hexagon import Hexagon
from .lib.shapes.line import Line
from .lib.shapes.triangle import Triangle

with open(ASSET_PATH + "conf.json") as j:  # noqa: PTH123
    conf = json.loads(j.read())


class Clock(app.App):
    """Clock."""

    def __init__(self):
        """Construct."""
        eventbus.emit(PatternDisable())
        ntptime.settime()
        self.background_colour = conf["background-colour"]
        self.overhang = conf["hands-overhang"]
        self.blob_radius = conf["blob-radius"]
        self.fill_blobs = conf["filled-blobs"]
        self.add_hand_ends = conf["add-hand-ends"]
        self.full_spectrum = conf["full-spectrum"]
        self.hands = conf["hands"]
        self.shapes = conf["shapes"]

        self.button_states = Buttons(self)
        self.top = 0
        self.radius = 118
        self.blob_offset = self.radius - self.blob_radius - 1
        self.colour_offset = 0
        self.colour_increment = 1
        self.led_brightness = 0.5

        self.rotation_offset = 0

    def update(self, _):
        """Update."""
        if self.button_states.get(BUTTON_TYPES["CANCEL"]):
            self.button_states.clear()
            self.minimise()

        if self.button_states.get(BUTTON_TYPES["CONFIRM"]):
            self.button_states.clear()
            self.fill_blobs = not self.fill_blobs

        if self.button_states.get(BUTTON_TYPES["RIGHT"]):
            self.button_states.clear()
            self.add_hand_ends = not self.add_hand_ends

        if self.button_states.get(BUTTON_TYPES["DOWN"]):
            self.button_states.clear()
            self.full_spectrum = not self.full_spectrum

        if self.button_states.get(BUTTON_TYPES["UP"]):
            self.button_states.clear()
            self.shapes = rotate(self.shapes)

        if self.button_states.get(BUTTON_TYPES["LEFT"]):
            self.button_states.clear()
            self.rotation_offset = (self.rotation_offset + 90) % 360

    def draw(self, ctx):
        """Draw."""
        self.fill_screen(ctx, self.background_colour)

        self.overlays = []

        ctx.image(ASSET_PATH + "background.png", -120, -120, 240, 240)

        self.draw_blobs()
        self.light_leds()

        now = localtime()

        hours = now[3]
        minutes = now[4]
        seconds = now[5]

        self.hour_hand(hours, minutes, seconds)
        self.minute_hand(minutes, seconds)
        self.second_hand(seconds)

        self.draw_overlays(ctx)
        tildagonos.leds.write()

        self.colour_offset = (self.colour_offset - self.colour_increment) % 360

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
        rotation = rotation + self.rotation_offset
        coords = {
            "start": (
                sin(radians(rotation)) * -self.overhang,
                cos(radians(rotation)) * self.overhang,
            ),
            "end": (
                sin(radians(rotation)) * self.hands[key]["length"],
                cos(radians(rotation)) * -self.hands[key]["length"],
            ),
        }

        colour = rgb_from_degrees(self.colour_offset % 360)
        if self.full_spectrum:
            colour = rgb_from_degrees((180 - rotation + self.colour_offset) % 360)

        self.overlays.append(
            Line(
                start=(coords["start"]),
                end=coords["end"],
                width=self.hands[key]["width"],
                colour=colour,
                opacity=0.8,
            )
        )

        if self.add_hand_ends:
            if self.shapes[0] == "hexagons":
                self.overlays.append(
                    Hexagon(
                        centre=coords["end"],
                        radius=self.hands[key]["end-radius"],
                        colour=colour,
                        rotation=radians(rotation),
                        filled=True,
                        opacity=1.0,
                    )
                )
            elif self.shapes[0] == "triangles":
                self.overlays.append(
                    Triangle(
                        centre=coords["end"],
                        height=self.blob_radius * 2,
                        base=self.blob_radius * 2,
                        colour=colour,
                        rotation=radians(rotation),
                        filled=True,
                        opacity=1.0,
                    )
                )
            else:
                self.overlays.append(
                    Circle(
                        radius=self.hands[key]["end-radius"],
                        centre=coords["end"],
                        colour=colour,
                        filled=True,
                        opacity=1.0,
                    )
                )

    def fill_screen(self, ctx, rgb):
        """Fill the screen."""
        ctx.rgb(*rgb).rectangle(-120, -120, 240, 240).fill()

    def draw_blobs(self):
        """Draw the number-ish bits."""
        for angle in range(0, 360, 30):
            rotation = angle + self.rotation_offset
            pair = (
                sin(radians(rotation)) * self.blob_offset,
                cos(radians(rotation)) * self.blob_offset,
            )

            colour = rgb_from_degrees(self.colour_offset % 360)
            if self.full_spectrum:
                colour = rgb_from_degrees((rotation + self.colour_offset) % 360)

            if self.shapes[0] == "hexagons":
                self.overlays.append(
                    Hexagon(
                        centre=pair,
                        radius=self.blob_radius,
                        colour=colour,
                        rotation=radians(-rotation),
                        filled=self.fill_blobs,
                    )
                )

            elif self.shapes[0] == "triangles":
                self.overlays.append(
                    Triangle(
                        centre=pair,
                        base=self.blob_radius * 2,
                        colour=colour,
                        rotation=radians(-rotation),
                        filled=self.fill_blobs,
                    )
                )

            else:
                self.overlays.append(
                    Circle(
                        radius=self.blob_radius,
                        centre=pair,
                        colour=colour,
                        filled=self.fill_blobs,
                        opacity=1.0,
                    )
                )

    def light_leds(self):
        """Light the lights."""
        for i in range(12):
            colour = rgb_from_degrees(self.colour_offset % 360)
            if self.full_spectrum:
                colour = rgb_from_degrees(
                    ((i * 30) + 15 + 180 + self.colour_offset) % 360
                )
            tildagonos.leds[12 - i] = [
                gamma_corrections[int(c * 255 * self.led_brightness)] for c in colour
            ]


def rotate(array):
    """Rotate a list."""
    return array[1:] + [array[0]]


__app_export__ = Clock

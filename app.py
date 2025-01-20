from math import cos, radians, sin
from time import localtime

import ntptime
from events.input import BUTTON_TYPES, Buttons
from system.eventbus import eventbus
from system.patterndisplay.events import PatternDisable
from tildagonos import tildagonos

import app

from .lib.circle import Circle
from .lib.gamma import gamma_corrections
from .lib.line import Line
from .lib.rgb_from_hue import rgb_from_degrees

g = 9.806


class Clock(app.App):
    """Clock."""

    def __init__(self):
        """Construct."""
        eventbus.emit(PatternDisable())
        ntptime.settime()
        self.button_states = Buttons(self)
        self.top = 0
        self.radius = 120
        self.blob_radius = 10
        self.blob_offset = self.radius - self.blob_radius - 1
        self.colour_offset = 0
        self.colour_increment = 1
        self.led_brightness = 0.5
        self.overhang = 20

        self.fill_blobs = True

        self.hands = {
            "hour": {
                "distance": 40,
                "blob-size": 8,
                "width": 8,
            },
            "minute": {
                "distance": 70,
                "blob-size": 8,
                "width": 4,
            },
            "second": {
                "distance": 80,
                "blob-size": 8,
                "width": 2,
            },
        }

    def update(self, _):
        """Update."""
        if self.button_states.get(BUTTON_TYPES["CANCEL"]):
            self.button_states.clear()
            self.minimise()

        if self.button_states.get(BUTTON_TYPES["CONFIRM"]):
            self.button_states.clear()
            self.fill_blobs = not self.fill_blobs

    def draw(self, ctx):
        """Draw."""
        self.fill_screen(ctx, (0, 0, 0))

        self.overlays = []

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

        self.colour_offset = (self.colour_offset + self.colour_increment) % 360

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
        coords = {
            "start": (
                sin(radians(rotation)) * -self.overhang,
                cos(radians(rotation)) * self.overhang,
            ),
            "end": (
                sin(radians(rotation)) * self.hands[key]["distance"],
                cos(radians(rotation)) * -self.hands[key]["distance"],
            ),
        }

        colour = rgb_from_degrees((180 - rotation + self.colour_offset) % 360)

        self.overlays.append(
            Line(
                start=(coords["start"]),
                end=coords["end"],
                width=self.hands[key]["width"],
                colour=colour,
            )
        )

    def fill_screen(self, ctx, rgb):
        """Fill the screen."""
        ctx.rgb(*rgb).rectangle(-120, -120, 240, 240).fill()

    def draw_blobs(self):
        """Draw the number-ish bits."""
        for i in range(0, 360, 30):
            pair = (
                sin(radians(i)) * self.blob_offset,
                cos(radians(i)) * self.blob_offset,
            )
            self.overlays.append(
                Circle(
                    radius=self.blob_radius,
                    centre=pair,
                    colour=rgb_from_degrees((i + self.colour_offset) % 360),
                    filled=self.fill_blobs,
                )
            )

    def light_leds(self):
        """Light the lights."""
        for i in range(12):
            tildagonos.leds[12 - i] = [
                gamma_corrections[int(c * 255 * self.led_brightness)]
                for c in rgb_from_degrees(
                    ((i * 30) + 15 + 180 + self.colour_offset) % 360
                )
            ]


__app_export__ = Clock

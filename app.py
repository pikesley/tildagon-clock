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
        self.blob_radius = 6
        self.blob_offset = self.radius - self.blob_radius - 1
        self.colour_offset = 0
        self.colour_increment = 1
        self.led_brightness = 0.5
        self.hands_extra = 30

        self.hands = {
            "hour": {
                "distance": 40,
                "blob-size": 8,
            },
            "minute": {
                "distance": 70,
                "blob-size": 8,
            },
            "second": {
                "distance": 80,
                "blob-size": 8,
            },
        }

    def update(self, _):
        """Update."""
        if self.button_states.get(BUTTON_TYPES["CANCEL"]):
            self.button_states.clear()
            self.minimise()

    def draw(self, ctx):
        """Draw."""
        self.fill_screen(ctx, (0, 0, 0))

        self.overlays = []

        self.draw_blobs()
        self.light_leds()

        now = localtime()

        # now = (2025, 1, 20, 18, 15, 32, 0, 20)

        hours = now[3]
        minutes = now[4]
        seconds = now[5]

        self.hour_hand(ctx, hours, minutes, seconds)
        self.minute_hand(ctx, minutes, seconds)
        self.second_hand(ctx, seconds)

        self.draw_overlays(ctx)
        tildagonos.leds.write()

        self.colour_offset = (self.colour_offset + self.colour_increment) % 360

    def second_hand(self, ctx, seconds):
        """Draw the second hand."""
        self.draw_hand(ctx, "second", seconds * 6)

    def minute_hand(self, ctx, minutes, seconds):
        """Draw the minute hand."""
        self.draw_hand(ctx, "minute", ((minutes * 60) + seconds) / 10)

    def hour_hand(self, ctx, hours, minutes, seconds):
        """Draw the minute hand."""
        self.draw_hand(ctx, "hour", ((hours * 3600) + (minutes * 60) + seconds) / 120)

    def draw_hand(self, ctx, key, amount):
        """Draw a hand."""
        x = sin(radians(amount)) * self.hands[key]["distance"]
        y = cos(radians(amount)) * -self.hands[key]["distance"]
        colour = rgb_from_degrees((180 - amount + self.colour_offset) % 360)

        self.overlays.append(
            Circle(
                radius=self.hands[key]["blob-size"],
                centre=(x, y),
                colour=colour,
                filled=True,
            )
        )

        ctx.rgb(*colour)
        ctx.move_to(0, 0)
        ctx.line_to(x, y)
        ctx.stroke()

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

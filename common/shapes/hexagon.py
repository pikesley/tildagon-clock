from math import sqrt

from .shape import Shape


class Hexagon(Shape):
    """A hexagon."""

    def draw_lines(self, ctx):
        """Draw ourself."""
        ctx.move_to(0 - self.size, 0)
        ctx.line_to((0 - self.size) / 2, (self.size * sqrt(3)) / 2)
        ctx.line_to(self.size / 2, (self.size * sqrt(3)) / 2)
        ctx.line_to(self.size, 0)
        ctx.line_to(self.size / 2, (-self.size * sqrt(3)) / 2)
        ctx.line_to((0 - self.size) / 2, (-self.size * sqrt(3)) / 2)

        ctx.close_path()

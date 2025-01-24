from math import sqrt

from .shape import Shape


class Hexagon(Shape):
    """A hexagon."""

    def draw(self, ctx):
        """Draw ourself."""
        ctx.rgba(*self.colour).begin_path()
        ctx.translate(*self.centre)
        ctx.rotate(self.rotation)

        ctx.move_to(0 - self.size, 0)
        ctx.line_to((0 - self.size) / 2, (self.size * sqrt(3)) / 2)
        ctx.line_to(self.size / 2, (self.size * sqrt(3)) / 2)
        ctx.line_to(self.size, 0)
        ctx.line_to(self.size / 2, (-self.size * sqrt(3)) / 2)
        ctx.line_to((0 - self.size) / 2, (-self.size * sqrt(3)) / 2)

        ctx.close_path()

        self.finalise(ctx)

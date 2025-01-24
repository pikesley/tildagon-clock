import math

from .shape import Shape


class Circle(Shape):
    """A circle."""

    def draw(self, ctx):
        """Draw ourself."""
        self.x, self.y = self.centre
        ctx.rgba(*self.colour)
        ctx.arc(
            self.x,
            self.y,
            self.size,
            0,
            2 * math.pi,
            True,  # noqa: FBT003
        )

        self.finalise(ctx)

import math


class Circle:
    """A circle."""

    def __init__(self, radius=0, centre=(0, 0), colour=(255, 0, 0), filled=False):  # noqa: FBT002
        """Construct."""
        self.x, self.y = centre
        self.radius = radius
        self.colour = colour
        self.filled = filled

    def draw(self, ctx):
        """Draw ourself."""
        entity = ctx.rgb(*self.colour).arc(
            self.x,
            self.y,
            self.radius,
            0,
            2 * math.pi,
            True,  # noqa: FBT003
        )

        if self.filled:
            entity.fill()
        else:
            entity.stroke()

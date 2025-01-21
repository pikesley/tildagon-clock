import math


class Circle:
    """A circle."""

    def __init__(
        self,
        radius=0,
        centre=(0, 0),
        colour=(255, 0, 0),
        opacity=0.7,
        filled=False,  # noqa: FBT002
    ):
        """Construct."""
        self.x, self.y = centre
        self.radius = radius
        self.colour = list(colour) + [opacity]  # noqa: RUF005
        self.filled = filled

    def draw(self, ctx):
        """Draw ourself."""
        entity = ctx.rgba(*self.colour).arc(
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

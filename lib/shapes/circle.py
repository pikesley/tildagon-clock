import math


class Circle:
    """A circle."""

    def __init__(  # noqa: PLR0913
        self,
        centre=(0, 0),
        size=10,
        rotation=0,
        colour=(255, 0, 0),
        opacity=0.7,
        filled=True,  # noqa: FBT002
    ):
        """Construct."""
        self.x, self.y = centre
        self.size = size
        self.colour = list(colour) + [opacity]  # noqa: RUF005
        self.filled = filled
        self.rotation = rotation

    def draw(self, ctx):
        """Draw ourself."""
        ctx.rgba(*self.colour)
        ctx.arc(
            self.x,
            self.y,
            self.size,
            0,
            2 * math.pi,
            True,  # noqa: FBT003
        )

        if self.filled:
            ctx.fill()
        else:
            ctx.stroke()

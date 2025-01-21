from math import sqrt


class Hexagon:
    """A hexagon."""

    def __init__(  # noqa: PLR0913
        self,
        centre=(0, 0),
        radius=10,
        rotation=0,
        colour=(255, 0, 0),
        opacity=0.7,
        filled=True,  # noqa: FBT002
    ):
        """Construct."""
        self.centre = centre
        self.radius = radius
        self.rotation = rotation
        self.colour = list(colour) + [opacity]  # noqa: RUF005
        self.filled = filled

    def draw(self, ctx):
        """Draw ourself."""
        ctx.rgba(*self.colour).begin_path()
        ctx.translate(*self.centre)
        ctx.rotate(self.rotation)

        ctx.move_to(0 - self.radius, 0)
        ctx.line_to((0 - self.radius) / 2, (self.radius * sqrt(3)) / 2)
        ctx.line_to(self.radius / 2, (self.radius * sqrt(3)) / 2)
        ctx.line_to(self.radius, 0)
        ctx.line_to(self.radius / 2, (-self.radius * sqrt(3)) / 2)
        ctx.line_to((0 - self.radius) / 2, (-self.radius * sqrt(3)) / 2)

        ctx.close_path()

        if self.filled:
            ctx.fill()
        else:
            ctx.stroke()

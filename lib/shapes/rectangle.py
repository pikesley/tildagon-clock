class Rectangle:
    """A rectangle."""

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
        self.centre = centre
        self.size = size
        self.rotation = rotation
        self.colour = list(colour) + [opacity]  # noqa: RUF005
        self.filled = filled

        self.width = 4

    def draw(self, ctx):
        """Draw ourself."""
        max_y = 0 - self.size / 2
        min_y = 0 + self.size / 2

        max_x = 0 + (self.width / 2)
        min_x = 0 - (self.width / 2)

        ctx.rgba(*self.colour).begin_path()
        ctx.translate(*self.centre)
        ctx.rotate(self.rotation)

        ctx.move_to(min_x, max_y)
        ctx.line_to(min_x, min_y)
        ctx.line_to(max_x, min_y)
        ctx.line_to(max_x, max_y)

        ctx.close_path()

        if self.filled:
            ctx.fill()
        else:
            ctx.stroke()

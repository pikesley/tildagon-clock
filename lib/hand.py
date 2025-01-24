from math import radians


class Hand:
    """The hand of a clock."""

    def __init__(  # noqa: PLR0913
        self,
        colour=(255, 0, 0),
        filled=True,  # noqa: FBT002
        opacity=0.7,
        principal_length=70,
        rotation=0,
        tail_length=10,
        taper_factor=0.6,
        width=10,
    ):
        """Construct."""
        self.principal_length = principal_length
        self.tail_length = tail_length
        self.width = width / 2
        self.colour = list(colour) + [opacity]  # noqa: RUF005
        self.rotation = radians(rotation)
        self.filled = filled
        self.taper_factor=taper_factor

    def draw(self, ctx):
        """Draw ourself."""
        ctx.rgba(*self.colour).begin_path()
        ctx.translate(0, 0)
        ctx.rotate(self.rotation)

        ctx.move_to(0 - (self.width * self.taper_factor), 0 - self.principal_length)
        ctx.line_to(self.width * self.taper_factor, 0 - self.principal_length)
        ctx.line_to(self.width, self.tail_length)
        ctx.line_to(0 - self.width, self.tail_length)

        ctx.close_path()

        if self.filled:
            ctx.fill()
        else:
            ctx.stroke()

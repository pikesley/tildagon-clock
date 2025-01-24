class Hand:
    """The hand of a clock."""

    def __init__(  # noqa: PLR0913
        self,
        principal_length=70,
        tail_length=10,
        width=10,
        colour=(255, 0, 0),
        opacity=0.7,
        rotation=0,
        filled=True,  # noqa: FBT002
    ):
        """Construct."""
        self.principal_length = principal_length
        self.tail_length = tail_length
        self.width = width / 2
        self.colour = list(colour) + [opacity]  # noqa: RUF005
        self.rotation = rotation
        self.filled = filled

    def draw(self, ctx):
        """Draw ourself."""
        ctx.rgba(*self.colour).begin_path()
        ctx.translate(0, 0)
        ctx.rotate(self.rotation)



        ctx.move_to(0 - self.width, 0 - self.principal_length)
        ctx.line_to(self.width, 0 - self.principal_length)
        ctx.line_to(self.width, self.tail_length)
        ctx.line_to(0-self.width, self.tail_length)

        ctx.close_path()

        if self.filled:
            ctx.fill()
        else:
            ctx.stroke()

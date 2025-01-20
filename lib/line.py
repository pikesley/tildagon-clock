class Line:
    """A live."""

    def __init__(
        self, start=(0, 0), end=(0, 0), width=1, colour=(255, 0, 0), opacity=0.7
    ):
        """Construct."""
        self.start = start
        self.end = end
        self.width = width
        self.colour = colour + [opacity]  # noqa: RUF005

    def draw(self, ctx):
        """Draw ourself."""
        ctx.rgba(*self.colour)
        ctx.line_width = self.width
        ctx.move_to(*self.start)
        ctx.line_to(*self.end)
        ctx.stroke()

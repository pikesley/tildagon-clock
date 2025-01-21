class EMF:
    """Letters."""

    def __init__(
        self, centre=(0, 0), scale=10.0, colour=(255, 0, 0), opacity=1.0, line_width=3
    ):
        """Construct."""
        self.centre = centre
        self.scale = scale
        self.colour = list(colour) + [opacity]  # noqa: RUF005
        self.line_width = line_width

    def draw(self, ctx):
        """Draw ourself."""
        ctx.rgba(*self.colour).begin_path()
        ctx.line_width = self.line_width
        ctx.translate(*self.centre)

        # E
        ctx.move_to(-1.5 * self.scale, -1 * self.scale)
        ctx.line_to(-3.5 * self.scale, -1 * self.scale)
        ctx.line_to(-3.5 * self.scale, 1 * self.scale)
        ctx.line_to(-1.5 * self.scale, 1 * self.scale)
        ctx.move_to(-3.5 * self.scale, 0)
        ctx.line_to(-2 * self.scale, 0)

        # M
        ctx.move_to(-1 * self.scale, 1 * self.scale)
        ctx.line_to(-1 * self.scale, -1 * self.scale)
        ctx.line_to(0, 0)
        ctx.line_to(1 * self.scale, -1 * self.scale)
        ctx.line_to(1 * self.scale, 1 * self.scale)

        # F
        ctx.move_to(3.5 * self.scale, -1 * self.scale)
        ctx.line_to(1.5 * self.scale, -1 * self.scale)
        ctx.line_to(1.5 * self.scale, 1 * self.scale)
        ctx.move_to(1.5 * self.scale, 0)
        ctx.line_to(3 * self.scale, 0)

        ctx.stroke()

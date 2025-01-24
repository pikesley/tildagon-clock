class Shape:
    """A shape."""

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

    def finalise(self, ctx):
        """Finish drawing."""
        if self.filled:
            ctx.fill()
        else:
            ctx.stroke()

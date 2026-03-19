from math import radians


class Shape:
    """A shape."""

    def __init__(  # noqa: PLR0913
        self,
        centre=(0, 0),
        colour=(255, 0, 0),
        filled=True,  # noqa: FBT002
        opacity=0.7,
        rotation=0,
        size=10,
    ):
        """Construct."""
        self.centre = centre
        self.size = size
        self.rotation = radians(rotation)
        self.colour = list(colour) + [opacity]
        self.filled = filled

    def position(self, ctx):
        """Get in position."""
        if self.__class__.__name__ not in ["Circle"]:
            ctx.translate(*self.centre)
            ctx.rotate(self.rotation)

    def set_colour(self, ctx):
        """Set our colour."""
        ctx.rgba(*self.colour).begin_path()

    def close_shape(self, ctx):
        """Close the shape."""
        if self.__class__.__name__ not in ["Circle"]:
            ctx.close_path()

    def finalise(self, ctx):
        """Finish drawing."""
        if self.filled:
            ctx.fill()
        else:
            ctx.stroke()

    def draw(self, ctx):
        """Actual drawing steps."""
        self.position(ctx)
        self.set_colour(ctx)

        self.draw_lines(ctx)

        self.close_shape(ctx)
        self.finalise(ctx)

from math import sqrt


class Triangle:
    """A triangle."""

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

    def draw(self, ctx):
        """Draw ourself."""
        y_offset = sqrt(3) * (self.size / 2)
        max_y = 0 - y_offset
        min_y = 0 + y_offset

        max_x = 0 + (self.size)
        min_x = 0 - (self.size)

        apex = (0, max_y)
        left_vertex = (min_x, min_y)
        right_vertex = (max_x, min_y)

        ctx.rgba(*self.colour).begin_path()
        ctx.translate(*self.centre)
        ctx.rotate(self.rotation)
        ctx.move_to(*apex)
        ctx.line_to(*left_vertex)
        ctx.line_to(*right_vertex)
        ctx.close_path()

        if self.filled:
            ctx.fill()
        else:
            ctx.stroke()

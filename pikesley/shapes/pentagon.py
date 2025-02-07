from .shape import Shape


class Pentagon(Shape):
    """A pentagon."""

    def draw_lines(self, ctx):
        """Draw ourself."""
        ctx.move_to(0, self.size)  # top
        ctx.line_to(self.size * 0.8090, self.size * 0.4125)  # upper-right
        ctx.line_to(self.size * 0.5, -self.size * 0.5388)  # lower-right
        ctx.line_to(-self.size * 0.5, -self.size * 0.5388)  # lower-left
        ctx.line_to(-self.size * 0.8090, self.size * 0.4125)  # upper-left

        ctx.close_path()

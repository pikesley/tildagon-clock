from .shape import Shape


class Square(Shape):
    """A square."""

    def draw_lines(self, ctx):
        """Draw ourself."""
        ctx.move_to(self.size, -self.size)
        ctx.line_to(self.size, self.size)
        ctx.line_to(-self.size, self.size)
        ctx.line_to(-self.size, -self.size)

        ctx.close_path()

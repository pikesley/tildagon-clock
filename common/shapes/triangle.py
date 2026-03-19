from math import sqrt

from .shape import Shape


class Triangle(Shape):
    """A triangle."""

    def draw_lines(self, ctx):
        """Draw ourself."""
        y_offset = sqrt(3) * (self.size / 2)
        max_y = 0 - y_offset
        min_y = 0 + y_offset

        max_x = 0 + (self.size)
        min_x = 0 - (self.size)

        apex = (0, max_y)
        left_vertex = (min_x, min_y)
        right_vertex = (max_x, min_y)
        ctx.move_to(*apex)
        ctx.line_to(*left_vertex)
        ctx.line_to(*right_vertex)

        ctx.close_path()

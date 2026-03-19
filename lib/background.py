from ..common.asset_path import asset_path


class Background:
    """Background."""

    def __init__(
        self,
        colour=(0, 0, 0),
        image="emf.png",
        opacity=0.6,
    ):
        """Construct."""
        self.image = image
        self.colour = list(colour) + [opacity]

    def draw(self, ctx):
        """Draw ourself."""
        ctx.image(asset_path("clock") + self.image, -120, -120, 240, 240)
        ctx.rgba(*self.colour).rectangle(-120, -120, 240, 240).fill()

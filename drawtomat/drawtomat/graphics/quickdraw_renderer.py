from drawtomat.graphics.quickdraw_composer import QuickDrawComposer
from drawtomat.quickdraw.quickdraw_dataset import QuickDrawDataset


class QuickDrawRenderer:
    """
    An image renderer based on "Quick, Draw!" data.
    """

    def __init__(self):
        self.dataset = QuickDrawDataset.words()
        self.composer = QuickDrawComposer()

    def render(self, scene: 'Scene', file: None) -> None:
        """
        Renders a scene into an image.

        Parameters
        ----------
        file
        scene
            The scene to render.

        Returns
        -------
        None
        """


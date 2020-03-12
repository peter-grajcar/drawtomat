from drawtomat.quickdraw.quickdraw_dataset import QuickDrawDataset


class QuickDrawComposer:
    """
    A scene composer based on "Quick, Draw!" data.
    """

    def __init__(self):
        self.dataset = QuickDrawDataset.words()

    def compose(self, scene: 'Scene') -> list:
        """
        Composes object from the scene into a list of strokes.

        Parameters
        ----------
        scene

        Returns
        -------

        """
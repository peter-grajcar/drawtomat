import ndjson


class QuickDrawDataset:
    """
    Tris class provides data from the Google's "Quick, Draw!" dataset.
    """
    _words = None
    _images = None

    @staticmethod
    def words() -> list:
        """
        Returns a list of words present in the Quick, Draw! dataset.

        Returns
        -------
        list
            A list of words available in the dataset.
        """
        if not QuickDrawDataset._words:
            QuickDrawDataset._words = list()
            with open("../resources/quickdraw/categories.txt") as f:
                for word in f.readlines():
                    QuickDrawDataset._words.append(word.strip())

        return QuickDrawDataset._words

    @staticmethod
    def images():
        """
        Returns a dictionary of data for each word.

        Returns
        -------
        dict

        """
        if not QuickDrawDataset._images:
            QuickDrawDataset._images = dict()
            for word in QuickDrawDataset.words():
                with open(f"../resources/quickdraw/dataset/{word}.ndjson") as f:
                    QuickDrawDataset._images[word] = ndjson.loads(f.readlines())
        return QuickDrawDataset._images

    @staticmethod
    def images(word: str) -> dict:
        """
        Returns data for a single word.

        Parameters
        ----------
        word : str

        Returns
        -------
        dict

        """
        return QuickDrawDataset.images()[word]

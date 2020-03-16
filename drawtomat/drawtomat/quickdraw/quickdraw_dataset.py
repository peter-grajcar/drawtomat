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
    def images(word: str = None):
        """
        Returns a dictionary of data for each word.

        Returns
        -------
        dict

        """
        if not QuickDrawDataset._images:
            QuickDrawDataset._images = dict()
            for w in QuickDrawDataset.words():
                with open(f"../resources/quickdraw/dataset/{w}.ndjson") as f:
                    QuickDrawDataset._images[w] = ndjson.load(f)
        if word:
            return QuickDrawDataset.images()[word]
        return QuickDrawDataset._images


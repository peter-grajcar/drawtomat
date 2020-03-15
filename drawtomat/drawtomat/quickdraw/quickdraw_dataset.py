import ndjson


class QuickDrawDataset:
    """
    Tris class provides data from the Google's "Quick, Draw!" dataset.
    """
    _words = None
    _images = None

    @staticmethod
    def words():
        if not QuickDrawDataset._words:
            QuickDrawDataset._words = []
            with open("../resources/quickdraw/categories.txt") as f:
                for word in f.readlines():
                    QuickDrawDataset._words.append(word.strip())

        return QuickDrawDataset._words

    @staticmethod
    def images():
        if not QuickDrawDataset._images:
            QuickDrawDataset._images = dict()
            for word in QuickDrawDataset.words():
                with open(f"../resources/quickdraw/dataset/{word}.ndjson") as f:
                    QuickDrawDataset._images[word] = ndjson.loads(f.readlines())
        return QuickDrawDataset._images

import ndjson


class QuickDrawDataset:
    """
    This class provides data from the Google's "Quick, Draw!" dataset.
    Drawtomat uses Google's Quick, Draw! dataset which consists of 345 drawing
    categories. The dataset contains more than 50 million drawings, however,
    only a selected portion of drawings is used in Drawtomat as the dataset
    also contains irrelevant and inappropriate content.

    The categories and selected drawings can be found in `resources/quickdraw`
    directory.The Quick, Draw! data are extended with attributes, which at the
    moment contain default object sizes (in centimetres). These data are used
    for scaling the objects to preserve natural proportions. Attribute data can
    be found in `resources/quickdraw/attributes.csv` and
    `resources/quickdraw/attributes_relative.csv`. If one of the default
    dimensions is omitted then only the defined dimension is used for scaling.
    If both default dimensions are defined then the drawing is scaled by the
    major dimension.
    """
    _words = None
    _images = None

    @staticmethod
    def words() -> 'list':
        """
        Returns a list of words present in the Quick, Draw! dataset.

        Returns
        -------
        list
            A list of words available in the dataset.
        """
        if not QuickDrawDataset._words:
            QuickDrawDataset._words = list()
            with open("resources/quickdraw/categories.txt") as f:
                for word in f.readlines():
                    QuickDrawDataset._words.append(word.strip())

        return QuickDrawDataset._words

    @staticmethod
    def images(word: 'str' = None) -> 'dict':
        """
        Returns a dictionary of data for each word.

        Returns
        -------
        dict

        """
        if not QuickDrawDataset._images:
            QuickDrawDataset._images = dict()
            for w in QuickDrawDataset.words():
                with open(f"resources/quickdraw/dataset/{w}.ndjson") as f:
                    QuickDrawDataset._images[w] = ndjson.load(f)
        if word:
            return QuickDrawDataset._images[word]
        return QuickDrawDataset._images

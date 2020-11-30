import logging
from typing import List

import regex as re

bases = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19,
    "twenty": 20,
    "thirty": 30,
    "forty": 40,
    "fifty": 50,
    "sixty": 60,
    "seventy": 70,
    "eighty": 80,
    "ninety": 90
}

multiples = {
    "hundred": 100,
    "thousand": 1000,
    "million": 1_000_000,
    "billion": 1_000_000_000
}

connectives = [
    "and", "-", ","
]


def is_numeric(word: 'str') -> 'bool':
    """
    Returns true if the word is a numeral.

    Parameters
    ----------
    word: str

    Returns
    -------
    bool

    """
    return word in bases or word in multiples


def words2int(num_by_words: 'str') -> 'int':
    """
    Converts number represented as words, i.e. 'ten', 'twenty-five', ...; to
    its integer value.

    Parameters
    ----------
    num_by_words: str
        Number represented by words

    Returns
    -------
    int
        Integer value of a given number
    """

    result = 0

    idx = 0
    words = num_by_words.split()
    word_count = len(words)
    while idx < word_count:
        n = bases.get(words[idx])
        if n is not None:
            mul = multiples.get(words[idx + 1]) if idx + 1 < word_count else None
            if mul is not None:
                result += n * mul
                idx += 2
                continue
            else:
                result += n
                idx += 1
                continue

        n = multiples.get(words[idx])
        if n is not None:
            result += n
            idx += 1
            continue

        if words[idx] in connectives:
            idx += 1
            continue

        logging.error(f"{words[idx]} is not a number")
        idx += 1

    return result


def tokenize(text: 'str') -> 'List[str]':
    result = re.sub(r"(\p{P})", r" \1 ", text)
    return result.split()


def replace_with_numbers(text: 'str') -> 'str':
    """

    Parameters
    ----------
    text : str

    Returns
    -------
    str

    """
    words = tokenize(text)
    word_count = len(words)
    result = []

    def is_part_of_num(w): return is_numeric(w) or w in connectives

    number = False
    start = 0
    idx = 0
    while idx < word_count:
        if is_numeric(words[idx]) and not number:
            number = True
            start = idx
        elif number and not is_part_of_num(words[idx]):
            number = False
            num_by_words = " ".join(words[start:idx])
            result.append(str(words2int(num_by_words)))
            result.append(words[idx])
        elif not number:
            result.append(words[idx])

        idx += 1

    if number:
        num_by_words = " ".join(words[start:idx])
        result.append(str(words2int(num_by_words)))

    return " ".join(result)

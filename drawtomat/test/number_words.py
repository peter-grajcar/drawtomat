import drawtomat.processor.text2num as t2n

numbers = [
    "two",
    "sixty-six",
    "two hundred",
    "five thousand eight hundred and seven",
    "nineteen hundred and eighty five",
    "ten thousand and forty three",
]

for number in numbers:
    int_val = t2n.words2int(number)
    print(number, "=", int_val)

sentences = [
    "two dogs, and thirty-five cats stole ten million dollars."
]

for sentence in sentences:
    print(sentence, "->", t2n.replace_with_numbers(sentence))

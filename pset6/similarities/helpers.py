from nltk.tokenize import sent_tokenize


def lines(a, b):
    """Return lines in both a and b"""

    lines = set(a.split("\n")) & set(b.split("\n"))
    return lines


def sentences(a, b):
    """Return sentences in both a and b"""

    sentences = set(sent_tokenize(a)) & set(sent_tokenize(b))
    return sentences


def split(line, n):
    """Splits a string into a substring of given length"""
    split = []
    for i in range(len(line)-n+1):
        split.append(line[i:i+n])
    return split


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    substrings = set(split(a, n)) & set(split(b, n))
    return substrings

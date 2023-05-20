from utilities import timeit


@timeit
def spinning_words(words: str) -> str:
    separate_words = words.split()
    length = len(separate_words) - 1
    result = ""

    for index, word in enumerate(separate_words):
        if len(word) >= 5:
            word = word[::-1]

        result += word
        if index < length:
            result += " "

    return result


def spinning_words_one_liner(sentence: str) -> str:
    return " ".join(word if len(word) < 5 else word[::-1] for word in sentence.split())


def test_sppining_words():
    assert spinning_words("Hey fellow warriors") == "Hey wollef sroirraw"
    assert spinning_words("This is a test") == "This is a test"
    assert spinning_words("This is another test") == "This is rehtona test"

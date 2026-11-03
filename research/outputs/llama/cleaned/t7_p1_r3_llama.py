import re

def word_frequency(text):
    """
    Count how many times each word appears in the given text.

    Args:
        text (str): The input text.

    Returns:
        dict: A dictionary with words as keys and their frequencies as values.
    """
    words = re.findall('\\b\\w+\\b', text.lower())
    frequency = {word: words.count(word) for word in set(words)}
    return frequency
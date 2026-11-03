import re

def word_frequency(text):
    """
    Returns a dictionary with word frequencies in the given text.

    :param text: The input text.
    :return: A dictionary where keys are words and values are their frequencies.
    """
    text = re.sub('\\s+', ' ', text).lower()
    words = text.split()
    frequency = {}
    for word in words:
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] = 1
    return frequency
import re
from collections import Counter

def word_frequency(text):
    """
    Returns a dictionary of word frequencies, where the keys are words 
    (case-insensitive) and the values are their respective counts.

    Parameters:
    text (str): The input text for which we want to count word frequencies.

    Returns:
    dict: A dictionary with words as keys and their counts as values.
    """
    text = text.lower()
    words = re.findall('\\b\\w+\\b', text)
    frequency = Counter(words)
    return dict(frequency)
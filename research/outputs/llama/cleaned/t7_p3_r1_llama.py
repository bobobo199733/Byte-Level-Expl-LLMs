import re

def word_frequency(text):
    """
    Returns a dictionary where keys are unique words and values are their frequencies.
    
    :param text: The input string to be processed
    :return: A dictionary with word frequencies
    """
    words = re.findall('\\b\\w+\\b', text.lower())
    frequency = {}
    for word in words:
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] = 1
    return frequency
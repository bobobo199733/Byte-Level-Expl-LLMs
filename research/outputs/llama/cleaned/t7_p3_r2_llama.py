import re

def word_frequency(text):
    """
    Counts the occurrences of each word in a given text.
    
    Args:
        text (str): The input text
    
    Returns:
        dict: A dictionary where keys are unique words and values are their frequencies
    """
    text = re.sub('[^\\w\\s]', '', text.lower())
    words = text.split()
    frequency = {word: words.count(word) for word in set(words)}
    return frequency
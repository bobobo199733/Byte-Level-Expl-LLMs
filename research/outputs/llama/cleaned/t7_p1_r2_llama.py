import re
from collections import defaultdict

def word_frequency(text):
    """
    Counts the frequency of each word in the given text.
    
    Args:
        text (str): The input text to count word frequencies from.
    
    Returns:
        dict: A dictionary where keys are words and values are their respective frequencies.
    """
    text = text.lower()
    text = re.sub('[^\\w\\s]', '', text)
    words = text.split()
    frequency_dict = defaultdict(int)
    for word in words:
        frequency_dict[word] += 1
    return dict(frequency_dict)
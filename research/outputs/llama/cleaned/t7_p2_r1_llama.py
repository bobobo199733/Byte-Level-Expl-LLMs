import re

def word_frequency(text):
    """
    Calculate the frequency of each word in a given text.

    Args:
        text (str): The input text.

    Returns:
        dict: A dictionary where keys are unique words and values are their frequencies.
    """
    cleaned_text = re.sub('\\s+', ' ', text)
    words = cleaned_text.split()
    frequency_dict = {}
    for word in words:
        if word in frequency_dict:
            frequency_dict[word] += 1
        else:
            frequency_dict[word] = 1
    return frequency_dict
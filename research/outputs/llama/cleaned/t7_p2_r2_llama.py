def word_frequency(text):
    """
    Calculate the frequency of each word in a given text.

    Args:
        text (str): The input text.

    Returns:
        dict: A dictionary where keys are unique words and values are their frequencies.
    """
    words = text.split()
    freq_dict = {}
    for word in words:
        if word in freq_dict:
            freq_dict[word] += 1
        else:
            freq_dict[word] = 1
    return freq_dict
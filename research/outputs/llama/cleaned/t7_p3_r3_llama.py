def word_frequency(text):
    """
    This function takes a string as input and returns a dictionary with the frequency of each word.
    
    Args:
        text (str): The input string.

    Returns:
        dict: A dictionary where keys are unique words from the input string and values are their respective frequencies.
    """
    text = text.lower()
    text = ''.join((char if char.isalnum() else ' ' for char in text))
    words = text.split()
    frequency_dict = {}
    for word in words:
        if word not in frequency_dict:
            frequency_dict[word] = 1
        else:
            frequency_dict[word] += 1
    return frequency_dict
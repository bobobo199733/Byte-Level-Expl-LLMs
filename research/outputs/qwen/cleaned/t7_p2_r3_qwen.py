def word_frequency(text):
    words = text.split()
    frequency_dict = {}
    for word in words:
        lower_word = word.lower()
        if lower_word in frequency_dict:
            frequency_dict[lower_word] += 1
        else:
            frequency_dict[lower_word] = 1
    return frequency_dict
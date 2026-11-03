def word_frequency(text):
    frequency_dict = {}
    words = re.split('\\s+', text)
    for word in words:
        if word:
            frequency_dict[word] = frequency_dict.get(word, 0) + 1
    return frequency_dict
import re
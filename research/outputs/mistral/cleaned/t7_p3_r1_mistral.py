import re

def word_frequency(text):
    words = re.findall('\\w+', text)
    freq_dict = {}
    for word in words:
        if word in freq_dict:
            freq_dict[word] += 1
        else:
            freq_dict[word] = 1
    return freq_dict
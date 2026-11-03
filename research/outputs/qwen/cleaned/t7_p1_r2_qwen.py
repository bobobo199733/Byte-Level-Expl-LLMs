def word_frequency(text):
    text = text.lower()
    import re
    words = re.findall('\\b\\w+\\b', text)
    frequency_dict = {}
    for word in words:
        if word in frequency_dict:
            frequency_dict[word] += 1
        else:
            frequency_dict[word] = 1
    return frequency_dict
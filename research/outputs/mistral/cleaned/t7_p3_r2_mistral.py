def word_frequency(text):
    text = re.sub('[^\\w\\s]', '', text).lower()
    words = text.split()
    freq_dict = {}
    for word in set(words):
        if word in freq_dict:
            freq_dict[word] += 1
        else:
            freq_dict[word] = 1
    return freq_dict
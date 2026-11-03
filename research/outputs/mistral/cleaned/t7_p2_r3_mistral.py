def word_frequency(text):
    words = text.lower().split()
    freq_dict = {}
    for word in words:
        word = ''.join(filter(str.isalnum, word))
        if word:
            freq_dict[word] = freq_dict.get(word, 0) + 1
    return freq_dict
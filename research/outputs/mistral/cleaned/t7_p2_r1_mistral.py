def word_frequency(text):
    words = text.lower().split()
    freq_dict = {}
    for word in words:
        word = ''.join((c for c in word if c.isalnum()))
        if word:
            freq_dict[word] = freq_dict.get(word, 0) + 1
    return freq_dict
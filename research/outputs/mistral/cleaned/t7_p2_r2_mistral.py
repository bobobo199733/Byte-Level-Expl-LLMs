def word_frequency(text):
    words = text.strip().replace('  ', ' ').lower().split()
    freq_dict = {}
    for word in words:
        if word not in freq_dict:
            freq_dict[word] = 1
        else:
            freq_dict[word] += 1
    return freq_dict
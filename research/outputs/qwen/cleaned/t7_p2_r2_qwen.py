def word_frequency(text):
    word_count = {}
    words = text.split()
    for word in words:
        word = word.strip(' ,.!?;:"\'()[]{}')
        word = word.lower()
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    return word_count
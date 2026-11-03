from collections import Counter

def word_frequency(text):
    text = text.lower()
    import string
    translator = str.maketrans('', '', string.punctuation)
    cleaned_text = text.translate(translator)
    words = cleaned_text.split()
    word_count = Counter(words)
    return word_count
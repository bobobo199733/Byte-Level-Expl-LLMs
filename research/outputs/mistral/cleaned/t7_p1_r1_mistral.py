import string
from collections import Counter

def word_frequency(text):
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = text.lower()
    words = [word for word in text.split() if word]
    word_counts = Counter(words)
    return word_counts
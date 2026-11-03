import re
from collections import Counter

def word_frequency(text):
    words = re.findall('\\w+', text.lower())
    word_count = Counter(words)
    return word_count
from collections import defaultdict

def group_anagrams(words):
    if not isinstance(words, list):
        raise ValueError('Input must be a list')
    groups = defaultdict(list)
    for word in words:
        if not isinstance(word, str):
            raise ValueError('All elements in the list must be strings')
        sorted_word = ''.join(sorted(word))
        groups[sorted_word].append(word)
    return list(groups.values())
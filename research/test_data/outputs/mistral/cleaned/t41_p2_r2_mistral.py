from collections import defaultdict

def group_anagrams(words):
    groups = defaultdict(list)
    for word in words:
        if not isinstance(word, str):
            raise ValueError('Invalid input type. All elements must be strings.')
        sorted_word = list(sorted(word))
        groups[sorted_word].append(word)
    return list(groups.values())
def group_anagrams(words):
    if not isinstance(words, list) or any((not isinstance(word, str) for word in words)):
        raise ValueError('Invalid input: expected a list of strings')
    anagrams = {}
    for word in words:
        sorted_word = ''.join(sorted(word))
        anagrams.setdefault(sorted_word, []).append(word)
    return list(anagrams.values())
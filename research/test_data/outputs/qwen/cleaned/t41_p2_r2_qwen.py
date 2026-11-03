def group_anagrams(words):
    if not isinstance(words, list) or not all((isinstance(word, str) for word in words)):
        raise ValueError('Input must be a list of strings')
    anagram_groups = []
    anagram_map = {}
    for word in words:
        sorted_word = ''.join(sorted(word))
        if sorted_word in anagram_map:
            anagram_map[sorted_word].append(word)
        else:
            anagram_map[sorted_word] = [word]
    return list(anagram_map.values())
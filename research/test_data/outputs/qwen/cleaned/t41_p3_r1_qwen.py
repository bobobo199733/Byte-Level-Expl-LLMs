def group_anagrams(words):
    from collections import defaultdict
    anagram_groups = defaultdict(list)
    for word in words:
        sorted_word = ''.join(sorted(word))
        anagram_groups[sorted_word].append(word)
    return list(anagram_groups.values())
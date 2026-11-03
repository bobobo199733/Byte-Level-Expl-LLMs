from collections import defaultdict

def group_anagrams(words):
    anagram_groups = defaultdict(list)
    for word in words:
        sorted_word = ''.join(sorted(word))
        anagram_groups[sorted_word].append(word)
    result = list(anagram_groups.values())
    return result
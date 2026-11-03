from collections import defaultdict

def group_anagrams(words):
    anagram_groups = defaultdict(list)
    for word in words:
        sorted_word = sorted(list(word))
        anagram_groups[sorted_word].append(word)
    return list(anagram_groups.values())
def group_anagrams(words):
    anagram_groups = {}
    for word in words:
        sorted_word = ''.join(sorted(word))
        if sorted_word not in anagram_groups:
            anagram_groups[sorted_word] = [word]
        else:
            anagram_groups[sorted_word].append(word)
    return list(anagram_groups.values())
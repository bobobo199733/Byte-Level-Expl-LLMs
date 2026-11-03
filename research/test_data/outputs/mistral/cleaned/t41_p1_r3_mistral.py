def group_anagrams(words):
    groups = {}
    for word in words:
        sorted_word = ''.join(sorted(word))
        if sorted_word not in groups:
            groups[sorted_word] = [word]
        else:
            groups[sorted_word].append(word)
    return list(groups.values())
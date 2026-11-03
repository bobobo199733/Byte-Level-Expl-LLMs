def group_anagrams(words):
    groups = {}
    for word in words:
        sort_word = ''.join(sorted(word))
        if sort_word not in groups:
            groups[sort_word] = []
        groups[sort_word].append(word)
    return list(groups.values())
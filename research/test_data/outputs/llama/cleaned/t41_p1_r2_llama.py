def group_anagrams(words):
    """
    Groups together words that are anagrams of each other.

    Args:
        words (list): A list of words.

    Returns:
        list: A list of grouped anagrams.
    """
    anagrams = {}
    for word in words:
        sorted_word = ''.join(sorted(word))
        if sorted_word not in anagrams:
            anagrams[sorted_word] = [word]
        else:
            anagrams[sorted_word].append(word)
    return list(anagrams.values())
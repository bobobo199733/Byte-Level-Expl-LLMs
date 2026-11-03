def group_anagrams(words):
    """
    Groups together words that are anagrams of each other.

    Args:
        words (list): List of words to be grouped.

    Returns:
        list: List of lists, where each sublist contains anagrams.
    """
    anagrams_dict = {}
    for word in words:
        sorted_word = ''.join(sorted(word))
        if sorted_word in anagrams_dict:
            anagrams_dict[sorted_word].append(word)
        else:
            anagrams_dict[sorted_word] = [word]
    return list(anagrams_dict.values())

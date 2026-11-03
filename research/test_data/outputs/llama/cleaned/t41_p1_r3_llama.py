def group_anagrams(words):
    """
    Groups together words that are anagrams of each other.

    Args:
        words (list): A list of words.

    Returns:
        list: A list of grouped anagrams.
    """
    anagram_dict = {}
    for word in words:
        sorted_word = ''.join(sorted(word))
        if sorted_word in anagram_dict:
            anagram_dict[sorted_word].append(word)
        else:
            anagram_dict[sorted_word] = [word]
    grouped_anagrams = list(anagram_dict.values())
    return grouped_anagrams
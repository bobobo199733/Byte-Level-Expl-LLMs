def group_anagrams(words):
    """
    Groups a list of words into anagrams.

    Args:
        words (list): A list of strings, each representing a word.

    Returns:
        dict: A dictionary where the keys are the sorted characters of each word,
              and the values are lists of words that are anagrams of each other.
    """
    anagram_groups = {}
    for word in words:
        sorted_word = ''.join(sorted(word))
        if sorted_word in anagram_groups:
            anagram_groups[sorted_word].append(word)
        else:
            anagram_groups[sorted_word] = [word]
    return anagram_groups
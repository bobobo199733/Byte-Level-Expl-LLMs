def group_anagrams(words):
    """
    Groups anagrams together.

    Args:
        words (list): A list of strings.

    Returns:
        dict: A dictionary where each key is a sorted string and the value is a list of its anagrams.
    """
    grouped_anagrams = {}
    for word in words:
        sorted_word = ''.join(sorted(word))
        if sorted_word not in grouped_anagrams:
            grouped_anagrams[sorted_word] = []
        grouped_anagrams[sorted_word].append(word)
    return grouped_anagrams
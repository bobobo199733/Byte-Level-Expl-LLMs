from collections import defaultdict

def group_anagrams(words):
    """
    Group anagrams together.

    Args:
        words (list): A list of words to group by anagrams.

    Returns:
        dict: A dictionary where keys are the sorted versions of the words and values are lists of words that are anagrams of each other.
    """
    anagram_dict = defaultdict(list)
    for word in words:
        sorted_word = ''.join(sorted(word))
        anagram_dict[sorted_word].append(word)
    return dict(anagram_dict)
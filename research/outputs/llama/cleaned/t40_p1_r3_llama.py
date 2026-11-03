def autocomplete_system(words, prefix):
    """
    Returns a list of words from the given list that match the provided prefix,
    sorted in ascending order.

    Args:
        words (list): List of words to search through.
        prefix (str): Prefix to search for.

    Returns:
        list: Sorted list of matching words.
    """
    if not words or not prefix:
        return []
    matching_words = sorted([word for word in words if word.startswith(prefix)])
    return matching_words
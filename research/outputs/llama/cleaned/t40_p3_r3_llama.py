def autocomplete_system(words, prefix):
    """
    Returns a list of matching autocomplete suggestions.

    Args:
        words (list): List of words to search from.
        prefix (str): Prefix to match against words.

    Returns:
        list: Sorted list of matching autocomplete suggestions.
    """
    return sorted([word for word in words if word.startswith(prefix)])
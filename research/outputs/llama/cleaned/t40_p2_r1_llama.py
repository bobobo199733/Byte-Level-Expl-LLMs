def autocomplete_system(words, prefix):
    """
    Returns all words from the given list that start with the provided prefix.

    Args:
        words (list): A list of strings to be searched.
        prefix (str): The starting characters for the search.

    Returns:
        list: A sorted list of words matching the prefix.

    Example usage:
        >>> autocomplete_system(['apple', 'banana', 'apricot'], 'a')
        ['apple', 'apricot']
    """
    if not words or not prefix:
        return []
    matching_words = sorted([word for word in words if word.startswith(prefix)])
    return matching_words
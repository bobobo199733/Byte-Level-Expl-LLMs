def autocomplete_system(words, prefix):
    """
    Returns a list of words from the given list that match the provided prefix.

    Args:
        words (list): List of words to search in.
        prefix (str): The prefix to match against each word.

    Returns:
        list: Sorted list of matching words. If no matches are found, an empty list is returned.
    """
    if not words or not prefix:
        return []
    filtered_words = [word for word in words if word.startswith(prefix)]
    return sorted(filtered_words)
def autocomplete_system(words, prefix):
    """
    Returns a list of words that start with the given prefix.

    Args:
        words (list): A list of words to search through.
        prefix (str): The prefix to match against.

    Returns:
        list: A sorted list of words that start with the given prefix.
    """
    if not words or not prefix:
        return []
    suggestions = [word for word in words if word.startswith(prefix)]
    return sorted(suggestions)
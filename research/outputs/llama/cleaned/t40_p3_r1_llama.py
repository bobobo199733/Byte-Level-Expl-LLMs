def autocomplete_system(words, prefix):
    """
    Returns a list of words that match the given prefix.

    Args:
        words (list): A list of words to search in.
        prefix (str): The prefix to match against each word.

    Returns:
        list: A sorted list of matching suggestions.
    """
    matches = [word for word in words if word.startswith(prefix)]
    matches.sort()
    return matches
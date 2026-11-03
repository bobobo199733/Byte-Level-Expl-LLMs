def autocomplete_system(words, prefix):
    """
    Returns a sorted list of autocomplete suggestions given a prefix.

    Args:
        words (list): A list of words to search from.
        prefix (str): The prefix to match.

    Returns:
        list: A sorted list of matching autocomplete suggestions.
    """
    matches = [word for word in words if word.startswith(prefix)]
    matches.sort()
    return matches
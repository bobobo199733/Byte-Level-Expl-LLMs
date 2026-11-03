def autocomplete_system(words, prefix):
    """
    Returns a list of words from the given word list that match the provided prefix,
    sorted alphabetically.

    Args:
        words (list): A list of words to search through.
        prefix (str): The prefix to match against.

    Returns:
        list: A list of matching words in alphabetical order.
    """
    if not words or not prefix:
        return []
    matching_words = [word for word in words if word.startswith(prefix)]
    matching_words.sort()
    return matching_words
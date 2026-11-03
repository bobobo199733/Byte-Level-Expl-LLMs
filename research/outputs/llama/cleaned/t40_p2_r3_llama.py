def autocomplete_system(words, prefix):
    """
    Returns a sorted list of words from `words` that start with the given `prefix`.

    :param words: A list of words to search in.
    :param prefix: The prefix to search for.
    :return: A sorted list of words that match the prefix.
    """
    if not isinstance(words, list) or not all((isinstance(word, str) for word in words)):
        raise ValueError('Input `words` must be a non-empty list of strings')
    if not isinstance(prefix, str):
        raise ValueError('Prefix must be a string')
    matching_words = [word for word in words if word.startswith(prefix)]
    return sorted(matching_words)
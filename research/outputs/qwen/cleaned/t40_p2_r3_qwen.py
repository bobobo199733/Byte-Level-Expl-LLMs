def autocomplete_system(words, prefix):
    if not words or not prefix:
        return []
    matching_words = [word for word in words if word.startswith(prefix)]
    matching_words.sort()
    return matching_words
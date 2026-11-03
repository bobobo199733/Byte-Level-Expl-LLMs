def autocomplete_system(words, prefix):
    if not words:
        return []
    matching_words = [word for word in words if word.startswith(prefix)]
    return sorted(matching_words)
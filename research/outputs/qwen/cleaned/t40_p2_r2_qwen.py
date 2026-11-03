def autocomplete_system(words, prefix):
    if not words:
        return []
    filtered_words = [word for word in words if word.startswith(prefix)]
    return sorted(filtered_words)